from argparse import ArgumentParser
import sys
import os
from glob import glob

from utils.config import Config
import utils.log as log
from assignment.emme_assignment import EmmeAssignmentModel
from assignment.mock_assignment import MockAssignmentModel
from modelsystem import ModelSystem, AgentModelSystem
from datahandling.matrixdata import MatrixData
from datahandling.resultdata import ResultsData


def main(args):
    name = (args.scenario_name if args.scenario_name is not None
        else Config.DefaultScenario)
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
            "log": log.filename,
        }
    }
    # Check input data folders/files exist
    if not os.path.exists(base_zonedata_path):
        raise NameError(
            "Baseline zonedata directory '{}' does not exist.".format(
                base_zonedata_path))
    if not os.path.exists(base_matrices_path):
        raise NameError(
            "Baseline zonedata directory '{}' does not exist.".format(
                base_matrices_path))
    if not os.path.exists(forecast_zonedata_path):
        raise NameError(
            "Forecast data directory '{}' does not exist.".format(
                forecast_zonedata_path))
    # Choose and initialize the Traffic Assignment (supply)model
    if args.do_not_use_emme:
        log.info("Initializing MockAssignmentModel...")
        mock_result_path = os.path.join(
            results_path, args.scenario_name, "Matrices")
        if not os.path.exists(mock_result_path):
            raise NameError(
                "Mock Results directory {} does not exist.".format(
                    mock_result_path))
        ass_model = MockAssignmentModel(MatrixData(mock_result_path))
    else:
        if not os.path.isfile(emme_project_path):
            raise NameError(
                ".emp project file not found in given '{}' location.".format(
                    emme_project_path))
        log.info("Initializing Emme...")
        from assignment.emme_bindings.emme_project import EmmeProject
        ass_model = EmmeAssignmentModel(
            EmmeProject(emme_project_path),
            first_scenario_id=args.first_scenario_id,
            save_matrices=args.save_matrices,
            first_matrix_id=args.first_matrix_id)
    # Initialize model system (wrapping Assignment-model,
    # and providing demand calculations as Python modules)
    # Read input matrices (.omx) and zonedata (.csv)
    log.info("Initializing matrices and models...", extra=log_extra)
    if args.is_agent_model:
        model = AgentModelSystem(
            forecast_zonedata_path, base_zonedata_path, base_matrices_path,
            results_path, ass_model, name)
    else:
        model = ModelSystem(
            forecast_zonedata_path, base_zonedata_path, base_matrices_path,
            results_path, ass_model, name)

    # Regular model run
    run(log_extra, model)

    # Run with increased car ownership
    new_name = name + "_car++"
    model.resultdata = ResultsData(os.path.join(results_path, new_name))
    model.resultmatrices = MatrixData(
            os.path.join(results_path, new_name, "Matrices"))
    model.cdm.set_car_growth(constant=+0.1)
    run(log_extra, model)

    # Run with decreased car ownership
    new_name = name + "_car--"
    model.resultdata = ResultsData(os.path.join(results_path, new_name))
    model.resultmatrices = MatrixData(
            os.path.join(results_path, new_name, "Matrices"))
    model.cdm.set_car_growth(factor=0.8)
    run(log_extra, model)

    # delete emme strategy files for scenarios
    if args.del_strat_files:
        dbase_path = os.path.join(os.path.dirname(emme_project_path), "database")
        filepath = os.path.join(dbase_path, "STRAT_s{}*")
        dirpath = os.path.join(dbase_path, "STRATS_s{}", "*")
        scenario_ids = range(args.first_scenario_id, args.first_scenario_id+5)
        for s in scenario_ids:
            strategy_files = glob(filepath.format(s)) + glob(dirpath.format(s))
            for f in strategy_files:
                try:
                    os.remove(f)
                except:
                    log.info("Not able to remove file {}.".format(f))
        log.info("Removed strategy files in {}".format(dbase_path))
    log.info("Simulation ended.", extra=log_extra)

def run(log_extra, model):
    iterations = log_extra["status"]["total"]
    # Run traffic assignment simulation for N iterations,
    # on last iteration model-system will save the results
    log_extra["status"]["state"] = "preparing"
    log.info(
        "Starting simulation with {} iterations...".format(iterations),
        extra=log_extra)
    impedance = model.assign_base_demand(
        args.use_fixed_transit_cost, iterations==0)
    log_extra["status"]["state"] = "running"
    for i in range(1, iterations + 1):
        log_extra["status"]["current"] = i
        try:
            log.info("Starting iteration {}".format(i), extra=log_extra)
            impedance = (model.run_iteration(impedance, "last")
                         if i == iterations
                         else model.run_iteration(impedance, i))
            log_extra["status"]["completed"] += 1
        except Exception as error:
            log_extra["status"]["failed"] += 1
            log.error("Exception at iteration {}".format(i), error)
            log.error(
                "Fatal error occured, simulation aborted.", extra=log_extra)
            break
        log_extra["status"]["results"] = model.mode_share
        if i == iterations:
            log_extra["status"]['state'] = 'finished'


if __name__ == "__main__":
    # Initially read defaults from config file ("dev-config.json")
    # but allow override via command-line arguments
    config = Config().read_from_file()
    parser = ArgumentParser(epilog="HELMET model system entry point script.")
    parser.add_argument(
        "--version",
        action="version",
        version="helmet " + str(config.HELMET_VERSION))
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
        "--run-agent-simulation",
        dest="is_agent_model",
        action="store_true",
        default=config.RUN_AGENT_SIMULATION,
        help="Using this flag runs agent simulations instead of aggregate model.",
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
        "--del-strat-files",
        dest="del_strat_files",
        action="store_true",
        default=config.DELETE_STRATEGY_FILES,
        help="Using this flag deletes strategy files from Emme-project Database folder.",
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
        "--first-matrix-id",
        dest="first_matrix_id",
        type=int,
        default=config.FIRST_MATRIX_ID,
        help="First matrix ID within EMME project (.emp). Used only if --save-emme-matrices."),
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
        help="Number of demand model iterations to run (each using re-calculated impedance from traffic and transit assignment)."),
    parser.add_argument(
        "--use-fixed-transit-cost",
        dest="use_fixed_transit_cost",
        action="store_true",
        default=config.USE_FIXED_TRANSIT_COST,
        help="Using this flag activates use of pre-calculated (fixed) transit costs."),
    args = parser.parse_args()

    config.LOG_LEVEL = args.log_level
    config.LOG_FORMAT = args.log_format
    config.SCENARIO_NAME = args.scenario_name
    config.RESULTS_PATH = args.results_path
    log.initialize(config)
    log.debug("helmet_version=" + str(config.HELMET_VERSION))
    log.debug('sys.version_info=' + str(sys.version_info[0]))
    log.debug('sys.path=' + str(sys.path))
    log.debug('log_level=' + args.log_level)
    log.debug('emme_path=' + args.emme_path)
    log.debug('baseline_data_path=' + args.baseline_data_path)
    log.debug('forecast_data_path=' + args.forecast_data_path)
    log.debug('iterations=' + str(args.iterations))
    log.debug('use_fixed_transit_cost=' + str(args.use_fixed_transit_cost))
    log.debug('save_matrices=' + str(args.save_matrices))
    log.debug('del_strat_files=' + str(args.del_strat_files))
    log.debug('first_scenario_id=' + str(args.first_scenario_id))
    log.debug('scenario_name=' + args.scenario_name)

    main(args)
