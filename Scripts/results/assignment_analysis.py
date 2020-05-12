import parameters as param
import numpy

def assign_auto_transit(emme_project, resultmatrices, emme_scenarios, bike_scenario):
    """
    Assing volumes for last iteration round.
    """        
    # ask for emme mtx ids to hold demand
    ass_classes = resultmatrices.list_matrices("demand", "aht")
    while True:
        try:
            no_matrices = len(emme_scenarios.keys()) * len(ass_classes)
            print "Initialize {} matrices to emmebank.".format(no_matrices)
            mtx_id = int(input("Matrix ids to hold demand matrices:"))
            break
        except ValueError:
            print("Value should be a whole number.") 
    for tp in emme_scenarios:
        emme_mtx = {}
        for ass_class in param.emme_demand_mtx:
            emme_mtx[ass_class] = {
                "id": "mf{}".format(str(mtx_id)), 
                "description": "{}_demand_{}".format(ass_class, tp)}
            mtx_id = mtx_id + 1
        for ass_class in emme_mtx:
            emme_project.create_matrix(
                matrix_id=emme_mtx[ass_class]["id"],
                matrix_name="demand_"+ass_class,
                matrix_description=emme_mtx[ass_class]["description"],
                default_value=0,
                overwrite=True)
            emme_project.logger.info("Created matrix {}".format(emme_mtx[ass_class]["id"]))
        emme_project.logger.info("Assigning transit and car for period {}".format(tp))
        with resultmatrices.open("demand", tp) as mtx:
            demand = {ass_class: mtx[ass_class] for ass_class in ass_classes}
        emmebank = emme_project.modeller.emmebank
        tmp_mtx = {
            "transit": 0,
            "bike": 0,
        }
        for mtx in demand:
            mtx_label = mtx.split('_')[0]
            if mtx_label in tmp_mtx:
                idx = emme_mtx[mtx_label]["id"]
                tmp_mtx[mtx_label] += demand[mtx]
                if numpy.isnan(tmp_mtx[mtx_label]).any():
                    msg = "NAs in Numpy-demand matrix. Would cause infinite loop in Emme-assignment."
                    emme_project.logger.error(msg)
                    raise ValueError(msg)
                else:
                    emmebank.matrix(idx).set_numpy_data(tmp_mtx[mtx_label])
            else:
                idx = emme_mtx[mtx]["id"]
                if numpy.isnan(demand[mtx]).any():
                    msg = "NAs in Numpy-demand matrix. Would cause infinite loop in Emme-assignment."
                    emme_project.logger.error(msg)
                    raise ValueError(msg)
                else:
                    emmebank.matrix(idx).set_numpy_data(demand[mtx])
        emme_scenarios[tp].demand_mtx = emme_mtx
        emme_scenarios[tp].create_attributes(param.emme_attributes)
        emme_scenarios[tp]._calc_road_cost()
        emme_scenarios[tp]._calc_boarding_penalties()
        emme_scenarios[tp]._calc_background_traffic()
        emme_scenarios[tp]._specify()
        emme_scenarios[tp]._assign_cars(param.stopping_criteria_fine)
        emme_scenarios[tp]._calc_extra_wait_time()
        emme_scenarios[tp]._assign_congested_transit()
        bike_scenario.demand_mtx = emme_mtx
        bike_scenario._specify()
        bike_scenario._assign_bikes("all", "@bike_"+tp)    

def auto_link_24h(emme_scenarios, emme_result_scenario, attr):
    """ 
    Sums and expands link volumes from different scenarios
    to one result scenario.
    """
    extra_attr = param.link_volumes[attr]
    # get attr from different time periods to dictionary
    links_attr = {}
    for tp in emme_scenarios:
        tp_attr = {}
        scenario = emme_scenarios[tp]
        network = scenario.get_network()
        for link in network.links():
            tp_attr[link.id] = link[extra_attr]
        links_attr[tp] = tp_attr
    # get result network
    scenario = emme_result_scenario
    # create attr to save volume
    extra_attr_day = str(param.link_volumes[attr])
    network = scenario.get_network()
    # save link volumes to result network
    for link in network.links():
        day_add_attr = 0
        for tp in emme_scenarios:
             if link.id in links_attr[tp]:
                expansion_factor = param.volume_factors[attr][tp]
                add_attr = links_attr[tp][link.id]
                day_add_attr += add_attr * expansion_factor
        link[extra_attr_day] = day_add_attr
    scenario.set_network(network)

