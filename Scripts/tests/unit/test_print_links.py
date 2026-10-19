import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from datahandling.resultdata import ResultsData
from utils.print_links import linkwise_transit_capacity, print_links


class PrintLinksTest(unittest.TestCase):
    def test_zero_headways_are_ignored(self):
        class Segment(dict):
            line: SimpleNamespace

        segment = Segment({
            "@hw_aht": 0,
            "@hw_pt": 10,
            "@hw_iht": 999,
        })
        segment.line = SimpleNamespace(
            vehicle=SimpleNamespace(seated_capacity=30, total_capacity=60))

        class Link:
            def segments(self):
                return [segment]

        self.assertEqual(
            linkwise_transit_capacity(Link()), (0, 0, 360, 180, 0, 0))

    def test_header_matches_data_columns(self):
        class Link:
            i_node = SimpleNamespace(id=1, x=10, y=20)
            j_node = SimpleNamespace(id=2, x=30, y=40)
            modes = []

            def __getitem__(self, attribute):
                return 5

            def segments(self):
                return []

        class Network:
            def attributes(self, domain):
                return ["@example"]

            def links(self):
                return [Link()]

        scenario = SimpleNamespace(id=7, get_network=lambda: Network())

        with tempfile.TemporaryDirectory() as output_directory:
            resultdata = ResultsData(output_directory)
            with patch("utils.print_links.NoiseModel") as noise_model:
                noise_model.return_value.calc_noise.return_value = 12
                print_links(scenario, resultdata)

            with open(f"{output_directory}/links_7.txt") as output_file:
                header, row = [line.rstrip("\n").split("\t") for line in output_file]

        self.assertEqual(len(header), len(row))
        self.assertEqual(header[-7:], [
            "transit_cap_total_aht", "transit_cap_seated_aht",
            "transit_cap_total_pt", "transit_cap_seated_pt",
            "transit_cap_total_iht", "transit_cap_seated_iht",
            "Noise_zone_width",
        ])