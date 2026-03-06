from argparse import ArgumentParser
from pathlib import Path

import utils.config
import utils.log as log
from assignment.emme_bindings.emme_project import EmmeProject
import inro.emme.desktop.app as _app
import inro.emme.database.emmebank as _eb
from inro.emme.desktop.types import Box
from inro.emme.desktop.view import ViewItem
import parameters.assignment as param
import os

#Example usage from cmd:
#"C:\Program Files\Bentley\OpenPaths\EMME 25.00.00\Python311\python" create_emme_project.py --log-format=TEXT --project-name="Automation test" --emme-path="C:\Users\HajduPe\Emme_Helmet5\Projektit\automated_tests"

def create_emme_project(args):
    project_dir = args.emme_path
    project_name = args.project_name
    try:
        project_path = _app.create_project(project_dir, project_name)
    except FileExistsError:
            project_path = Path(project_dir, project_name, project_name + ".emp")
    default_dimensions = {
        "scalar_matrices": 9999,
        "origin_matrices": 10,
        "destination_matrices": 10,
        "full_matrices": 100,
        "scenarios": args.number_of_emme_scenarios,
        "turn_entries": 10000,
        "transit_vehicles": 30,
        "functions": 99,
        "operators": 5000,
        "sola_analyses": 240,
    }
    submodel_dimensions = {
        "helmet": {
            "centroids": 2350,
            "regular_nodes": 20000,
            "links": 55000,
            "transit_lines": 2000,
            "transit_segments": 200000,
        },
    }

    # calculate extra attribute dimensions:
    dim = submodel_dimensions["helmet"]
    dim["extra_attribute_values"] = 9900000

    dim.update(default_dimensions)
    scenario_num = args.first_scenario_id
    db_dir = Path(project_dir, project_name, "Database")
    db_dir.mkdir(parents=True, exist_ok=True)
    eb = _eb.create(db_dir / "emmebank", dim)
    eb.text_encoding = 'utf-8'
    eb.title = "Database"
    eb.coord_unit_length = 0.001
    eb.create_scenario(scenario_num)
    #emmebank_path = eb.path
    eb.dispose()
    ed = _app.start_dedicated(project=project_path, visible=False, user_initials="HSL")
    ed.project.name = "HELMET_example_project"
    #db = ed.data_explorer().add_database(emmebank_path)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    ed.project.spatial_reference_file = os.path.join(dir_path,"project_data", "Helmet_proj.prj").replace("\\", "/")

    #Set initial view
    box= Box(25487600,
             6664330,
             25508900,
             6680290)
    ed.project.initial_view = box

    ed.project.save()

    #Adjust user data in manual, no API seems to be available for that
    # Read in the file
    user_data_path = os.path.join(project_dir, project_name, "Worksheets","general.emu").replace("\\", "/")
    with open(user_data_path, 'r') as file:
        filedata = file.read()
    # Replace the target string
    filedata = filedata.replace('IncludeBack = ', 'IncludeBack = %<$EmmePath>%/common/default_web_basemap.eml')
    # Write the file out again
    with open(user_data_path, 'w') as file:
        file.write(filedata)

if __name__ == "__main__":
    # Initially read defaults from config file ("dev-config.json")
    # but allow override via command-line arguments
    config = utils.config.read_from_file()
    parser = ArgumentParser(epilog="HELMET model system entry point script.")
    # Logging
    parser.add_argument(
        "--log-level",
        choices={"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"},
    )
    parser.add_argument(
        "--log-format",
        choices={"TEXT", "JSON"},
    )
    parser.add_argument(
        "--project-name",
        type=str,
        help="Name of HELMET project. Influences name of database directory"),
    parser.add_argument(
        "--submodel",
        type=str,
        help="Name of submodel, used for choosing appropriate database dimensions"),
    parser.add_argument(
        "--emme-path",
        type=str,
        help="Filepath to folder where EMME project will be created"),
    parser.add_argument(
        "--number-of-emme-scenarios",
        type=int,
        help="Number of scenarios in the emmebank"),
    parser.add_argument(
        "-s", "--separate-emme-scenarios",
        action="store_true",
        help="Using this flag enables saving network time-period specific results in separate EMME scenarios."),
    parser.add_argument(
        "--first-scenario-id",
        type=int,
        help="First EMME project scenario ID"),
    parser.set_defaults(
        **{key.lower(): val for key, val in config.__dict__.items()})
    args = parser.parse_args()
    log.initialize(args)
    #log.debug(utils.config.dump(vars(args)))

    create_emme_project(args)
