import subprocess, os
import unittest

TEST_DATA_PATH = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "..", "test_data")
MODELSYSTEM = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "..", "..")
RESULTSPATH = os.path.join(TEST_DATA_PATH, "Results")
EMMEPATH = None #relatiivinen polku projektin .emp tiedostoon
BASELINEPATH = os.path.join(TEST_DATA_PATH, "Base_input_data")
FORECASTPATH = os.path.join(TEST_DATA_PATH, "Scenario_input_data")

def run_helmet(scenario_name, first_scenario_id, forecast_data_folder, modelsystem=MODELSYSTEM, baselinepath=BASELINEPATH, optional_arguments=''):
    """Wrapper around helmet.py CLI call

    Return code is *not* checked so if errors are found, one model run
    will stop but the script resumes."""

    command = f'python {modelsystem}/helmet.py \
        --log-level DEBUG \
        --del-strat-files \
        --scenario-name {scenario_name} \
        --results-path "{RESULTSPATH}" \
        --emme-path {EMMEPATH} \
        --first-scenario-id {first_scenario_id} \
        --baseline-data-path {baselinepath} \
        --forecast-data-path {FORECASTPATH}/{forecast_data_folder} \
        --iterations 15'
    print(command)
    subprocess.run('python {modelsystem}/helmet.py \
        --log-level DEBUG \
        --del-strat-files \
        --scenario-name {scenario_name} \
        --results-path "{resultspath}" \
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

    
class TestMockRun(unittest.TestCase):
     def run_mock_run(self):
        print('[BATCH] Run: 2023')
        run_helmet(scenario_name='test01', modelsystem=MODELSYSTEM, first_scenario_id=1, forecast_data_folder='2023')
