from types import SimpleNamespace
import unittest

import numpy as np

from datatypes.tour import Tour
from models.park_and_ride_model import ParkAndRideModel, ParkAndRideUtilities
from parameters.assignment import vot_inv


class ParkAndRideTourCostTest(unittest.TestCase):
    def test_tour_cost_and_generalized_cost_include_both_legs(self):
        model = ParkAndRideModel.__new__(ParkAndRideModel)
        model._purpose = SimpleNamespace(
            name="hw",
            bounds=slice(0, 1),
        )
        model._facilities = [
            SimpleNamespace(zone_offset=0),
            SimpleNamespace(zone_offset=1),
        ]
        model._saved_utilities = ParkAndRideUtilities(
            car_utility=np.array([[[0.0, np.log(3.0)]]]),
            transit_utility=np.zeros((1, 2, 2)),
            facility_utility=np.zeros((1, 1, 2)),
        )
        model._day_impedance = {
            "car_work": {
                "cost": np.array([[2.0, 6.0], [0.0, 0.0]]),
                "time": np.array([[1.0, 3.0], [0.0, 0.0]]),
            },
            "transit_work": {
                "cost": np.array([[0.0, 10.0], [0.0, 20.0]]),
                "time": np.array([[0.0, 5.0], [0.0, 7.0]]),
            },
        }

        purpose = SimpleNamespace(
            name="hw",
            park_and_ride_model=model,
            modes=["park_and_ride"],
        )
        tour = Tour.__new__(Tour)
        tour._mode_idx = 0
        tour.purpose = purpose
        tour.purpose_name = "hw"
        tour._position = (0, 1)

        tour.calc_cost({})

        self.assertAlmostEqual(tour.cost, 22.5)
        self.assertAlmostEqual(
            tour.gen_cost, 22.5 + 9.0 / vot_inv["work"]
        )


if __name__ == "__main__":
    unittest.main()
