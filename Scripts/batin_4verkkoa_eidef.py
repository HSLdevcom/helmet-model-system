bike = False

import os
from IPython.display import display
_m    = inro.modeller
_moMo = inro.modeller.Modeller()
ebank = _m.Modeller().emmebank
desktop = _m.Modeller().desktop
data_explorer = desktop.data_explorer()

scen_24 = ebank.scenario(24)
data_explorer.replace_primary_scenario(scen_24)

# poistetaan vanhat linjat, kaantymiset, linkit ja solmut

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
# *** does not work: 'all' and '*' are not possible
# veh_to_delete = _m.Modeller().scenario.transit_vehicle("*")
# delete_vehicle(vehicle = veh_to_delete)

NAME_DEL_MODES = "inro.emme.data.network.mode.delete_mode"
delete_mode = _m.Modeller().tool(NAME_DEL_MODES)
# *** does not work: 'all' and '*' are not possible
# mode_to_delete = _m.Modeller().scenario.mode("*")
# delete_mode(mode=mode_to_delete)

# luetaan uusi verkko, linjasto ja kaantymiset

folder  = '\sijopankki2018\\'
version = '2018_20191014'
init_modes = 'd201_modes_init.in'
init_veh   = 'd202_veh_init.in'

file_modeA = 'd201_modes_M2016.in'
file_modeB = 'd201_modes_M2016_pyora.in'
file_veh   = 'd202_veh_M2016.in'
file_base  = folder + 'd211_verkko_' + version + '.in'
file_turns = folder + 'd231_verkko_' + version + '.in'
file_lines = folder + 'd221_linjat_' + version + '.in'
file_toll  = folder + 'd241_hinta_'  + version + '.in'
file_hdwy  = folder + 'd241_vuorovalit_' + version + '.in'
file_bike  = folder + 'd241_pyoratieluokka_' + version + '.in'

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

display('network in scenario ' + str(scen_24.id) + ' "' + str(scen_24.title) + '" initiallzed')
scen_24.title = "new version of " + str(scen_24.id)

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
    import_values(file_path = bikeway_path,
              scenario = _m.Modeller().scenario,
              field_separator=" ",
              column_labels={0: "inode", 
                             1: "jnode", 
                             2: "@pyoratieluokka"},
              revert_on_error=True)
else:
    headway_path = (default_path + file_hdwy).replace("\\","/")
    display(headway_path)
    import_values(file_path = headway_path,
              scenario = _m.Modeller().scenario,
              field_separator=" ",
              column_labels={0: "line", 
                             1: "@hwaht", 
                             2: "@hwpt",
                             3: "@hwiht"},
              revert_on_error=False)
    roadprice_path = (default_path + file_toll).replace("\\","/")
    display(roadprice_path)
    import_values(file_path = roadprice_path,
              scenario = _m.Modeller().scenario,
              field_separator=" ",
              column_labels={0: "inode", 
                             1: "jnode", 
                             2: "@hinah",
                             3: "@hinpt",
                             4: "@hinih"},
              revert_on_error=True)

display('network in scenario ' + str(scen_24.id) + ' "' + str(scen_24.title) + '" completed')
netw_24 = scen_24.get_network()
scen_24.publish_network(netw_24)
