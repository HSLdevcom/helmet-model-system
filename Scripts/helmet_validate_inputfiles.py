import os
import sys
from argparse import ArgumentParser
from contextlib import contextmanager
from typing import List, Union

import utils.config
import utils.log as log
from utils.validate_network import validate, validate_network_connectivity
from assignment.mock_assignment import MockAssignmentModel
from datahandling.matrixdata import MatrixData
from datahandling.zonedata import ZoneData
import parameters.assignment as param




def main(args):
    # Variables from args
    base_zonedata_path = os.path.join(args.baseline_data_path, "2023_zonedata")
    base_matrices_path = os.path.join(args.baseline_data_path, "base_matrices")
    emme_paths: List[str] = args.emme_paths
    first_scenario_ids: List[int] = args.first_scenario_ids
    forecast_zonedata_paths: List[str] = args.forecast_data_paths
    do_not_use_emme: bool = args.do_not_use_emme
    if not do_not_use_emme:
        separate_emme_scenarios: bool = args.separate_emme_scenarios
    else: 
        separate_emme_scenarios = False
    results_path: str = args.results_path
    scenario_name: str = args.scenario_name
    # Validation
    errors = 0
    errors += validate_arguments(emme_paths, first_scenario_ids, forecast_zonedata_paths)
    base_input_errors, zone_numbers = validate_base_input_data(base_zonedata_path, base_matrices_path, emme_paths, first_scenario_ids, results_path, scenario_name, do_not_use_emme)
    if zone_numbers is None:
        msg = f"Zone numbers could not be determined from EMME or MockAssignmentModel, cannot continue with validation. Input file validation failed with {errors} error(s)."
        log.error(msg)
        raise ValueError(msg)
    errors += base_input_errors
    scenario_input_errors, different_zones = validate_scenario_input_data(emme_paths, first_scenario_ids, forecast_zonedata_paths, zone_numbers, do_not_use_emme, separate_emme_scenarios)
    errors += scenario_input_errors
    # Different zones logged separately here to prevent it being printed for every scenario
    if different_zones:
        log.warn("Scenarios with different zones found in EMME bank! Matrices will not be compatible between scenarios with different zones.")
    if errors > 0:
        msg = f"Scenario validation failed with {errors} error(s)."
        log.error(msg)
        raise ValueError(msg)            
    log.info("Successfully validated all input files")
    log.info("Validating scenario networks...")
    for i, emp_path in enumerate(emme_paths):
        scenario_id = first_scenario_ids[i]
        forecast_zonedata = ZoneData(forecast_zonedata_paths[i], zone_numbers)
        if do_not_use_emme:
            continue
        with open_emme(emp_path) as (app,_m):
            emmebank = app.data_explorer().active_database().core_emmebank
            scen = emmebank.scenario(scenario_id)
            if scen is None:
                msg = "Project {} has no scenario {}".format(emp_path, scenario_id)
                log.error(msg)
                raise ValueError(msg)
            # NOTE: validate_network.validate() will not go through all scenarios if errors are found in one of them
            modeller = _m.Modeller(app)
            validate(scen.get_network(), forecast_zonedata.transit_zone)
            if not args.skip_test_network_connectivity:
                validate_network_connectivity(modeller, scen)
    log.info("Successfully validated all scenario networks")

def validate_arguments(emme_paths, first_scenario_ids, forecast_zonedata_paths):
    errors = 0
    # Cheching if arguments exist is not necessary, argparse will already check them and there should not be an issue when using Helmet UI anyway.
    # Check arg lengths
    if not (len(emme_paths) == len(first_scenario_ids)):
        msg = ("Non-matching number of emme-paths (.emp files) "
               + "vs. number of first-scenario-ids")
        log.error(msg)
        errors += 1
    if not (len(emme_paths) == len(forecast_zonedata_paths)):
        msg = ("Non-matching number of emme-paths (.emp files) "
               + "vs. number of forecast-zonedata-paths")
        log.error(msg)
        errors += 1
    return errors