def transit_link_24h(emme_scenarios, emme_result_scenario):
    """ 
    Sums and expands segment volumes to links from different scenario.
    """
    attr = "transit"
    extra_attr = "@transit_link"
    # get attr from different time periods to dictionary
    links_attr = {}
    for tp in emme_scenarios:
        tp_attr = {}
        scenario = emme_scenarios[tp]
        network = scenario.get_network()
        for link in network.links():
            voltr_segment = 0
            for segment in link.segments():
                voltr_segment += segment.transit_volume
            link[extra_attr] = voltr_segment
            tp_attr[link.id] = voltr_segment
        links_attr[tp] = tp_attr
        scenario.set_network(network)
    # save link volumes to result network
    network = emme_result_scenario.get_network()
    for link in network.links():
        day_add_attr = 0
        for tp in emme_scenarios:
             if link.id in links_attr[tp]:
                expansion_factor = param.volume_factors[attr][tp]
                add_attr = links_attr[tp][link.id]
                day_add_attr += add_attr * expansion_factor
        link[extra_attr] = day_add_attr
    emme_result_scenario.set_network(network)

def transit_node_24h(emme_scenarios, emme_result_scenario):
    """ 
    Sums and expands node volumes to links from different scenario.
    """
    attr = "transit"
    extra_attr = "@transit_node"
    # get attr from different time periods to dictionary
    nodes_attr = {}
    for tp in emme_scenarios:
        tp_attr = {}
        scenario = emme_scenarios[tp]
        network = scenario.get_network()
        for node in network.nodes():
            board_segment = 0
            for segment in node.outgoing_segments():
                board_segment += segment.transit_boardings
            node[extra_attr] = board_segment
            tp_attr[node.id] = board_segment
        nodes_attr[tp] = tp_attr
        scenario.set_network(network)
    # save link volumes to result network
    network = emme_result_scenario.get_network()
    for node in network.nodes():
        day_add_attr = 0
        for tp in emme_scenarios:
             if node.id in nodes_attr[tp]:
                expansion_factor = param.volume_factors[attr][tp]
                add_attr = nodes_attr[tp][node.id]
                day_add_attr += add_attr * expansion_factor
        node[extra_attr] = day_add_attr
    emme_result_scenario.set_network(network)

def transit_segment_24h(emme_scenarios, emme_result_scenario):
    """ 
    Sums and expands node volumes to links from different scenario.
    """
    attr = "transit"
    extra_attr = "@transit_segment"
    # get attr from different time periods to dictionary
    segments_attr = {}
    for tp in emme_scenarios:
        tp_attr = {}
        scenario = emme_scenarios[tp]
        network = scenario.get_network()
        for segment in network.transit_segments():
            tp_attr[segment.id] = segment.transit_boardings
        segments_attr[tp] = tp_attr
    # save link volumes to result network
    network = emme_result_scenario.get_network()
    for segment in network.transit_segments():
        day_add_attr = 0
        for tp in emme_scenarios:
             if segment.id in segments_attr[tp]:
                expansion_factor = param.volume_factors[attr][tp]
                add_attr = segments_attr[tp][segment.id]
                day_add_attr += add_attr * expansion_factor
        segment[extra_attr] = day_add_attr
    emme_result_scenario.set_network(network)

def bike_link_24h(bike_scenario):
    """ 
    Sums and expands link volumes from different scenarios
    to one result scenario.
    """
    attr = "bike"
    # get attr from different time periods to dictionary
    links_attr = {}
    for tp in param.emme_scenario:
        extra_attr = "@{}_{}".format(attr, tp)
        tp_attr = {}
        network = bike_scenario.get_network()
        for link in network.links():
            tp_attr[link.id] = link[extra_attr]
        links_attr[tp] = tp_attr
    # save link volumes to result network
    for link in network.links():
        day_add_attr = 0
        for tp in param.emme_scenario:
             if link.id in links_attr[tp]:
                expansion_factor = param.volume_factors[attr][tp]
                add_attr = links_attr[tp][link.id]
                day_add_attr += add_attr * expansion_factor
        extra_attr = "@{}_{}".format(attr, "day")
        link[extra_attr] = day_add_attr
    bike_scenario.set_network(network)


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
        revert_on_error=True
        )


