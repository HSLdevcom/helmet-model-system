from argparse import ArgumentParser
import os
import numpy

from utils.config import Config
import utils.log as log
from utils.validate_network import validate
from assignment.emme_assignment import EmmeAssignmentModel
from assignment.mock_assignment import MockAssignmentModel
from datahandling.matrixdata import MatrixData
from datahandling.zonedata import ZoneData
import parameters.assignment as param


def main(args):
    base_zonedata_path = os.path.join(args.baseline_data_path, "2016_zonedata")
    base_matrices_path = os.path.join(args.baseline_data_path, "base_matrices")
    emme_paths = args.emme_paths
    first_scenario_ids = args.first_scenario_ids
    forecast_zonedata_paths = args.forecast_data_paths

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
            msg = "Mock Results directory {} does not exist.".format(
                mock_result_path)
            log.error(msg)
            raise NameError(msg)
        assignment_model = MockAssignmentModel(MatrixData(mock_result_path))
        zone_numbers = assignment_model.zone_numbers
    else:
        emp_path = emme_paths[0]
        if not os.path.isfile(emp_path):
            msg = ".emp project file not found in given '{}' location.".format(
                emp_path)
            log.error(msg)
            raise ValueError(msg)
        import inro.emme.desktop.app as _app
        app = _app.start_dedicated(
            project=emp_path, visible=False, user_initials="HSL")
        scen = app.data_explorer().active_database().core_emmebank.scenario(
            first_scenario_ids[0])
        if scen is None:
            msg = "Project {} has no scenario {}".format(emp_path, scen.id)
            log.error(msg)
            raise ValueError(msg)
        else:
            zone_numbers = scen.zone_numbers
        app.close()
    # Check base zonedata
    base_zonedata = ZoneData(base_zonedata_path, zone_numbers)
    # Check base matrices
    matrixdata = MatrixData(base_matrices_path)
    for tp in ("aht", "pt", "iht"):
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
            nr_attr = {
                # Number of existing extra attributes
                # TODO Count existing extra attributes which are NOT included
                # in the set of attributes created during model run
                "nodes": 0,
                "links": 4,
                "transit_lines": 3,
                "transit_segments": 0,
            }
            nr_transit_classes = len(param.transit_classes)
            nr_segment_results = len(param.segment_results)
            nr_vehicle_classes = len(param.emme_demand_mtx) + 1
            nr_new_attr = {
                "nodes": nr_transit_classes * (nr_segment_results-1),
                "links": nr_vehicle_classes + 3,
                "transit_lines": 0,
                "transit_segments": nr_transit_classes*nr_segment_results + 1,
            }
            if not args.save_matrices:
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
            scen = emmebank.scenario(first_scenario_ids[i])
            if scen is None:
                msg = "Project {} has no scenario {}".format(emp_path, scen.id)
                log.error(msg)
                raise ValueError(msg)
            elif scen.zone_numbers != zone_numbers:
                msg = "Zone numbers do not match for EMME scenario {}".format(
                    scen.id)
                log.error(msg)
                raise ValueError(msg)
            attrs = (
                "@pyoratieluokka",
                "@hinta_aht",
                "@hinta_pt",
                "@hinta_iht",
                "@hw_aht",
                "@hw_pt",
                "@hw_iht",
            )
            for attr in attrs:
                if scen.extra_attribute(attr) is None:
                    msg = "Extra attribute {} missing from scenario {}".format(
                        attr, scen.id)
            validate(scen.get_network(), forecast_zonedata.transit_zone)
            app.close()

    log.info("Successfully validated all input files")


if __name__ == "__main__":
    # Initially read defaults from config file ("dev-config.json")
    # but allow override via command-line arguments
    config = Config().read_from_file()
    parser = ArgumentParser(epilog="HELMET model system entry point script.")
    # Logging
    parser.add_argument(
        "--log-level",
        dest="log_level",
        choices={"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"},
        default=config.LOG_LEVEL,
    )
    parser.add_argument(
        "--log-format",
        dest="log_format",
        choices={"TEXT", "JSON"},
        default=config.LOG_FORMAT,
    )
    parser.add_argument(
        "--do-not-use-emme",
        dest="do_not_use_emme",
        action="store_true",
        default=(not config.USE_EMME),
        help="Using this flag runs with MockAssignmentModel instead of EmmeAssignmentModel, not requiring EMME.",
    )
    parser.add_argument(
        "--save-emme-matrices",
        dest="save_matrices",
        action="store_true",
        default=config.SAVE_MATRICES_IN_EMME,
        help="Using this flag saves additional matrices and strategy files to Emme-project Database folder.",
    )
    parser.add_argument(
        "--scenario-name",
        dest="scenario_name",
        type=str,
        default=config.SCENARIO_NAME,
        help="Name of HELMET scenario. Influences result folder name and log file name."),
    parser.add_argument(
        "--results-path",
        dest="results_path",
        type=str,
        default=config.RESULTS_PATH,
        help="Path to folder where result data is saved to."),
    # Base input (across all scenarios)
    parser.add_argument(
        "--baseline-data-path",
        dest="baseline_data_path",
        type=str,
        default=config.BASELINE_DATA_PATH,
        help="Path to folder containing both baseline zonedata and -matrices (Given privately by project manager)"),
    # Scenarios' individual input
    parser.add_argument(
        "--emme-paths",
        dest="emme_paths",
        type=str,
        nargs="+",
        required=True,
        help="List of filepaths to .emp EMME-project-files"),
    parser.add_argument(
        "--first-scenario-ids",
        dest="first_scenario_ids",
        type=int,
        nargs="+",
        required=True,
        help="List of first (biking) scenario IDs within EMME project (.emp)."),
    parser.add_argument(
        "--forecast-data-paths",
        dest="forecast_data_paths",
        type=str,
        nargs="+",
        required=True,
        help="List of paths to folder containing forecast zonedata"),
    args = parser.parse_args()

    config.LOG_LEVEL = args.log_level
    config.LOG_FORMAT = args.log_format
    config.SCENARIO_NAME = "input_file_validation"
    config.RESULTS_PATH = args.results_path
    log.initialize(config)

    main(args)
