from IPython.display import display
import os
import math as _math
import inro.modeller as _m

def bus_stops(self, scen_id):
    """ 
    booardings and alightnings of buses basing on node attribute ui2, ui3 and @hsl values

    ui2-kentassa tulee olla tieto, millaisten linjojen pysakki on kyseessa
        ui2=0, ei pysakki (samoin ui2=20 ja muutkin joita ei ole alla lueteltu)
        ui2=1, ratikka- ja pikaratikkapysakki
        ui2=2, bussipysakki paikallisliikenne (HSL+Vallu)
        ui2=3, bussipysakki paikallis- ja runkoliikenne
        ui2=4, bussipysakki paikallis- ja pikavuoroliikenne
        ui2=5, bussipysakki paikallis, runko- ja pikavuoroliikenne
        ui2=7, bussipysakki pikavuoro- ja valluliikenne, ei HSL
        ui2=11, bussiterminaali (kaikki linjat)

    ui3-kentassa tulee olla tieto kunnasta
    HSL-alueen kunnat 2016 ovat:
         49 Espoo
         91 Helsinki 
         92 Vantaa
        235 Kauniainen
        245 Kerava
        257 Kirkkonummi 
        753 Sipoo
        755 Siuntio
        858 Tuusula

    Vallu-linjojen (d) ja pikavuorojen (e) linjatunnuksessa on oltava
    tasmalleen 6 merkkia, joista viimeinen kuvaa suuntaa (1 tai 2). 
    Kokonaan HSL-alueen ulkopuolella kulkevilla linjoilla suunnalla ei
    ole niin valia, koska linja pysahtyy joka tapauksessa kaikilla
    pysakeilla (pikavuoro kaikilla pikavuoropysakeilla). Linjatunnukset
    kuudennen (6.) merkin pitaa kuitenkin olla 1 tai 2, jotta makro toimii.  

    Attribuutti @hsl kertoo, onko pysakki (solmu) HSL-alueella (0=ei, 1=on). 
    varmista @hsl-attribuutin olemassa olo (solmuattribuutti)
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

    # *** poistetaan kaikki pysakit bussi-, ratikka- ja pikaratikkalinjoilla 

    network_calc['specification'] = {'aggregation' : None,
        'expression' : '1',
        'result' : 'noali',
        'selections' : {'link' : 'mode==bgdetp', 'line' : 'mode==bgdetp'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()

    network_calc['specification'] = {'aggregation' : None,
        'expression' : '1',
        'result' : 'noboa',
        'selections' : {'link' : 'mode==bgdetp', 'line' : 'mode==bgdetp'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()

    # *** lisataan ratikkapysakkien (t ja p) poistumiset ja nousemiset

    network_calc['specification'] = {'aggregation' : None,
        'expression' : '1-(uj2==1)',
        'result' : 'noalin',
        'selections' : {'link' : 'mode==tp', 'line' : 'mode==tp'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()

    network_calc['specification'] = {'aggregation' : None,
        'expression' : '1-(ui2==1)',
        'result' : 'noboa',
        'selections' : {'link' : 'mode==tp', 'line' : 'mode==tp'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()

    # *** lisataan HSL-bussien (b) poistumiset ja nousemiset

    network_calc['specification'] = {'aggregation' : None,
        'expression' : '1-((uj2==2)+(uj2==3)+(uj2==4)+(uj2==5)+(uj2==11))',
        'result' : 'noalin',
        'selections' : {'link' : 'mode==b', 'line' : 'mode==b'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()

    network_calc['specification'] = {'aggregation' : None,
        'expression' : '1-((ui2==2)+(ui2==3)+(ui2==4)+(ui2==5)+(ui2==11))',
        'result' : 'noboa',
        'selections' : {'link' : 'mode==b', 'line' : 'mode==b'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()

    # *** lisataan runkolinjojen (g) poistumiset ja nousemiset

    network_calc['specification'] = {'aggregation' : None,
        'expression' : '1-((uj2==3)+(uj2==5)+(uj2==11))',
        'result' : 'noalin',
        'selections' : {'link' : 'mode==g', 'line' : 'mode==g'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()

    network_calc['specification'] = {'aggregation' : None,
        'expression' : '1-((ui2==3)+(ui2==5)+(ui2==11))',
        'result' : 'noboa',
        'selections' : {'link' : 'mode==g', 'line' : 'mode==g'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()

    # *** lisataan pikavuorot (e) ykkossuuntaan eli Helsingista poispain

    # poistumiset (pikavuoropysakeilla HSL-alueen ulkopuolella)
    network_calc['specification'] = {'aggregation' : None,
        'expression' : '1-((@hsl==0) .and. ((uj2==4)+(uj2==5)+(uj2==7)+(uj2==11)))',
        'result' : 'noalin',
        'selections' : {'link' : 'mode==e', 'line' : 'mode==e .and. _____1'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()

    # nousut (kaikilla pikavuoropysakeilla)
    network_calc['specification'] = {'aggregation' : None,
        'expression' : '1-((ui2==4)+(ui2==5)+(ui2==7)+(ui2==11))',
        'result' : 'noboa',
        'selections' : {'link' : 'mode==e', 'line' : 'mode==e .and. _____1'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()

    # *** lisataan pikavuorot (e) kakkossuuntaan eli Helsinkiin pain

    #poistumiset (kaikilla pikavuoropysakeilla)
    network_calc['specification'] = {'aggregation' : None,
        'expression' : '1-((uj2==4)+(uj2==5)+(uj2==7)+(uj2==11))',
        'result' : 'noalin',
        'selections' : {'link' : 'mode==e', 'line' : 'mode==e .and. _____2'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()

    #nousut (pikavuoropysakeilla HSL-alueen ulkopuolella)
    network_calc['specification'] = {'aggregation' : None,
        'expression' : '1-((@hsl==0) .and. ((ui2==4)+(ui2==5)+(ui2==7)+(ui2==11)))',
        'result' : 'noboa',
        'selections' : {'link' : 'mode==e', 'line' : 'mode==e .and. _____2'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()

    # *** lisataan Vallu-linjat (d) ykkossuuntaan eli Helsingista poispain

    # poistumiset (kaikilla bussipysakeilla HSL-alueen ulkopuolella)
    network_calc['specification'] = {'aggregation' : None,
        'expression' : '1-((@hsl==0) .and. ((uj2==2)+(uj2==3)+' +
            '(uj2==4)+(uj2==5)+(uj2==7)+(uj2==11)))',
        'result' : 'noalin',
        'selections' : {'link' : 'mode==d', 'line' : 'mode==d .and. _____1'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()

    # nousut (kaikilla bussipysakeilla)
    network_calc['specification'] = {'aggregation' : None,
        'expression' : '1-((ui2==2)+(ui2==3)+(ui2==4)+(ui2==5)+(uj2==7)+(ui2==11))',
        'result' : 'noboa',
        'selections' : {'link' : 'mode==d', 'line' : 'mode==d .and. _____1'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()

    # *** lisataan Vallu-linjat (d) kakkossuuntaan eli Helsinkiin pain
 
    #poistumiset (kaikilla bussipysakeilla)
    network_calc['specification'] = {'aggregation' : None,
        'expression' : '1-((uj2==2)+(uj2==3)+(uj2==4)+(uj2==5)+(uj2==7)+(uj2==11))',
        'result' : 'noalin',
        'selections' : {'link' : 'mode==d', 'line' : 'mode==d .and. _____2'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()

    #nousut (kaikilla bussipysakeilla HSL-alueen ulkopuolella)
    network_calc['specification'] = {'aggregation' : None,
        'expression' : '1-((@hsl==0) .and. ((ui2==2)+(ui2==3)+' +
            '(ui2==4)+(ui2==5)+(uj2==7)+(ui2==11)))',
        'result' : 'noboa',
        'selections' : {'link' : 'mode==d', 'line' : 'mode==d .and. _____2'},
        'type' : 'NETWORK_CALCULATION'}
    network_calc.run()

    display('Bussi-, ratikka- ja pikaratikkalinjojen pysakit on korjattu ui2- ja ui3-tietojen mukaisiksi.')

