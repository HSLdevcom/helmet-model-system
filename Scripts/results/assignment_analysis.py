from assignment.emme_assignment import EmmeAssignmentModel
import parameters as param
import numpy

def end_assignment(emme_project, resultmatrices, first_scenario_id):
    """
    Assing volumes for last iteration round.
    """        
    ass_classes = resultmatrices.list_matrices("demand", "aht")
    # ask where to save matrices
    while True:
        try:
            no_matrices = len(ass_model.emme_scenarios.keys()) * len(ass_classes)
            print "Initialize {} matrices to emmebank.".format(no_matrices)
            mtx_id = int(input("Matrix ids to hold demand matrices:"))
            break
        except ValueError:
            print("Value should be a whole number.") 
    # assignment itself
    ass_model = EmmeAssignmentModel(emme_project, first_scenario_id=first_scenario_id)
    ass_model.prepare_network()
    for tp in ass_model.emme_scenarios:
        emme_project.logger.info("Assigning transit and car for period {}".format(tp))
        emme_mtx = {}
        for ass_class in param.emme_demand_mtx:
            emme_mtx[ass_class] = {
                "id": "mf{}".format(str(mtx_id)), 
                "description": "{}_demand_{}".format(ass_class, tp)}
            mtx_id = mtx_id + 1
        with resultmatrices.open("demand", tp) as mtx:
            demand = {ass_class: mtx[ass_class] for ass_class in ass_classes}
        ass_model.assign(tp, demand, is_last_iteration=True, is_first_iteration=False, demand_mtx=emme_mtx)

def import_count_data(emme_project, scen_id, count_datapath, attr):
    emmebank = emme_project.modeller.emmebank
    scenario = emmebank.scenario(scen_id)
    emme_project.create_extra_attribute(
        extra_attribute_type="LINK",
        extra_attribute_name="@{}".format(attr),
        extra_attribute_description="observed counts",
        overwrite=True,
        scenario = scenario
        )
    emme_project.create_extra_attribute(
        extra_attribute_type="LINK",
        extra_attribute_name="@count_type",
        extra_attribute_description="observed counts types",
        overwrite=True,
        scenario = scenario
        )
    emme_project.create_extra_attribute(
        extra_attribute_type="LINK",
        extra_attribute_name="@count_dir",
        extra_attribute_description="observed counts direction",
        overwrite=True,
        scenario = scenario
        )
    emme_project.import_attr(
        count_datapath,
        scenario = scenario,
        field_separator=",",
        column_labels={0:"inode", 1:"jnode", 2:"@count_type", 3:"@count_dir", 4:"@{}".format(attr)},
        revert_on_error=False
        )


