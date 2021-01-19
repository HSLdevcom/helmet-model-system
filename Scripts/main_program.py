from IPython.display import display
import os
import math as _math
import inro.modeller as _m

import batin_python.bike_functions as _modbike
import batin_python.bus_stops as _modbus
import batin_python.function_parameters as _modfun
import batin_python.check_network as _netche
from batin_python.batin_methods import BatinMethods as _batmet

def main_program(self, scen_id, folder, version):
    
    ebank = _m.Modeller().emmebank
    desktop = _m.Modeller().desktop
    data_explorer = desktop.data_explorer()
    
    scen_list = [19, 20, 21, 22, 23]

    # bike network
    
    scen_id = scen_list[0]
    try:
        scen_xx = ebank.scenario(scen_id)
        data_explorer.replace_primary_scenario(scen_xx)
    except Exception, error:
        display('Could not change ', scen_id, ' to primary scenario')

    _batmet.initiallze_network(self, scen_id, bike=True)
    _batmet.read_network(self, scen_id, folder, version, bike=True)
    _modbike.bike_functions(self, scen_id)
    _netche.check_network(self, scen_id, bike=True)   # method still missing
    
    # road and rail networks
    
    scen_id = scen_list[2]
    _batmet.initiallze_network(self, scen_id, bike=False)
    _batmet.read_network(self, scen_id, folder, version, bike=False)
    _modbus.bus_stops(self, scen_id)
    
    _batmet.delete_scenario(self, scen_list[3], scen_list[2])
    _batmet.copy_scenario(self, scen_list[2], scen_list[3])
    _batmet.delete_scenario(self, scen_list[4], scen_list[2])
    _batmet.copy_scenario(self, scen_list[2], scen_list[4])
    
    period_list = ['aht', 'pt', 'iht']
    attr_list_line = ['@hwaht', '@hwpt' , '@hwiht']
    attr_list_link = ['@hinah', '@hinpt', '@hinih']
        
    for k in range(3):
        _modfun.function_parameters(self, scen_list[k+2], period_list[k])
        _batmet.copy_attribute(self, scen_list[k+2], 'line', attr_list_line[k], 'hdwy')
        _batmet.copy_attribute(self, scen_list[k+2], 'link', attr_list_link[k], '@hinta')

    _batmet.delete_scenario(self, scen_list[1], scen_list[3])
    _batmet.copy_scenario(self, scen_list[3], scen_list[1])
    _netche.check_network(self, scen_list[1], bike=False)   # method still missing
   