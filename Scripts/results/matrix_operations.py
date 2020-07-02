import parameters
import os
import numpy as np
import pandas as pd

def del_emmebank_matrices(emme_project, mtxtype, lower_limit, upper_limit):
    emmebank = emme_project.modeller.emmebank
    delmat_list = []
    for i in range(lower_limit, upper_limit):
        delmat_list.append(i)
    for i in delmat_list:
        matrix_temp = "%s%s" % (mtxtype, i)
        if matrix_temp in [m.id for m in emmebank.matrices()]:
            matrix_mf = emmebank.matrix(matrix_temp)
            emme_project.delete_matrix(matrix=matrix_mf)
    emme_project.logger.info("Deleted matrices type {} between {}-{}".format(mtxtype, lower_limit, upper_limit)) 

def mtx_to_24h(resultmatrices, zone_numbers, scenarios):
    mtxtype = raw_input('Choose matrix type (demand, transit, transfers):')
    ass_classes = resultmatrices.list_matrices(mtxtype, "aht")
    nr_zones = len(zone_numbers)
    # sum full day trips and aggregate
    # day matrix using parameters volume_factors
    assign_mtx_day = {}
    for ass_class in ass_classes:
        assign_mtx_day[ass_class] = np.zeros((nr_zones, nr_zones))
    if mtxtype == 'demand':
        for tp in scenarios:
            with resultmatrices.open(mtxtype, tp) as mtx:
                for ass_class in ass_classes:
                    coeff =  parameters.volume_factors[ass_class][tp]
                    assign_mtx_day[ass_class] += coeff * mtx[ass_class]
    elif mtxtype in ['transit', 'transfers']:
        for tp in scenarios:
            with resultmatrices.open(mtxtype, tp) as mtx:
                for ass_class in ass_classes:
                    coeff =  parameters.volume_factors['transit'][tp]
                    assign_mtx_day[ass_class] += coeff * mtx[ass_class]
    else: 
        pass
    with resultmatrices.open(mtxtype, "day", 'w') as mtx:
        mtx.mapping = zone_numbers
        for ass_class in ass_classes:
            mtx[ass_class] = assign_mtx_day[ass_class]

def get_emme_matrix(emme_project, emme_mtx_id):
    return emme_project.modeller.emmebank.matrix(emme_mtx_id).get_numpy_data()

def emme_matrices_to_omx(zone_numbers, resultmatrices, mtxtype, tp, mtxdict):
    with resultmatrices.open(mtxtype, tp, 'w') as mtx:
        mtx.mapping = zone_numbers
        for name in mtxdict:
            mtx[name] = mtxdict[name]['demand']

def transit_mode_matrices(emme_project, emme_scenarios, mtxdict):
    for name in mtxdict:
        tp = mtxdict[name]['scenario']
        emmebank = emme_project.modeller.emmebank
        scen = emmebank.scenario(emme_scenarios[tp])
        emme_project.create_extra_attribute(
            extra_attribute_type = "TRANSIT_LINE",
            extra_attribute_name = "@select",
            extra_attribute_description = "selected for path analysis",
            overwrite = True,
            scenario = scen)
        selector = "mode=" + mtxdict[name]['emme_mode']
        emme_project.network_calc({ 
            "type": "NETWORK_CALCULATION",
            "selections": {"transit_line": selector},
            "expression": "1",
            "result": "@select",
            "aggregation": None
            }, scenario=scen)
        idx = mtxdict[name]['id']
        emme_project.create_matrix(
            matrix_id=idx,
            matrix_name=name,
            matrix_description="select_demand_" + name,
            default_value=0,
            overwrite=True
            )
        transit_strategy_spec = {
            "type": "EXTENDED_TRANSIT_STRATEGY_ANALYSIS",
            "trip_components": {
                "boarding": "@select"
            },
            "sub_path_combination_operator": ".max.",
            "sub_strategy_combination_operator": ".max.",
            "selected_demand_and_transit_volumes": {
                "sub_strategies_to_retain": "FROM_COMBINATION_OPERATOR",
                "selection_threshold": {"lower": 1, "upper": 1}
            },
            "results": {"selected_demand": idx},
        }
        emme_project.strategy_analysis(transit_strategy_spec, scen, num_processors ="max")
        emme_project.logger.info("Selected {} demand from scenario {} to {}".format(name, emme_scenarios[tp], idx))

def transfer_matrices(emme_project, emme_scenarios, mtxdict):
    for name in mtxdict:
        tp = mtxdict[name]['scenario']
        emmebank = emme_project.modeller.emmebank
        scen = emmebank.scenario(emme_scenarios[tp])
        emme_project.create_extra_attribute(
            extra_attribute_type = "TRANSIT_SEGMENT",
            extra_attribute_name = "@select",
            extra_attribute_description = "selected for path analysis",
            overwrite = True,
            scenario = scen)
        emme_project.network_calc({ 
            "type": "NETWORK_CALCULATION",
            "selections": {
                "link": "all",
                "transit_line": "all"
                },
            "expression": "1",
            "result": "@select",
            "aggregation": None
            }, scenario=scen)
        idx = mtxdict[name]['id']
        emme_project.create_matrix(
            matrix_id=idx,
            matrix_name=name,
            matrix_description="select_demand_" + name,
            default_value=0,
            overwrite=True
            )
        transit_strategy_spec = {
            "type": "EXTENDED_TRANSIT_STRATEGY_ANALYSIS",
            "trip_components": {
                "boarding": "@select"
            },
            "sub_path_combination_operator": "+",
            "sub_strategy_combination_operator": ".max.",
            "selected_demand_and_transit_volumes": {
                "sub_strategies_to_retain": "FROM_COMBINATION_OPERATOR",
                "selection_threshold": {
                    "lower": mtxdict[name]['select_lower'], 
                    "upper": mtxdict[name]['select_upper']}
            },
            "results": {"selected_demand": idx},
        }
        emme_project.strategy_analysis(transit_strategy_spec, scen, num_processors ="max")
        emme_project.logger.info("Selected {} demand from scenario {} to {}".format(name, emme_scenarios[tp], idx))

def aggregate_matrix(aggregation_data, mtxs, result_path, zone_numbers, fname):
    # load aggregation shares and sum for new zones
    if aggregation_data is not None:
        aggregation_data = aggregation_data.reset_index()
        dest = zone_numbers
        orig = zone_numbers
        for mode_keys in mtxs.keys():
            mtx = pd.DataFrame(mtxs[mode_keys], orig, dest)
            mtx = mtx.reset_index().melt(id_vars = 'index')
            mtx.columns = ['orig', 'dest', 'value']
            aggregation_data.columns = ['index', 'orig', 'orig_agg', 'orig_share']
            mtx = mtx.merge(aggregation_data, on='orig', how='left')
            aggregation_data.columns = ['index', 'dest', 'dest_agg', 'dest_share']
            mtx = mtx.merge(aggregation_data, on='dest', how='left')
            mtx['value'] = mtx['value'] * mtx['orig_share'] * mtx['dest_share']
            mtx_agg = mtx.groupby(['orig_agg', 'dest_agg'])['value'].sum().reset_index()
            # save to file
            filename = "{}_{}.txt".format(fname, str(mode_keys))
            filepath = os.path.join(result_path, filename)
            mtx_agg.to_csv(filepath, sep='\t', float_format="%1.5f")
