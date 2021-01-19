# batin_methods.py

from IPython.display import display
import os
import math as _math
import inro.modeller as _m

import inro.emme.database.emmebank as _eb
emmebank = _eb.Emmebank('C:\Users\elolati\Timon_emme\HELMET_testi_31\sijoittelu\database\emmebank')

class BatinMethods(_m.Tool()):
    def __init__():
        pass
    
    def __call__():
        pass
    
    # ***************************
    # change prim_scen_id to primary scenario and delete scenario del_scen_id

    def delete_scenario(self, del_scen_id, prim_scen_id):
        ebank = _m.Modeller().emmebank
        desktop = _m.Modeller().desktop
        data_explorer = desktop.data_explorer()
        NAME_DEL_SCEN = "inro.emme.data.scenario.delete_scenario"
        delete_scenario = _m.Modeller().tool(NAME_DEL_SCEN)

        try:
            primary = ebank.scenario(prim_scen_id)
            data_explorer.replace_primary_scenario(primary)
        except Exception, error:
            display('Could not change ', prim_scen_id, ' to primary scenario')

        try:
            scen_xx = ebank.scenario(del_scen_id)
            delete_scenario(scenario=scen_xx)
        except Exception, error:
            display('Could not delete scenario ', del_scen_id)

    # ***************************
    # copy scenario scen1_id to scenario scen2_id

    def copy_scenario(self, scen1_id, scen2_id):
        ebank = _m.Modeller().emmebank
        NAME_COPY_SCEN = "inro.emme.data.scenario.copy_scenario"
        copy_scenario = _m.Modeller().tool(NAME_COPY_SCEN)

        try:
            scenario1 = ebank.scenario(scen1_id)
            scenario2 = copy_scenario(from_scenario=scenario1,
                scenario_id=scen2_id,
                scenario_title="copy of scenario " + str(scenario1.id),
                copy_strategies=True,
                copy_linkshapes=True,
                overwrite=False)
        except Exception, error:
            display('Could not copy scenario ', scen1_id, ' to scenario ', scen2_id)

    # ***************************
    # initiallze the lines, turns, links, nodes, vehicles and modes of the network
    
    def initiallze_network(self, scen_id, bike):
        ebank = _m.Modeller().emmebank
        desktop = _m.Modeller().desktop
        data_explorer = desktop.data_explorer()

        try:
            scen_xx = ebank.scenario(scen_id)
            data_explorer.replace_primary_scenario(scen_xx)
        except Exception, error:
            display('Could not change ', scen_id, ' to primary scenario')
        
        NAME_DEL_LINES = "inro.emme.data.network.transit.delete_transit_lines"
        delete_lines = _m.Modeller().tool(NAME_DEL_LINES)
        if bike:
            pass
        else:
            delete_lines(selection="all")
        
        NAME_DEL_TURNS = "inro.emme.data.network.turn.delete_turns"
        delete_turns = _m.Modeller().tool(NAME_DEL_TURNS)
        if bike:
            pass
        else:
            delete_turns(selection="all")
        
        NAME_DEL_LINKS = "inro.emme.data.network.base.delete_links"
        delete_links = _m.Modeller().tool(NAME_DEL_LINKS)
        delete_links(selection="all", condition="ignore")
        
        NAME_DEL_NODES = "inro.emme.data.network.base.delete_nodes"
        delete_nodes = _m.Modeller().tool(NAME_DEL_NODES)
        delete_nodes(selection="all", condition="ignore")
        
        NAME_DEL_VEH = "inro.emme.data.network.transit.delete_vehicle"
        delete_vehicle = _m.Modeller().tool(NAME_DEL_VEH)
        if bike:
            pass
        else:
            # *** DOES NOT WORK: 'all' and '*' are not possible
            # veh_to_delete = _m.Modeller().scenario.transit_vehicle("*")
            # delete_vehicle(vehicle = veh_to_delete)
            pass
        
        NAME_DEL_MODES = "inro.emme.data.network.mode.delete_mode"
        delete_mode = _m.Modeller().tool(NAME_DEL_MODES)
        # *** DOES NOT WORK: 'all' and '*' are not possible
        # mode_to_delete = _m.Modeller().scenario.mode("*")
        # delete_mode(mode=mode_to_delete)

        init_modes = 'd201_modes_init.in'
        init_veh   = 'd202_veh_init.in'
        
        default_path = os.path.dirname(_m.Modeller().emmebank.path).replace("\\","/")
        display(default_path)
        
        NAME_INPUT_MODES = "inro.emme.data.network.mode.mode_transaction"
        process_modes = _m.Modeller().tool(NAME_INPUT_MODES)
        
        NAME_INPUT_VEH = "inro.emme.data.network.transit.vehicle_transaction"
        process_vehicles = _m.Modeller().tool(NAME_INPUT_VEH)
        
        if bike:
            pass
        else:
            vehicle_path = os.path.join(default_path,init_veh).replace("\\","/")
            process_vehicles(transaction_file = vehicle_path,
                revert_on_error = True,
                scenario = _m.Modeller().scenario)

        modes_path = os.path.join(default_path,init_modes).replace("\\","/")
        process_modes(transaction_file = modes_path,
            revert_on_error = True,
            scenario = _m.Modeller().scenario)
   
        display('network in scenario ' + str(scen_xx.id) + ' "' + 
            str(scen_xx.title) + '" initiallzed')
   
    # ***************************
    # read the modes, vehicles, nodes, lines, turns and lines of the new network
    
    def read_network(self, scen_id, folder, version, bike):
        ebank = _m.Modeller().emmebank
        desktop = _m.Modeller().desktop
        data_explorer = desktop.data_explorer()
        
        try:
            scen_xx = ebank.scenario(scen_id)
            data_explorer.replace_primary_scenario(scen_xx)
        except Exception, error:
            display('Could not change ', scen_id, ' to primary scenario')
        
        #folder  = '\sijopankki2018\\'
        #version = '2018_20191014'
        
        file_modeA = 'd201_modes_M2016.in'
        file_modeB = 'd201_modes_M2016_pyora.in'
        file_veh   = 'd202_veh_M2016.in'
        file_base  = folder + 'd211_verkko_' + version + '.in'
        file_turns = folder + 'd231_verkko_' + version + '.in'
        file_lines = folder + 'd221_linjat_' + version + '.in'
        file_toll  = folder + 'd241_hinta_'  + version + '.in'
        file_hdwy  = folder + 'd241_vuorovalit_' + version + '.in'
        file_bike  = folder + 'd241_pyoratieluokka_' + version + '.in'
        # file_HSL   = folder + 'hsl_kunnat_'  + version + '.dat'
        
        scen_xx.title = "new version of " + str(scen_xx.id) + " " + version
        
        default_path = os.path.dirname(_m.Modeller().emmebank.path).replace("\\","/")
        display(default_path)
        
        NAME_INPUT_MODES = "inro.emme.data.network.mode.mode_transaction"
        process_modes = _m.Modeller().tool(NAME_INPUT_MODES)
        
        NAME_INPUT_VEH = "inro.emme.data.network.transit.vehicle_transaction"
        process_vehicles = _m.Modeller().tool(NAME_INPUT_VEH)
        
        if bike:
            modes_path = os.path.join(default_path,file_modeB).replace("\\","/")
        else:
            modes_path = os.path.join(default_path,file_modeA).replace("\\","/")
        display(modes_path)
        process_modes(transaction_file = modes_path,
            revert_on_error = True,
            scenario = _m.Modeller().scenario)

        if bike:
            pass
        else:
            vehicle_path = os.path.join(default_path,file_veh).replace("\\","/")
            display(vehicle_path)
            process_vehicles(transaction_file = vehicle_path,
                revert_on_error = True,
                scenario = _m.Modeller().scenario)

        NAME_INPUT_BASE = "inro.emme.data.network.base.base_network_transaction"
        process_base = _m.Modeller().tool(NAME_INPUT_BASE)
        basenet_path = (default_path + file_base).replace("\\","/")
        display(basenet_path)
        process_base(transaction_file = basenet_path,
            revert_on_error = True,
            scenario = _m.Modeller().scenario)

        NAME_INPUT_TURNS = "inro.emme.data.network.turn.turn_transaction"
        process_turns = _m.Modeller().tool(NAME_INPUT_TURNS)
        if bike:
            pass
        else:
            turn_path = (default_path + file_turns).replace("\\","/")
            display(turn_path)
            process_turns(transaction_file = turn_path,
                revert_on_error = True,
                scenario = _m.Modeller().scenario)

        NAME_INPUT_LINES = "inro.emme.data.network.transit.transit_line_transaction"
        process_lines = _m.Modeller().tool(NAME_INPUT_LINES)
        if bike:
            pass
        else:
            transit_line_path = (default_path + file_lines).replace("\\","/")
            display(transit_line_path)
            process_lines(transaction_file = transit_line_path,
                revert_on_error = True,
                scenario = _m.Modeller().scenario)

        NAME_EXTRA = "inro.emme.data.extra_attribute.import_extra_attributes"
        import_values = _m.Modeller().tool(NAME_EXTRA)
        
        if bike:
            bikeway_path = (default_path + file_bike).replace("\\","/")
            display(bikeway_path)
            try:
                import_values(file_path = bikeway_path,
                    scenario = _m.Modeller().scenario,
                    field_separator=" ",
                    column_labels={0: "inode", 
                                   1: "jnode", 
                                   2: "@pyoratieluokka"},
                    revert_on_error=True)
            except Exception, error:
                display('Could not import extra attribute @pyoratieluokka')
        else:
            headway_path = (default_path + file_hdwy).replace("\\","/")
            display(headway_path)
            try:
                import_values(file_path = headway_path,
                    scenario = _m.Modeller().scenario,
                    field_separator=" ",
                    column_labels={0: "line", 
                                   1: "@hwaht", 
                                   2: "@hwpt",
                                   3: "@hwiht"},
                   revert_on_error=False)
            except Exception, error:
                display('Could not import extra attributes @hwaht, @hwpt and @hwiht')
            
            roadprice_path = (default_path + file_toll).replace("\\","/")
            display(roadprice_path)
            try:
                import_values(file_path = roadprice_path,
                    scenario = _m.Modeller().scenario,
                    field_separator=" ",
                    column_labels={0: "inode", 
                                   1: "jnode", 
                                   2: "@hinah",
                                   3: "@hinpt",
                                   4: "@hinih"},
                    revert_on_error=True)
            except Exception, error:
                display('Could not import extra attributes @hinah, @hinpt and @hinih')    
            
        # *** tahan valiin aluekoodien luku tiedostosta hal_kunnat_xxx.dat listaan hsl_area ***

        hsl_area = 'ui3==49 .or. ui3==91,92 .or. ui3==235 .or. ui3==245' \
            '.or. ui3==257 .or. ui3==753 .or. ui3==755 .or. ui3==858'

        NAME_NETW_CALC = "inro.emme.network_calculation.network_calculator"
        network_calc = _m.Modeller().tool(NAME_NETW_CALC)

        if bike:
            pass
        else:
            network_calc['specification'] = {'aggregation' : None,
                'expression' : '0',
                'result' : '@hsl',
                'selections' : {'node' : 'all'},
                'type' : 'NETWORK_CALCULATION'}
            network_calc.run()

            network_calc['specification'] = {'aggregation' : None,
                'expression' : '1',
                'result' : '@hsl',
                'selections' : {'node' : hsl_area},
                'type' : 'NETWORK_CALCULATION'}
            network_calc.run()
	
        display('network in scenario ' + str(scen_xx.id) + ' "' + 
            str(scen_xx.title) + '" completed')
        netw_xx = scen_xx.get_network()
        scen_xx.publish_network(netw_xx)
        
    # ***************************
    # copy value of attribute attr_from to attribute attr_to
    # the type of both attributes is attr_type

    def copy_attribute(self, scen_id, attr_type, attr_from, attr_to):
        ebank = _m.Modeller().emmebank
        desktop = _m.Modeller().desktop
        data_explorer = desktop.data_explorer()

        try:
            scen_xx = ebank.scenario(scen_id)
            data_explorer.replace_primary_scenario(scen_xx)
        except Exception, error:
            display('Could not change ', scen_id, ' to primary scenario')
        
        NAME_NETW_CALC = "inro.emme.network_calculation.network_calculator"
        network_calc = _m.Modeller().tool(NAME_NETW_CALC)
        
        if   (attr_type == 'node'):
           select = "'node' : 'all'"
        elif (attr_type == 'link'):
           select = "'link' : 'all'"
        elif (attr_type == 'line'):
           select = "'line' : 'all'"
        elif (attr_type == 'segment'):
           select = "'line' : 'all', 'link' : 'all'"
        else:
           display('parameter', attr_type, 'not recognized')
        
        network_calc['specification'] = {'aggregation' : None,
            'expression' : attr_from,
            'result' : attr_to,
            'selections' : {select},
            'type' : 'NETWORK_CALCULATION'}
        network_calc.run()
