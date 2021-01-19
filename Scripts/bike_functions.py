from IPython.display import display
import os
import math as _math
import inro.modeller as _m

def bike_functions(self, scen_id):
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
    
    network_calc['specification'] = {'aggregation' : None,
        'expression' : 70,
        'result' : 'vdf',
        'selections' : {'link' : '@pyoratieluokka==4'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()
    
    network_calc['specification'] = {'aggregation' : None,
        'expression' : 71,
        'result' : 'vdf',
        'selections' : {'link' : 'vdf==1 .or. vdf==6 .or. @pyoratieluokka==3 .and. mode==f'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()

    network_calc['specification'] = {'aggregation' : None,
        'expression' : 72,
        'result' : 'vdf',
        'selections' : {'link' : 'vdf==2 .or. vdf==7 .and. @pyoratieluokka==2'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()
    
    network_calc['specification'] = {'aggregation' : None,
        'expression' : 73,
        'result' : 'vdf',
        'selections' : {'link' : 'vdf==3,4 .or. vdf==8,9 .and. @pyoratieluokka==2'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()
    
    network_calc['specification'] = {'aggregation' : None,
        'expression' : 74,
        'result' : 'vdf', 
        'selections' : {'link' : 'vdf==0 .or. vdf==5 .or. vdf==10 .or. vdf==99 .and. ' +
            '@pyoratieluokka==2'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()
    
    network_calc['specification'] = {'aggregation' : None,
        'expression' : 75,
        'result' : 'vdf',
        'selections' : {'link' : '@pyoratieluokka==1'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()
    
    network_calc['specification'] = {'aggregation' : None,
        'expression' : 76,
        'result' : 'vdf',
        'selections' : {'link' : 'vdf==2 .or. vdf==7 .and. @pyoratieluokka==0 .and. mode==f'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()
    
    network_calc['specification'] = {'aggregation' : None,
        'expression' : 77,
        'result' : 'vdf',
        'selections' : {'link' : 'vdf==3,4 .or. vdf==8,9 .or. type==138,140 .or. ' +
            'type==238,240 .or. type==338,340 .or. type==438,440  .or. type==538,540 .or. ' + 
            'type==638,640 .and. @pyoratieluokka==0 .and. mode==f'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()
    
    network_calc['specification'] = {'aggregation' : None,
        'expression' : 78,
        'result' : 'vdf',
        'selections' : {'link' : 'vdf==0 .or. vdf==5 .or. vdf==10 .or. vdf==99 .and. ' + 
            '@pyoratieluokka==2 .and. mode==f'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()
    