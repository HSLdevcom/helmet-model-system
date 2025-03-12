from pathlib import Path
from events.model_system_event_listener import ModelSystemEventListener
from utils import log
from utils.validation import Validation, bar_plot, mean

class ModeShareAnalysis(ModelSystemEventListener):
    """
    A class to analyze mode shares.
    """
    data_path: Path
    result_path: Path
    validation: Validation
        
    def __init__(self):
        self.validation = None
        super().__init__()
    
    def on_simulation_started(self, forecastdata_path, result_path, args):
        self.result_path = result_path

    def on_validation_initialized(self, validation, validation_path):
        self.validation = validation
        self.data_path = validation_path / 'data'

    def on_simulation_complete(self):
        if self.validation is None:
            log.warn("Validation not initialized, skipping mode share analysis")
            return
        if not self.data_path.is_dir():
            log.warn(f"Validation data directory not found at {self.data_path}, skipping mode share analysis")
            return

        model_mode_shares = parse_mode_shares(self.result_path / 'result_summary.txt')
        survey_mode_shares = parse_mode_shares(self.data_path / 'result_summary_lt23.txt')
        helmet4_mode_shares = parse_mode_shares(self.data_path / 'result_summary_helmet4.txt')
        group = self.validation.create_group('Mode shares (result_summary.txt)')
        for mode, share in model_mode_shares.items():
            group.add_item(id=mode,
                           prediction=share,
                           expected=survey_mode_shares.get(mode, 0),
                           helmet4=helmet4_mode_shares.get(mode, 0))
        group.add_aggregation('mean_error', mean('absolute_error'))
        group.add_visualization('Mode shares', bar_plot(y=['prediction', 'expected', 'helmet4']))

def parse_mode_shares(filepath):
    """
    Lukee tiedoston ja palauttaa sanakirjan, jossa avaimina ovat liikennemuodot
    ja arvoina niiden osuus (prosentteina).
    """
    mode_shares = {}
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Tiedostoa ei löytynyt: {filepath}")
        return mode_shares

    # Etsi rivi, jossa lukee "Mode shares"
    start_index = None
    for i, line in enumerate(lines):
        if "Mode shares" in line:
            start_index = i + 1
            break

    if start_index is None:
        print(f"Mode shares -riviä ei löytynyt tiedostosta: {filepath}")
        return mode_shares

    # Käydään läpi osion rivit
    for line in lines[start_index:]:
        line = line.strip()
        if not line:
            break  # Oletetaan, että tyhjä rivi tarkoittaa osion loppua

        parts = line.split()
        if len(parts) < 2:
            continue

        mode = parts[0]
        try:
            # Poistetaan prosenttimerkki ja muunnetaan liukuluvuksi
            value = float(parts[1].replace('%', ''))
        except ValueError:
            continue

        mode_shares[mode] = value

    return mode_shares