def validate_database_extra_attrs_size(emmebank, scenario_id, separate_emme_scenarios):
    errors = 0
    # Count extra attributes and their space requirements
    nr_attr = {
        # Number of existing extra attributes
        # TODO Count existing extra attributes which are NOT included
        # in the set of attributes created during model run
        "nodes": 0,
        "links": 0,
        "transit_lines": 0,
        "transit_segments": 0,
    }

    for extra_attribute in emmebank.scenario(scenario_id).extra_attributes():
        if extra_attribute.type == "NODE":
            nr_attr["nodes"] += 1
        elif extra_attribute.type == "LINK":
            nr_attr["links"] += 1
        elif extra_attribute.type == "TRANSIT_LINE":
            nr_attr["transit_lines"] += 1
        elif extra_attribute.type == "TRANSIT_SEGMENT":
            nr_attr["transit_segments"] += 1
    nr_transit_classes = len(param.transit_classes)
    nr_segment_results = len(param.segment_results)
    nr_vehicle_classes = len(param.emme_matrices)
    nr_new_attr = {
        "nodes": nr_transit_classes * (nr_segment_results-1),
        "links": nr_vehicle_classes + 5,  # 5 extra attributes for car assignment (total_cost, toll_cost, car_time, bike_time, aux_transit)
        "transit_lines": 0,
        "transit_segments": nr_transit_classes*nr_segment_results + 1,
    }
    if not separate_emme_scenarios:
        # If results from all time periods are stored in same
        # EMME scenario
        for key in nr_new_attr:
            nr_new_attr[key] *= 4
    # Attributes created during congested transit assignment
    nr_new_attr["transit_segments"] += 3
    dim = emmebank.dimensions
    dim["nodes"] = dim["centroids"] + dim["regular_nodes"]
    attr_space_new = 0
    attr_space_existing = 0
    for key in nr_attr:
        attr_space_new += dim[key] * nr_new_attr[key]
        attr_space_existing += dim[key] * nr_attr[key]
    # TODO: A better approach would actually compare all the existing individual extra attributes against extra attributes to be created.
    # Currently, if a user has created many custom extra_attributes, we might think that there is sufficient space when there actually isn't
    if attr_space_new < attr_space_existing:  # Model has already run and extra attributes have been created
        attr_space = attr_space_existing
    else:  # Model has not run yet and extra attributes need to be created
        attr_space = attr_space_existing + attr_space_new
    log.debug(f"Extra attributes require {attr_space} words")
    if dim["extra_attribute_values"] < attr_space:
        msg = "At least {} words required for extra attributes".format(
            attr_space)
        log.error(msg)
        errors += 1
        return errors
    return errors

def validate_base_input_data(base_zonedata_path, base_matrices_path, emme_paths, first_scenario_ids, results_path, scenario_name, do_not_use_emme):
    errors = 0
    zone_numbers = None
    log.info("Checking base inputdata...")
    # Check filepaths (& first .emp path for zone_numbers in base zonedata)
    if not os.path.exists(base_zonedata_path):
        msg = "Baseline zonedata directory '{}' does not exist.".format(
            base_zonedata_path)
        log.error(msg)
        errors += 1
    if not os.path.exists(base_matrices_path):
        msg = "Baseline matrices' directory '{}' does not exist.".format(
            base_matrices_path)
        log.error(msg)
        errors += 1
    
    # Get zone numbers for base zonedata validation, either from EMME or from MockAssiginmentModel
    if do_not_use_emme:
        mock_result_path = os.path.join(
            results_path, scenario_name, "Matrices")
        if not os.path.exists(mock_result_path):
            msg = "Mock Results directory {} does not exist.".format(
                mock_result_path)
            log.error(msg)
            errors += 1
        assignment_model = MockAssignmentModel(MatrixData(mock_result_path))
        zone_numbers = assignment_model.zone_numbers
    else:
        emp_path = emme_paths[0]
        if not os.path.isfile(emp_path):
            msg = ".emp project file not found in given '{}' location.".format(
                emp_path)
            log.error(msg)
            errors += 1
        with open_emme(emp_path) as (app,_):
            log.debug(f"Emme version: {app.version}")
            scen = app.data_explorer().active_database().core_emmebank.scenario(
                first_scenario_ids[0])
            if scen is None:
                msg = "Project {} has no scenario {}".format(emp_path, first_scenario_ids[0])
                log.error(msg)
                errors += 1
            else:
                zone_numbers = scen.zone_numbers
    # Check base zonedata
    base_zonedata = ZoneData(base_zonedata_path, zone_numbers)
    # Check base matrices
    try: 
        matrixdata = MatrixData(base_matrices_path)
        for tp in param.time_periods:
            with matrixdata.open("demand", tp, zone_numbers) as mtx:
                for ass_class in param.transport_classes:
                    a = mtx[ass_class]
    except Exception as e:
        msg = f"Error reading base matrices: {e}"
        log.error(msg)
        errors += 1
    
    return errors, zone_numbers


