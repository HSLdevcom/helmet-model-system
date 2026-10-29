from types import SimpleNamespace
import unittest

import numpy

from datatypes.tour import Tour
from models.logit import ModeDestModel


class TourOutputTest(unittest.TestCase):
    def setUp(self):
        zone_data = SimpleNamespace(
            all_zone_numbers=numpy.array([100, 200, 34031]),
            zone_numbers=numpy.array([100, 200]),
            nr_zones=2,
        )
        self.purpose = SimpleNamespace(
            name="hw",
            bounds=slice(0, 1),
            zone_data=zone_data,
            sustainable_access={},
            modes=["car"],
            model=SimpleNamespace(
                cumul_dest_prob={
                    "car": numpy.array([[0.2], [0.8], [1.0]])
                }
            ),
            attracted_tours={"car": numpy.zeros(2)},
            dist=numpy.array([[1.0, 2.0]]),
            histograms={"car": SimpleNamespace(add=lambda distance: None)},
            aggregates={"car": SimpleNamespace(add=lambda orig, dest: None)},
            own_zone_aggregates={
                "car": SimpleNamespace(add=lambda orig: None)
            },
            sec_dest_purpose=SimpleNamespace(bounds=slice(5, 6)),
        )
        self.tour = Tour.__new__(Tour)
        self.tour.purpose = self.purpose
        self.tour.purpose_name = "hw"
        self.tour._mode_idx = 0
        self.tour._position = (0,)
        self.tour._dest_draw = 0.9
        self.tour._sec_dest_gen_draw = 1.0

    def test_output_zone_ids_use_full_zone_mapping(self):
        self.tour.position = (0, 1, 2)

        self.assertEqual(self.tour.orig, 100)
        self.assertEqual(self.tour.dest, 200)
        self.assertEqual(self.tour.sec_dest, 34031)

    def test_tour_output_includes_zone_columns(self):
        self.tour.person_id = 1
        self.tour.total_access = 2.0
        self.tour.cost = 4.0
        self.tour.gen_cost = 5.0
        self.tour.position = (0, 1, 2)

        self.assertEqual(
            Tour.attr,
            [
                "person_id", "purpose_name", "mode", "total_access",
                "sustainable_access", "cost", "gen_cost", "orig", "dest",
                "sec_dest",
            ],
        )
        self.assertEqual(
            str(self.tour).split("\t"),
            ["1", "hw", "car", "2.0", "-1", "4.0", "5.0", "100", "200", "34031"],
        )

    def test_destination_choice_excludes_external_zones(self):
        self.tour.choose_destination({})

        self.assertEqual(self.tour.dest, 200)
        self.assertEqual(self.purpose.attracted_tours["car"].tolist(), [0, 1])

    def test_destination_choice_reports_empty_probability_rows(self):
        self.purpose.model.cumul_dest_prob["car"] = numpy.array(
            [[numpy.nan], [numpy.nan], [numpy.nan]]
        )

        with self.assertRaisesRegex(ValueError, "No valid destination probabilities"):
            self.tour.choose_destination({})

    def test_individual_mode_choice_excludes_modes_without_destinations(self):
        model = ModeDestModel.__new__(ModeDestModel)
        model.purpose = SimpleNamespace(modes=["car", "walk"])
        model.mode_utils = {
            "car": numpy.array([1.0]),
            "walk": numpy.array([10.0]),
        }
        model.mode_choice_param = {
            "car": {"individual_dummy": {}},
            "walk": {"individual_dummy": {}},
        }
        model.dest_expsums = {
            "car": {"logsum": numpy.array([1.0])},
            "walk": {"logsum": numpy.array([0.0])},
        }

        utils = model.calc_individual_mode_prob(False, 0)

        self.assertEqual(utils[0], 1.0)
        self.assertEqual(utils[1], -numpy.inf)

    def test_basic_destination_probabilities_are_zero_when_unavailable(self):
        model = ModeDestModel.__new__(ModeDestModel)
        model._calc_utils = lambda impedance: None
        model.mode_choice_param = {"car": {}}
        model.dest_exps = {
            "car": numpy.array([[0.0, 0.0], [1.0, 1.0]])
        }

        model.calc_basic_prob({})

        numpy.testing.assert_array_equal(
            model.cumul_dest_prob["car"],
            numpy.array([[0.0, 0.5], [0.0, 1.0]]),
        )


if __name__ == "__main__":
    unittest.main()
