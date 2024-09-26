from argparse import ArgumentParser
import os
import sys
from typing import List, Union

import utils.config
import utils.log as log
from utils.validate_network import validate
from assignment.mock_assignment import MockAssignmentModel
from datahandling.matrixdata import MatrixData
from datahandling.zonedata import ZoneData
import parameters.assignment as param


def main(args):
    base_zonedata_path = os.path.join(args.baseline_data_path, "2018_zonedata")
    base_matrices_path = os.path.join(args.baseline_data_path, "base_matrices")
    emme_paths: Union[str,List[str]] = args.emme_paths
    first_scenario_ids: Union[int,List[int]] = args.first_scenario_ids
    forecast_zonedata_paths: Union[str,List[str]] = args.forecast_data_paths

    if not emme_paths:
        msg = "Missing required argument 'emme-paths'."
        log.error(msg)
        raise ValueError(msg)
    if not first_scenario_ids:
        msg = "Missing required argument 'first-scenario-ids'."
        log.error(msg)
        raise ValueError(msg)
    if not forecast_zonedata_paths:
        msg = "Missing required argument 'forecast-zonedata-paths'."
        log.error(msg)
        raise ValueError(msg)
    # Check arg lengths
    if not (len(emme_paths) == len(first_scenario_ids)):
        msg = ("Non-matching number of emme-paths (.emp files) "
               + "vs. number of first-scenario-ids")
        log.error(msg)
        raise ValueError(msg)
    if not (len(emme_paths) == len(forecast_zonedata_paths)):
        msg = ("Non-matching number of emme-paths (.emp files) "
               + "vs. number of forecast-zonedata-paths")
        log.error(msg)
        raise ValueError(msg)

    # Check basedata input
    log.info("Checking base inputdata...")
    # Check filepaths (& first .emp path for zone_numbers in base zonedata)
    if not os.path.exists(base_zonedata_path):
        msg = "Baseline zonedata directory '{}' does not exist.".format(
            base_zonedata_path)
        log.error(msg)
        raise ValueError(msg)
    if not os.path.exists(base_matrices_path):
        msg = "Baseline matrices' directory '{}' does not exist.".format(
            base_matrices_path)
        log.error(msg)
        raise ValueError(msg)
    if args.do_not_use_emme:
        mock_result_path = os.path.join(
            args.results_path, args.scenario_name, "Matrices")
        if not os.path.exists(mock_result_path):
            log.info("Matrices folder does not exist, copying the folder from test scenario")
            test_path = os.path.join(args.results_path,"test","Matrices")
            import shutil
            shutil.copytree(test_path, mock_result_path)
        assignment_model = MockAssignmentModel(MatrixData(mock_result_path))
        zone_numbers = assignment_model.zone_numbers
    else:
        emp_path = emme_paths[0]
        if not os.path.isfile(emp_path):
            msg = ".emp project file not found in given '{}' location.".format(
                emp_path)
            log.error(msg)
            raise ValueError(msg)
        import inro.emme.desktop.app as _app # type: ignore
        app = _app.start_dedicated(
            project=emp_path, visible=False, user_initials="HSL")
        scen = app.data_explorer().active_database().core_emmebank.scenario(
            first_scenario_ids[0])
        if scen is None:
            msg = "Project {} has no scenario {}".format(emp_path, first_scenario_ids[0])
            log.error(msg)
            raise ValueError(msg)
        else:
            zone_numbers = scen.zone_numbers
        app.close()
    # Check base zonedata
    base_zonedata = ZoneData(base_zonedata_path, zone_numbers)
    # Check base matrices
    matrixdata = MatrixData(base_matrices_path)
    for tp in param.time_periods:
        with matrixdata.open("demand", tp, zone_numbers) as mtx:
            for ass_class in param.transport_classes:
                a = mtx[ass_class]

    # Check scenario based input data
    log.info("Checking base zonedata & scenario-based input data...")
    for i, emp_path in enumerate(emme_paths):
        log.info("Checking input data for scenario #{} ...".format(i))

        # Check forecasted zonedata
        if not os.path.exists(forecast_zonedata_paths[i]):
            msg = "Forecast data directory '{}' does not exist.".format(
                forecast_zonedata_paths[i])
            log.error(msg)
            raise ValueError(msg)
        forecast_zonedata = ZoneData(forecast_zonedata_paths[i], zone_numbers)

        # Check network
        if not args.do_not_use_emme:
            if not os.path.isfile(emp_path):
                msg = ".emp project file not found in given '{}' location.".format(
                    emp_path)
                log.error(msg)
                raise ValueError(msg)
            app = _app.start_dedicated(
                project=emp_path, visible=False, user_initials="HSL")
            emmebank = app.data_explorer().active_database().core_emmebank
            link_attrs = ["@pyoratieluokka"]
            line_attrs = []
            for tp in param.time_periods:
                link_attrs.append(f"@hinta_{tp}")
                line_attrs.append(f"@hw_{tp}")
            nr_attr = {
                # Number of existing extra attributes
                # TODO Count existing extra attributes which are NOT included
                # in the set of attributes created during model run
                "nodes": 0,
                "links": len(link_attrs),
                "transit_lines": len(line_attrs),
                "transit_segments": 0,
            }
            nr_transit_classes = len(param.transit_classes)
            nr_segment_results = len(param.segment_results)
            nr_vehicle_classes = len(param.emme_matrices)
            nr_new_attr = {
                "nodes": nr_transit_classes * (nr_segment_results-1),
                "links": nr_vehicle_classes + 4,
                "transit_lines": 0,
                "transit_segments": nr_transit_classes*nr_segment_results + 1,
            }
            sc_name = emmebank.scenario(first_scenario_ids[i]).title
            if len(sc_name)>56:
                msg = "Scenario name: {} too long, time period extension might exceed Emme's 60 characters limit.".format(
                    sc_name)
                log.error(msg)
                raise ValueError(msg)     
            if not args.separate_emme_scenarios:
                # If results from all time periods are stored in same
                # EMME scenario
                for key in nr_new_attr:
                    nr_new_attr[key] *= 4
            # Attributes created during congested transit assignment
            nr_new_attr["transit_segments"] += 3
            dim = emmebank.dimensions
            dim["nodes"] = dim["centroids"] + dim["regular_nodes"]
            attr_space = 0
            for key in nr_attr:
                attr_space += dim[key] * (nr_attr[key]+nr_new_attr[key])
            if dim["extra_attribute_values"] < attr_space:
                msg = "At least {} words required for extra attributes".format(
                    attr_space)
                log.error(msg)
                raise ValueError(msg)
            for scen in emmebank.scenarios():
                if scen.zone_numbers != zone_numbers:
                    log.warn("Scenarios with different zones found in EMME bank!")
            scen = emmebank.scenario(first_scenario_ids[i])
            if scen is None:
                msg = "Project {} has no scenario {}".format(emp_path, first_scenario_ids[i])
                log.error(msg)
                raise ValueError(msg)
            elif scen.zone_numbers != zone_numbers:
                msg = "Zone numbers do not match for EMME scenario {}".format(
                    scen.id)
                log.error(msg)
                raise ValueError(msg)
            for attr in link_attrs + line_attrs:
                if scen.extra_attribute(attr) is None:
                    msg = "Extra attribute {} missing from scenario {}".format(
                        attr, scen.id)
                    log.error(msg)
                    raise ValueError(msg)
            validate(scen.get_network(), forecast_zonedata.transit_zone)
            app.close()

    log.info("Successfully validated all input files")


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
    args = parser.parse_args()

    log.initialize(args)

    if sys.version_info.major == 3:
        main(args)
    else:
        log.error("Python version not supported, must use version 3")
