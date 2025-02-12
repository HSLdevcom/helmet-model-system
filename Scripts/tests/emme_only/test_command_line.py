""""Petr Hajduk, based on MAL 2023 Model runs / Johanna Piipponen HSL 2022"""
import subprocess

HDD_PATH = "XXX" #absoluuttinen polku Helmet kansioon
MODELSYSTEM = HDD_PATH+'model-systems/helmet-model-system/Scripts'
RESULTSPATH = "XXX" #absoluuttinen polku tuloskansioon
EMMEPATH = HDD_PATH+"XXX" #relatiivinen polku projektin .emp tiedostoon
BASELINEPATH = HDD_PATH+'Lahtodata'
FORECASTPATH = HDD_PATH+'Ennusteskenaarioiden_syottotiedot'

def run_python_version():
    """Wrapper around python --version"""
    subprocess.run('python --version', check=True)

def run_input_validation(first_scenario_ids, forecast_data_folders, baselinepath=BASELINEPATH):
    """Wrapper around helmet_validate_inputfiles.py CLI call

    The return code is checked and if errors are found,
    subprocess.CalledProcessError is raised and model runs are stopped.
    """
    if len(first_scenario_ids) != len(forecast_data_folders):
        raise ValueError
    first_scenario_ids_string = ' '.join([str(id) for id in first_scenario_ids])
    forecast_data_paths_string = ' '.join([FORECASTPATH + '/' + folder for folder in forecast_data_folders])
    emme_paths_string = ' '.join([EMMEPATH] * len(first_scenario_ids))
    subprocess.run('python -u {modelsystem}/helmet_validate_inputfiles.py \
        --log-level DEBUG \
        --scenario-name input_file_validation \
        --results-path {resultspath} \
        --baseline-data-path {baselinepath} \
        --emme-paths {emme_paths} \
        --first-scenario-ids {first_scenario_ids} \
        --forecast-data-paths {forecast_data_paths}'
        .format(modelsystem=MODELSYSTEM,
                resultspath=RESULTSPATH,
                baselinepath=baselinepath,
                emme_paths=emme_paths_string,
                first_scenario_ids=first_scenario_ids_string,
                forecast_data_paths=forecast_data_paths_string),
        check=True)

def run_helmet(scenario_name, first_scenario_id, forecast_data_folder, modelsystem=MODELSYSTEM, baselinepath=BASELINEPATH, optional_arguments=''):
    """Wrapper around helmet.py CLI call

    Return code is *not* checked so if errors are found, one model run
    will stop but the script resumes."""

    command = f'python {modelsystem}/helmet.py \
        --log-level DEBUG \
        --del-strat-files \
        --scenario-name {scenario_name} \
        --results-path {RESULTSPATH} \
        --emme-path {EMMEPATH} \
        --first-scenario-id {first_scenario_id} \
        --baseline-data-path {baselinepath} \
        --forecast-data-path {FORECASTPATH}/{forecast_data_folder} \
        --iterations 15'
    print(command)
    exit()
    subprocess.run('python {modelsystem}/helmet.py \
        --log-level DEBUG \
        --del-strat-files \
        --scenario-name {scenario_name} \
        --results-path {resultspath} \
        --emme-path {emmepath} \
        --first-scenario-id {first_scenario_id} \
        --baseline-data-path {baselinepath} \
        --forecast-data-path {forecastpath}/{forecast_data_folder} \
        --iterations 15 \
        {optional_arguments}'
        .format(modelsystem=modelsystem,
                resultspath=RESULTSPATH,
                baselinepath=baselinepath,
                emmepath=EMMEPATH,
                forecastpath=FORECASTPATH,
                scenario_name=scenario_name,
                first_scenario_id=first_scenario_id,
                forecast_data_folder=forecast_data_folder,
                optional_arguments=optional_arguments),
        check=False)

def run_cba(baseline_scenario, projected_scenario, optional_arguments=''):
    """Wrapper around cba.py CLI call

    Return code is *not* checked so if errors are found, one model run
    will stop but the script resumes."""

    subprocess.run('python {modelsystem}/cba.py \
        {resultspath}/{baseline_scenario} \
        {resultspath}/{projected_scenario} \
        --log-level DEBUG \
        --log-format TEXT \
        --results-path {resultspath}/{projected_scenario} \
        {optional_arguments}'
        .format(modelsystem=MODELSYSTEM,
                resultspath=RESULTSPATH,
                baseline_scenario=baseline_scenario,
                projected_scenario=projected_scenario,
                optional_arguments=optional_arguments),
        check=False)


def main():
    """"Handles test model runs"""


    print('[BATCH] Starting input file validation...')
    # run_input_validation(first_scenario_ids=[100],
    #                      forecast_data_folders=['2023_Santeri_v2'])
    print('[BATCH] Finished input file validation!')

    modelsystem_olusanya = MODELSYSTEM

    print('[BATCH] Starting model runs...')

    print('[BATCH] Run: 2023')
    run_helmet(scenario_name='2023_pohjaverkko_2024_11_29', modelsystem=modelsystem_olusanya, first_scenario_id=100, forecast_data_folder='2023_Santeri_v2', optional_arguments='-e -s -E')
    
    print('[BATCH] Run: CBA (ve0 -> ve2)')
    #run_cba(baseline_scenario='2040_ve0', projected_scenario='2040_suunnitelmaluonnos_alennus35')

    print('[BATCH] Finished model runs!')

if __name__ == "__main__":
    main()
