from utils.config import Config
from utils.log import Log
from datahandling import resultdata
from assignment.emme_assignment import EmmeAssignmentModel
from assignment.mock_assignment import MockAssignmentModel
from modelsystem import ModelSystem
from datahandling.matrixdata import MatrixData
from emme.emme_context import EmmeContext
from argparse import ArgumentParser
import sys
import os


def main(config, logger):
    name = config.SCENARIO_NAME if config.SCENARIO_NAME is not None else Config.DefaultScenario
    iterations = config.ITERATION_COUNT
    log_extra = {
        "status": {
            "name": name,
            "state": "starting",
            "current": 0,
            "completed": 0,
            "failed": 0,
            "total": config.ITERATION_COUNT,
            "log": logger.get_filename()
        }
    }
    resultdata.set_path(name)

    # Read input matrices (.omx) and zonedata (.csv), and initialize models (assignment model and model-system)
    logger.info("Initializing matrices and models..", extra=log_extra)
    if config.USE_EMME:
        logger.info("Initializing Emme..")
        ass_model = EmmeAssignmentModel(EmmeContext(config.EMME_PROJECT_PATH), first_scenario_id=config.FIRST_SCENARIO_ID)
    else:
        logger.info("Initializing MockAssignmentModel..")
        mock_result_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "Matrices", config.SCENARIO_NAME)
        ass_model = MockAssignmentModel(MatrixData(mock_result_path))
    model = ModelSystem(config.DATA_PATH, "2016", "base", ass_model, name)
    log_extra["status"]["results"] = model.mode_share

    # Run traffic assignment simulation for N iterations, on last iteration model-system will save the results
    log_extra["status"]["state"] = "preparing"
    logger.info("Starting simulation with {} iterations..".format(iterations), extra=log_extra)
    impedance = model.assign_base_demand(Config.USE_FIXED_TRANSIT_COST)
    log_extra["status"]["state"] = "running"
    for i in range(1, iterations + 1):
        log_extra["status"]["current"] = i
        try:
            logger.info("Starting iteration {}".format(i), extra=log_extra)
            impedance = (model.run_iteration(impedance, is_last_iteration=True)
                         if i == iterations
                         else model.run_iteration(impedance))
            log_extra["status"]["completed"] = log_extra["status"]["completed"] + 1
        except Exception as error:
            log_extra["status"]["failed"] = log_extra["status"]["failed"] + 1
            logger.error("Exception at iteration {}".format(i), error)
            logger.error("Fatal error occured, simulation aborted.", extra=log_extra)
            break
        if i == iterations:
            log_extra["status"]['state'] = 'finished'
    logger.info("Simulation ended.", extra=log_extra)


if __name__ == "__main__":
    # Initially read config from file ("dev-config.json") but allow override via command-line arguments
    config = Config().read_from_file()
    parser = ArgumentParser(epilog="HELMET model system entry point script.")
    # Logging
    parser.add_argument("--log-level", dest="log_level", choices={"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})
    parser.add_argument("--log-format", dest="log_format", choices={"TEXT", "JSON"})
    # HELMET scenario metadata
    parser.add_argument(
        "--do-not-use-emme",
        dest="do_not_use_emme",
        action="store_true",
        default=False,
        help="Using this flag runs with MockAssignmentModel instead of EmmeAssignmentModel, not requiring EMME."
    )
    parser.add_argument(
        "--scenario-name",
        dest="scenario_name",
        type=str,
        help="Name of traffic assignment (HELMET) scenario. Influences result folder name and log file name.")
    # HELMET scenario input data
    parser.add_argument(
        "--emme-path",
        dest="emme_path",
        type=str,
        help="Filepath to .emp EMME-project-file")
    parser.add_argument(
        "--first-scenario-id",
        dest="first_scenario_id",
        type=int,
        help="First (biking) scenario ID within EMME project (.emp).")
    parser.add_argument(
        "--data-path",
        dest="data_path",
        type=str,
        help="Path to folder containing forecast zonedata")
    parser.add_argument(
        "--iterations",
        dest="iterations",
        type=int,
        help="Number of traffic assignment iterations to run (each re-using previously calculated impedance)")
    parser.add_argument(
        "--use-fixed-transit-cost",
        dest="use_fixed_transit_cost",
        action="store_true",
        default=False,
        help="Using this flag activates use of pre-calculated (fixed) transit costs.")
    args = parser.parse_args()

    # Optionally override each config value with args (if given)
    if args.log_level is not None:
        config.LOG_LEVEL = args.log_level
    if args.log_format is not None:
        config.LOG_FORMAT = args.log_format
    if args.do_not_use_emme:
        config.USE_EMME = False
    if args.scenario_name is not None:
        config.SCENARIO_NAME = args.scenario_name
    if args.emme_path is not None:
        config.EMME_PROJECT_PATH = args.emme_path
    if args.first_scenario_id is not None:
        config.FIRST_SCENARIO_ID = args.first_scenario_id
    if args.data_path is not None:
        config.DATA_PATH = args.data_path
    if args.iterations is not None:
        config.ITERATION_COUNT = args.iterations
    if args.use_fixed_transit_cost:
        config.USE_FIXED_TRANSIT_COST = True

    logger = Log.get_instance().initialize(config)
    logger.debug('sys.version_info=' + str(sys.version_info[0]))
    logger.debug('sys.path=' + str(sys.path))
    logger.debug('log_level=' + config.LOG_LEVEL)
    logger.debug('emme_path=' + config.EMME_PROJECT_PATH)
    logger.debug('data_path=' + config.DATA_PATH)
    logger.debug('iterations=' + str(config.ITERATION_COUNT))
    logger.debug('use_fixed_transit_cost=' + str(config.USE_FIXED_TRANSIT_COST))
    logger.debug('first_scenario_id=' + str(config.FIRST_SCENARIO_ID))
    logger.debug('scenario_name=' + config.SCENARIO_NAME)

    main(config, logger)
