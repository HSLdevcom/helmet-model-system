from argparse import ArgumentParser
import os
import numpy

from utils.config import Config
from utils.log import Log
from assignment.emme_assignment import EmmeAssignmentModel
from datahandling.matrixdata import MatrixData
from datahandling.zonedata import ZoneData
from assignment.emme_bindings.emme_project import EmmeProject
import parameters.assignment as param


def main(args, logger):
    base_zonedata_path = os.path.join(args.baseline_data_path, "2016_zonedata")
    base_matrices_path = os.path.join(args.baseline_data_path, "base_matrices")
    emme_paths = args.emme_paths
    first_scenario_ids = args.first_scenario_ids
    forecast_zonedata_paths = args.forecast_data_paths

    if not emme_paths:
        logger.error("Missing required argument 'emme-paths'.")
        raise ValueError("Missing required argument 'emme-paths'.")
    if not first_scenario_ids:
        logger.error("Missing required argument 'first-scenario-ids'.")
        raise ValueError("Missing required argument 'first-scenario-ids'.")
    if not forecast_zonedata_paths:
        logger.error("Missing required argument 'forecast-zonedata-paths'.")
        raise ValueError("Missing required argument 'forecast-zonedata-paths'.")
    # Check arg lengths
    if not (len(emme_paths) == len(first_scenario_ids)):
        logger.error("Non-matching number of emme-paths (.emp files) vs. number of first-scenario-ids")
        raise ValueError("Non-matching number of emme-paths (.emp files) vs. number of first-scenario-ids")
    if not (len(emme_paths) == len(forecast_zonedata_paths)):
        logger.error("Non-matching number of emme-paths (.emp files) vs. number of forecast-zonedata-paths")
        raise ValueError("Non-matching number of emme-paths (.emp files) vs. number of forecast-zonedata-paths")

    # Check basedata input
    logger.info("Checking base inputdata...")
    # Check filepaths (& first .emp path for zone_numbers in base zonedata)
    if not os.path.exists(base_zonedata_path):
        logger.error("Baseline zonedata directory '{}' does not exist.".format(base_zonedata_path))
        raise ValueError("Baseline zonedata directory '{}' does not exist.".format(base_zonedata_path))
    if not os.path.exists(base_matrices_path):
        logger.error("Baseline matrices' directory '{}' does not exist.".format(base_matrices_path))
        raise ValueError("Baseline matrices' directory '{}' does not exist.".format(base_matrices_path))
    if not os.path.isfile(emme_paths[0]):
        raise ValueError(".emp project file not found in given '{}' location.".format(emme_paths[0]))
    # Check base zonedata
    assignment_model = EmmeAssignmentModel(EmmeProject(emme_paths[0]), first_scenario_id=first_scenario_ids[0])
    base_zonedata = ZoneData(base_zonedata_path, assignment_model.zone_numbers)
    # Check base matrices
    matrixdata = MatrixData(base_matrices_path)
    for tp in assignment_model.emme_scenarios:
        # TODO Move checks to MatrixData
        with matrixdata.open("demand", tp) as mtx:
            path = os.path.join(base_matrices_path, "demand_"+tp+".omx")
            # TODO Get these as numpy arrays from source
            ass_numbers = numpy.array(assignment_model.zone_numbers)
            mtx_numbers = numpy.array(mtx.zone_numbers)
            if not (numpy.diff(mtx_numbers) > 0).all():
                raise IndexError("Zone numbers not in strictly ascending order in file {}".format(path))
            if mtx_numbers.size != ass_numbers.size or (mtx_numbers != ass_numbers).any():
                for i in mtx_numbers:
                    if int(i) not in ass_numbers:
                        raise IndexError("Zone number {} from file {} not found in network".format(i, path))
                for i in ass_numbers:
                    if i not in mtx_numbers:
                        raise IndexError("Zone number {} not found in file {}".format(i, path))
                raise IndexError("Zone numbers did not match for file {}".format(path))
            ass_classes = mtx.matrix_list
            for ass_class in param.transport_classes:
                if ass_class not in ass_classes:
                    raise IndexError("File {} does not contain {} matrix.".format(
                        path, ass_class))
                a = mtx[ass_class]
                if a.shape[0] != mtx_numbers.size or a.shape[1] != mtx_numbers.size:
                    raise IndexError("Matrix {} in file {} has wrong dimensions".format(
                        ass_class, path))

    # Check scenario based input data
    logger.info("Checking base zonedata & scenario-based input data...")
    for i, emp_path in enumerate(emme_paths):
        logger.info("Checking input data for scenario #{} ...".format(i))

        # Check filepaths
        if not os.path.isfile(emp_path):
            raise ValueError(".emp project file not found in given '{}' location.".format(emp_path))
        if not os.path.exists(forecast_zonedata_paths[i]):
            raise ValueError("Forecast data directory '{}' does not exist.".format(forecast_zonedata_paths[i]))

        # Check forecasted zonedata
        forecast_zonedata = ZoneData(forecast_zonedata_paths[i], assignment_model.zone_numbers)

    logger.info("Successfully validated all input files")


if __name__ == "__main__":
    # Initially read defaults from config file ("dev-config.json") but allow override via command-line arguments
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

    # This should be refactored some day to use Python base logger (which is in-built singleton already)
    config.LOG_LEVEL = args.log_level
    config.LOG_FORMAT = args.log_format
    config.SCENARIO_NAME = "input_file_validation"
    logger = Log.get_instance().initialize(config)

    main(args, logger)
