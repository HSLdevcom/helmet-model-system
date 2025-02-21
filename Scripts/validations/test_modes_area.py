from pathlib import Path

from events.model_system_event_listener import ModelSystemEventListener
from utils import log
from utils.validation import Validation, bar_plot, mae


class TripLengthAnalysis(ModelSystemEventListener):
    """
    A class to analyze trip lengths in a model system by listening to specific events.
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
            log.warn("Validation not initialized, skipping trip length analysis")
            return
        
        header, data = parse_trips_areas(self.result_path / 'trips_areas.txt')
        _, data_helmet4 = parse_trips_areas(self.data_path / 'trips_areas_helmet4.txt')

        group = self.validation.create_group('Trip areas vs helmet4')
        for area, values in data.items():
            for mode, value in values.items():
                group.add_item(area, value, data_helmet4[area].get(mode, 0), mode=mode)
        group.add_visualization('Trip lengths', bar_plot(color='mode'))
        group.add_aggregation('mean absolute error', mae, group_by='mode')

def parse_trips_areas(filepath):
    """
    Lukee tiedoston, jossa on taulukkomuotoinen data.

    Jos ensimmäinen rivi alkaa merkkijonolla "trips_areas:",
    poistetaan se ja käytetään jäljellä olevia sarakenimiä.
    Ensimmäinen sarake oletetaan olevan alueiden nimi (area),
    ja seuraavissa sarakkeissa ovat eri matkustusmuotojen (esim. car, transit jne.) arvot.

    Palauttaa tuple:n (header, data), jossa
      - header on lista sarakkeiden nimistä
      - data on sanakirja, jonka avaimina ovat alueiden nimet ja
        arvoina sanakirjat, joissa kunkin mode:n arvo on tallennettuna.
    """
    data = {}
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Poistetaan tyhjät rivit ja ylimääräiset välilyönnit
    lines = [line.strip() for line in lines if line.strip()]
    
    # Tarkastellaan ensimmäistä riviä: onko se "trips_areas:" -alkuinen
    tokens = lines[0].split()
    if tokens[0].lower().startswith('trips_areas'):
        header = ["area"] + tokens[1:]
        data_lines = lines[1:]
    else:
        header = tokens
        if header[0].lower() != "area":
            header = ["area"] + header
        data_lines = lines[1:]
    
    for line in data_lines:
        tokens = line.split()
        if len(tokens) < len(header):
            continue
        area = tokens[0]
        values = {}
        for col, token in zip(header[1:], tokens[1:]):
            try:
                values[col] = float(token)
            except ValueError:
                values[col] = 0.0
        data[area] = values

    return header, data
