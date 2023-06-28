from argparse import ArgumentParser, ArgumentTypeError
import sys
import os
from glob import glob

import utils.config
import utils.log as log
from assignment.emme_assignment import EmmeAssignmentModel
from assignment.mock_assignment import MockAssignmentModel
from modelsystem import ModelSystem, AgentModelSystem
from datahandling.matrixdata import MatrixData


def main(args):
    if args.end_assignment_only:
        iterations = 0
    elif args.iterations > 0:
        iterations = args.iterations
    else:
        raise ArgumentTypeError(
            "Iteration number {} not valid".format(args.iterations))
    base_zonedata_path = os.path.join(args.baseline_data_path, "2018_zonedata")
    base_matrices_path = os.path.join(args.baseline_data_path, "base_matrices")
    forecast_zonedata_path = args.forecast_data_path
    results_path = args.results_path
    emme_project_path = args.emme_path
    log_extra = {
        "status": {
            "name": args.scenario_name,
            "state": "starting",
            "current": 0,
            "completed": 0,
            "failed": 0,
            "total": iterations,
            "log": log.filename,
            "converged": 0,
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
            separate_emme_scenarios=args.separate_emme_scenarios,
            save_matrices=args.save_matrices,
            first_matrix_id=args.first_matrix_id)
    # Initialize model system (wrapping Assignment-model,
    # and providing demand calculations as Python modules)
    # Read input matrices (.omx) and zonedata (.csv)
    log.info("Initializing matrices and models...", extra=log_extra)
    if args.is_agent_model:
        model = AgentModelSystem(
            forecast_zonedata_path, base_zonedata_path, base_matrices_path,
            results_path, ass_model, args.scenario_name)
    else:
        model = ModelSystem(
            forecast_zonedata_path, base_zonedata_path, base_matrices_path,
            results_path, ass_model, args.scenario_name)
    log_extra["status"]["results"] = model.mode_share

    # Run traffic assignment simulation for N iterations,
    # on last iteration model-system will save the results
    log_extra["status"]["state"] = "preparing"
    log.info(
        "Starting simulation with {} iterations...".format(iterations),
        extra=log_extra)
    impedance = model.assign_base_demand(
        args.use_fixed_transit_cost, iterations==0)
    log_extra["status"]["state"] = "running"
    i = 1
    while i <= iterations:
        log_extra["status"]["current"] = i
        try:
            log.info("Starting iteration {}".format(i), extra=log_extra)
            convergence_args={"REL_GAP":args.rel_gap,"MAX_GAP":args.max_gap}
            impedance = (model.run_iteration(impedance, "last", convergence_args)
                         if i == iterations
                         else model.run_iteration(impedance, i, convergence_args))
            log_extra["status"]["completed"] += 1
        except Exception as error:
            log_extra["status"]["failed"] += 1
            log.error("Exception at iteration {}".format(i), error)
            log.error(
                "Fatal error occured, simulation aborted.", extra=log_extra)
            break
        gap = model.convergence.iloc[-1, :] # Last iteration convergence
        if i == iterations:
            log_extra["status"]['state'] = 'finished'
        elif gap["max_gap"] < args.max_gap or gap["rel_gap"] < args.rel_gap:
            iterations = i + 1
        #This is here separately because the model can converge in the last iteration as well
        if gap["max_gap"] < args.max_gap or gap["rel_gap"] < args.rel_gap: 
            log_extra["status"]["converged"] = 1
        i += 1
    
    if not log_extra["status"]["converged"]: log.warn("Model has not converged")

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


if __name__ == "__main__":
    # Initially read defaults from config file ("dev-config.json")
    # but allow override via command-line arguments
    config = utils.config.read_from_file()
    parser = ArgumentParser(epilog="HELMET model system entry point script.")
    parser.add_argument(
        "--version",
        action="version",
        version="helmet " + str(config.VERSION))
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
    # HELMET scenario metadata
    parser.add_argument(
        "-o", "--end-assignment-only",
        action="store_true",
        default=config.END_ASSIGNMENT_ONLY,
        help="Using this flag runs only end assignment of base demand matrices.",
    )
    parser.add_argument(
        "-a", "--run-agent-simulation",
        dest="is_agent_model",
        action="store_true",
        default=config.RUN_AGENT_SIMULATION,
        help="Using this flag runs agent simulations instead of aggregate model.",
    )
    parser.add_argument(
        "-m", "--do-not-use-emme",
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
        "-e", "--save-emme-matrices",
        dest="save_matrices",
        action="store_true",
        default=config.SAVE_MATRICES_IN_EMME,
        help="Using this flag saves matrices for all time periods to Emme-project Database folder.",
    )
    parser.add_argument(
        "-d", "--del-strat-files",
        action="store_true",
        default=config.DELETE_STRATEGY_FILES,
        help="Using this flag deletes strategy files from Emme-project Database folder.",
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
    # HELMET scenario input data
    parser.add_argument(
        "--emme-path",
        type=str,
        default=config.EMME_PROJECT_PATH,
        help="Filepath to .emp EMME-project-file"),
    parser.add_argument(
        "--first-scenario-id",
        type=int,
        default=config.FIRST_SCENARIO_ID,
        help="First (biking) scenario ID within EMME project (.emp)."),
    parser.add_argument(
        "--first-matrix-id",
        type=int,
        default=config.FIRST_MATRIX_ID,
        help="First matrix ID within EMME project (.emp). Used only if --save-emme-matrices."),
    parser.add_argument(
        "--baseline-data-path",
        type=str,
        default=config.BASELINE_DATA_PATH,
        help="Path to folder containing both baseline zonedata and -matrices (Given privately by project manager)"),
    parser.add_argument(
        "--forecast-data-path",
        type=str,
        default=config.FORECAST_DATA_PATH,
        help="Path to folder containing forecast zonedata"),
    parser.add_argument(
        "--iterations",
        type=int,
        default=config.ITERATION_COUNT,
        help="Maximum number of demand model iterations to run (each using re-calculated impedance from traffic and transit assignment)."),
    parser.add_argument(
        "--max-gap",
        type=float,
        default=config.MAX_GAP,
        help="Car work matrix maximum change between iterations"),
    parser.add_argument(
        "--rel-gap",
        type=float,
        default=config.REL_GAP,
        help="Car work matrix relative change between iterations"),
    parser.add_argument(
        "-t", "--use-fixed-transit-cost",
        action="store_true",
        default=config.USE_FIXED_TRANSIT_COST,
        help="Using this flag activates use of pre-calculated (fixed) transit costs."),
    args = parser.parse_args()

    log.initialize(args)
    log.debug("helmet_version=" + str(config.VERSION))
    log.debug('sys.version_info=' + str(sys.version_info[0]))
    log.debug('sys.path=' + str(sys.path))
    args_dict = vars(args)
    for key in args_dict:
        log.debug("{}={}".format(key, args_dict[key]))

    if sys.version_info.major == 3:
        main(args)
    else:
        log.error("Python version not supported, must use version 3")
