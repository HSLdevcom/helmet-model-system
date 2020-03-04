from utils.config import Config
from utils.log import Log
from assignment.emme_assignment import EmmeAssignmentModel
from assignment.mock_assignment import MockAssignmentModel
from modelsystem import ModelSystem
from datahandling.matrixdata import MatrixData
from emme_bindings.emme_project import EmmeProject
from argparse import ArgumentParser
import sys
import os


def main(args, logger):
    name = args.scenario_name if args.scenario_name is not None else Config.DefaultScenario
    iterations = args.iterations
    base_zonedata_path = os.path.join(args.baseline_data_path, "2016_zonedata")
    base_matrices_path = os.path.join(args.baseline_data_path, "base_matrices")
    forecast_zonedata_path = args.forecast_data_path
    results_path = args.results_path
    emme_project_path = args.emme_path
    log_extra = {
        "status": {
            "name": name,
            "state": "starting",
            "current": 0,
            "completed": 0,
            "failed": 0,
            "total": args.iterations,
            "log": logger.get_filename()
        }
    }

    # Read input matrices (.omx) and zonedata (.csv), and initialize models (assignment model and model-system)
    logger.info("Initializing matrices and models..", extra=log_extra)
    # Check input data folders/files exist
    if not os.path.exists(base_zonedata_path):
        raise NameError("Baseline zonedata directory '{}' does not exist.".format(base_zonedata_path))
    if not os.path.exists(base_matrices_path):
        raise NameError("Baseline zonedata directory '{}' does not exist.".format(base_matrices_path))
    if not os.path.exists(forecast_zonedata_path):
        raise NameError("Forecast data directory '{}' does not exist.".format(forecast_zonedata_path))
    if not os.path.isfile(emme_project_path):
        raise NameError(".emp project file not found in given '{}' location.".format(emme_project_path))
    # Choose and initialize the Traffic Assignment (supply)model
    if args.do_not_use_emme:
        logger.info("Initializing MockAssignmentModel..")
        mock_result_path = os.path.join(results_path, args.scenario_name)
        if not os.path.exists(mock_result_path):
            raise NameError("Mock Results directory " + mock_result_path + " does not exist.")
        ass_model = MockAssignmentModel(MatrixData(mock_result_path))
    else:
        logger.info("Initializing Emme..")
        ass_model = EmmeAssignmentModel(EmmeProject(emme_project_path), first_scenario_id=args.first_scenario_id)
    # Initialize model system (wrapping Assignment-model, and providing Demand-calculations as Python modules)
    model = ModelSystem(forecast_zonedata_path, base_zonedata_path, base_matrices_path, results_path, ass_model, name)
    log_extra["status"]["results"] = model.mode_share

    # Run traffic assignment simulation for N iterations, on last iteration model-system will save the results
    log_extra["status"]["state"] = "preparing"
    logger.info("Starting simulation with {} iterations..".format(iterations), extra=log_extra)
    impedance = model.assign_base_demand(args.use_fixed_transit_cost)
    log_extra["status"]["state"] = "running"
    for i in range(1, iterations + 1):
        log_extra["status"]["current"] = i
        try:
            logger.info("Starting iteration {}".format(i), extra=log_extra)
            impedance = (model.run_iteration(impedance, is_last_iteration=True)
                         if i == iterations
                         else model.run_iteration(impedance))
            log_extra["status"]["completed"] += 1
        except Exception as error:
            log_extra["status"]["failed"] += 1
            logger.error("Exception at iteration {}".format(i), error)
            logger.error("Fatal error occured, simulation aborted.", extra=log_extra)
            break
        if i == iterations:
            log_extra["status"]['state'] = 'finished'
    logger.info("Simulation ended.", extra=log_extra)


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
    # HELMET scenario metadata
    parser.add_argument(
        "--do-not-use-emme",
        dest="do_not_use_emme",
        action="store_true",
        default=(not config.USE_EMME),
        help="Using this flag runs with MockAssignmentModel instead of EmmeAssignmentModel, not requiring EMME.",
    )
    parser.add_argument(
        "--scenario-name",
        dest="scenario_name",
        type=str,
        default=config.SCENARIO_NAME,
        help="Name of traffic assignment (HELMET) scenario. Influences result folder name and log file name."),
    parser.add_argument(
        "--results-path",
        dest="results_path",
        type=str,
        default=config.RESULTS_PATH,
        help="Path to folder where result data is saved to."),
    # HELMET scenario input data
    parser.add_argument(
        "--emme-path",
        dest="emme_path",
        type=str,
        default=config.EMME_PROJECT_PATH,
        help="Filepath to .emp EMME-project-file"),
    parser.add_argument(
        "--first-scenario-id",
        dest="first_scenario_id",
        type=int,
        default=config.FIRST_SCENARIO_ID,
        help="First (biking) scenario ID within EMME project (.emp)."),
    parser.add_argument(
        "--baseline-data-path",
        dest="baseline_data_path",
        type=str,
        default=config.BASELINE_DATA_PATH,
        help="Path to folder containing both baseline zonedata and -matrices (Given privately by project manager)"),
    parser.add_argument(
        "--forecast-data-path",
        dest="forecast_data_path",
        type=str,
        default=config.FORECAST_DATA_PATH,
        help="Path to folder containing forecast zonedata"),
    parser.add_argument(
        "--iterations",
        dest="iterations",
        type=int,
        default=config.ITERATION_COUNT,
        help="Number of traffic assignment iterations to run (each re-using previously calculated impedance)"),
    parser.add_argument(
        "--use-fixed-transit-cost",
        dest="use_fixed_transit_cost",
        action="store_true",
        default=config.USE_FIXED_TRANSIT_COST,
        help="Using this flag activates use of pre-calculated (fixed) transit costs."),
    args = parser.parse_args()

    # This should be refactored some day to use Python base logger (which is in-built singleton already)
    config.LOG_LEVEL = args.log_level
    config.LOG_FORMAT = args.log_format
    config.SCENARIO_NAME = args.scenario_name
    logger = Log.get_instance().initialize(config)
    logger.debug('sys.version_info=' + str(sys.version_info[0]))
    logger.debug('sys.path=' + str(sys.path))
    logger.debug('log_level=' + args.log_level)
    logger.debug('emme_path=' + args.emme_path)
    logger.debug('baseline_data_path=' + args.baseline_data_path)
    logger.debug('forecast_data_path=' + args.forecast_data_path)
    logger.debug('iterations=' + str(args.iterations))
    logger.debug('use_fixed_transit_cost=' + str(args.use_fixed_transit_cost))
    logger.debug('first_scenario_id=' + str(args.first_scenario_id))
    logger.debug('scenario_name=' + args.scenario_name)

    main(args, logger)