def validate_scenario_input_data(emme_paths, first_scenario_ids, forecast_zonedata_paths, zone_numbers, do_not_use_emme, separate_emme_scenarios):
    # Check scenario based input data
    log.info("Checking input data and network(s) for scenario(s)...")
    errors = 0
    different_zones = False 
    for i, emp_path in enumerate(emme_paths):
        scenario_id = first_scenario_ids[i]
        log.info(f"Checking input data for the {number_to_ordinal(i+1)} scenario #{scenario_id} ...")

        # Check forecasted zonedata
        if not os.path.exists(forecast_zonedata_paths[i]):
            msg = "Forecast data directory '{}' does not exist.".format(
                forecast_zonedata_paths[i])
            log.error(msg)
            errors += 1
        forecast_zonedata = ZoneData(forecast_zonedata_paths[i], zone_numbers)

        # Stop validation if EMME is not being used
        if do_not_use_emme:
            continue
        # Continue validation if EMME is available
        with open_emme(emp_path) as (app,_):
            emmebank = app.data_explorer().active_database().core_emmebank

            errors += validate_database_extra_attrs_size(emmebank, scenario_id, separate_emme_scenarios)
            
            # Check if scenario name is too long
            sc_name = emmebank.scenario(scenario_id).title
            if len(sc_name)>56 and separate_emme_scenarios:
                msg = "Scenario name: {} too long, time period extension might exceed Emme's 60 characters limit.".format(
                    sc_name)
                log.error(msg)
                errors += 1

            # Check if emmebank has scenarios with different zone numbers
            scenarios_with_different_zones = 0
            for scen in emmebank.scenarios():
                compared_zone_numbers = scen.zone_numbers
                if len(compared_zone_numbers) < 1:  # Skip empty scenarios
                    continue
                if compared_zone_numbers != zone_numbers:
                    scenarios_with_different_zones += 1
            if scenarios_with_different_zones > 0:
                different_zones = True
            scen = emmebank.scenario(scenario_id)
            if scen is None:
                msg = "Project {} has no scenario {}".format(emp_path, scenario_id)
                log.error(msg)
                errors += 1
            elif scen.zone_numbers != zone_numbers:
                msg = "Zone numbers do not match for EMME scenario {}".format(
                    scen.id)
                log.error(msg)
                errors += 1
            log.info(f"Validating network for the {number_to_ordinal(i+1)} scenario #{scenario_id} ...")
            network_errors = validate(scen.get_network(), forecast_zonedata.transit_zone)
            if network_errors > 0:
                log.error(f"Network validation for scenario #{scenario_id} failed with {network_errors} errors.")
                errors += network_errors
    return errors, different_zones

@contextmanager
def open_emme(emp_path):
    import inro.emme.desktop.app as _app # type: ignore
    import inro.modeller as _m # type: ignore
    app = _app.start_dedicated(
        project=emp_path, visible=False, user_initials="HSL")
    try:
        yield (app,_m)
    finally:
        app.close()
    
def number_to_ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return str(n) + suffix



if __name__ == "__main__":
    # Initially read defaults from config file ("dev-config.json")
    # but allow override via command-line arguments
    config = utils.config.read_from_file()
    parser = ArgumentParser(epilog="HELMET model system entry point script.")
    # Logging
    parser.add_argument(
        "--log-level",
        choices={"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"},
        default=config.LOG_LEVEL,
    )
    parser.add_argument(
        "--log-format",
        choices={"TEXT", "JSON"},
        default=config.LOG_FORMAT,
    )
    parser.add_argument(
        "--do-not-use-emme",
        action="store_true",
        default=config.DO_NOT_USE_EMME,
        help="Using this flag runs with MockAssignmentModel instead of EmmeAssignmentModel, not requiring EMME.",
    )
    parser.add_argument(
        "-s", "--separate-emme-scenarios",
        action="store_true",
        default=config.SEPARATE_EMME_SCENARIOS,
        help="Using this flag creates four new EMME scenarios and saves network time-period specific results in them.",
    )
    parser.add_argument(
        "--scenario-name",
        type=str,
        default=config.SCENARIO_NAME,
        help="Name of HELMET scenario. Influences result folder name and log file name."),
    parser.add_argument(
        "--results-path",
        type=str,
        default=config.RESULTS_PATH,
        help="Path to folder where result data is saved to."),
    # Base input (across all scenarios)
    parser.add_argument(
        "--baseline-data-path",
        type=str,
        default=config.BASELINE_DATA_PATH,
        help="Path to folder containing both baseline zonedata and -matrices (Given privately by project manager)"),
    # Scenarios' individual input
    parser.add_argument(
        "--emme-paths",
        type=str,
        nargs="+",
        required=True,
        help="List of filepaths to .emp EMME-project-files"),
    parser.add_argument(
        "--first-scenario-ids",
        type=int,
        nargs="+",
        required=True,
        help="List of first (biking) scenario IDs within EMME project (.emp)."),
    parser.add_argument(
        "--forecast-data-paths",
        type=str,
        nargs="+",
        required=True,
        help="List of paths to folder containing forecast zonedata"),
    parser.add_argument(
        "--skip-test-network-connectivity",
        action="store_true",
        default=config.SKIP_NETWORK_CONNECTIVITY_TEST,
        help="Skip testing network connectivity."),
    args = parser.parse_args()

    log.initialize(args)

    if sys.version_info.major == 3:
        main(args)
    else:
        log.error("Python version not supported, must use version 3")
