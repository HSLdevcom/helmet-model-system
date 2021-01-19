from IPython.display import display
import os
import math as _math
import inro.modeller as _m

def function_parameters(self, scen_id, period):
    """ valitaan kunkin aikajakson viivytysfunktio ja muutetetaan niiden parametreja

    """

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
    
    # *** maaritellaan poikkeuksellisten linkkien (x91-x95) viivytysfunktiot, tuloksena 1 <= vdf <= 5
    
    expr_x91_x95 = '' \
        '(type-190)*(type.ge.191)*(type.le.195) + (type-290)*(type.ge.291)*(type.le.295) + ' \
        '(type-390)*(type.ge.391)*(type.le.395) + (type-490)*(type.ge.491)*(type.le.495) + ' \
        '(type-590)*(type.ge.591)*(type.le.595) + (type-690)*(type.ge.691)*(type.le.695)'
    selec_x91_x95 = 'type=191,195 or type=291,295 or type=391,395 ' \
            'or type=491,495 or type=591,595 or type=691,695'
    
    network_calc['specification'] = {'aggregation' : None,
        'expression' : expr_x91_x95,
        'result' : 'vdf',
        'selections' : {'link' : selec_x91_x95},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()

    # *** poistetaan mahdollisen bussikaistan funktiomaarittely, tuloksena 1 <= vdf <= 5
    
    network_calc['specification'] = {'aggregation' : None,
        'expression' : 'vdf-5*(vdf.ge.6)*(vdf.le.10)',
        'result' : 'vdf',
        'selections' : {'link' : 'all'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()
    
    # *** tehdaan aikajaksokohtaiset maaritykset
    
    if period == 'aht':
        road_types  = 'type=201,299 or type=301,399 or type=401,499 or type=601,699'
        capas_value = '2100*((type.eq.222)+(type.eq.322)+(type.eq.422)) + ' \
            '2000*((type.eq.224)+(type.eq.324)+(type.eq.424)) + ' \
            '2000*((type.eq.226)+(type.eq.326)+(type.eq.426)) + ' \
            '1900*((type.eq.228)+(type.eq.328)+(type.eq.428)) + ' \
            '1850*((type.eq.230)+(type.eq.330)+(type.eq.430))'
        capas_type = 'type=222,230 or type=322,330 or type=422,430 and lan=3,9'
        ttf_tram = '3'
    elif period == 'iht':
        road_types  = 'type=201,299 or type=301,399 or type=501,599 or type=601,699'
        capas_value = '2100*((type.eq.222)+(type.eq.322)+(type.eq.522)) + ' \
            '2000*((type.eq.224)+(type.eq.324)+(type.eq.524)) + ' \
            '2000*((type.eq.226)+(type.eq.326)+(type.eq.526)) + ' \
            '1900*((type.eq.228)+(type.eq.328)+(type.eq.528)) + ' \
            '1850*((type.eq.230)+(type.eq.330)+(type.eq.530))'
        capas_type = 'type=222,230 or type=322,330 or type=522,530 and lan=3,9'
        ttf_tram = '5'
    elif period == 'pt':
        road_types  = 'type=301,399 or type=601,699'
        capas_value = '2100*(type.eq.322) + 2000*(type.eq.324) + 2000*(type.eq.326) + ' \
            '1900*(type.eq.328) + 1850*(type.eq.330)'
        capas_type = 'type=322,330 and lan=3,9'
        ttf_tram = '4'
    else:
        road_types  = 'mode=w' # None ei toimi, yritetaan minimoida vahinko
        capas_value = 'ul1'
        capas_type  = 'all'
        ttf_tram = '4'
        display('time period ', period, ' not recognized')
        
    # *** lisataan aikajaksolle bussikaistafunktio

    network_calc['specification'] = {'aggregation' : None,
        'expression' : 'vdf+5*(vdf.le.5)',
        'result' : 'vdf',
        'selections' : {'link' : road_types},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()
    
    # *** muutetaan kapasiteettia (ul1), jos vahintaan kolmesta kaistasta yksi on joukkoliikennekaista
    
    network_calc['specification'] = {'aggregation' : None,
        'expression' : capas_value,
        'result' : 'ul1',
        'selections' : {'link' : capas_type},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()
    
    # *** parametri us2 bussikaistattomalla tiella
    
    us2_param_list = [
    [0.265, 'vdf==1 && ul2==112,130'],
    [0.309, 'vdf==1 && ul2==96,111.9'], 
    [0.370, 'vdf==1 && ul2==80,95.9'], 
    [0.309, 'vdf==2 && ul2==96,130 '], 
    [0.370, 'vdf==2 && ul2==80,95.9'], 
    [0.411, 'vdf==2 && ul2==70,79.9'], 
    [0.556, 'vdf==2 && ul2==50,69.9'], 
    [0.492, 'vdf==3 && ul2==60,130 '], 
    [0.556, 'vdf==3 && ul2==40,59.9'], 
    [0.625, 'vdf==4 && ul2==47,130 '], 
    [0.682, 'vdf==4 && ul2==43,46.9'], 
    [0.732, 'vdf==4 && ul2==10,42.9'], 
    [0.732, 'vdf==5 && ul2==40,130 '], 
    [0.833, 'vdf==5 && ul2==35,39.9'], 
    [1.000, 'vdf==5 && ul2==28,34.9'], 
    [1.304, 'vdf==5 && ul2==10,27.9']
    ]
    
    for k in range(len(us2_param_list)):
        network_calc['specification'] = {'aggregation' : None,
            'expression' : us2_param_list[k][0],
            'result' : 'us2',
            'selections' : {'link' : us2_param_list[k][1], line : 'mode=bgde'},
            'type' : 'NETWORK_CALCULATION'}
        network_calc.run()
     
    # *** parametri us2 bussikaistallisella tiella
    
    network_calc['specification'] = {'aggregation' : None,
        'expression' : '(60*1.5)/(ul2.max.30)',
        'result' : 'us2',
        'selections' : {'link' : road_types + ' and vdf=6,7', line : 'mode=bgde'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()
    
    network_calc['specification'] = {'aggregation' : None,
        'expression' : '(60*1.6)/(ul2.max.30)',
        'result' : 'us2',
        'selections' : {'link' : road_types + ' and vdf=8', line : 'mode=bgde'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()
    
    network_calc['specification'] = {'aggregation' : None,
        'expression' : '(60*1.7)/(ul2.max.30)',
        'result' : 'us2',
        'selections' : {'link' : road_types + ' and vdf=9,10', line : 'mode=bgde'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()
        
    # *** joukkoliikenteen viivytysfunktiot
    
    network_calc['specification'] = {'aggregation' : None,
        'expression' : '1',
        'result' : 'ttf',
        'selections' : {'link' : 'all', line : 'mode=bgde'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()
    
    network_calc['specification'] = {'aggregation' : None,
        'expression' : '2',
        'result' : 'ttf',
        'selections' : {'link' : road_types, line : 'mode=bgde'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()
    
    network_calc['specification'] = {'aggregation' : None,
        'expression' : ttf_tram,
        'result' : 'ttf',
        'selections' : {'link' : 'all', line : 'mode=tp'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()
    
    network_calc['specification'] = {'aggregation' : None,
        'expression' : '6',
        'result' : 'ttf',
        'selections' : {'link' : 'all', line : 'mode=rjm'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()
    