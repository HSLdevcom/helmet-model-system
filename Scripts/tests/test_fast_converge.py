import unittest

import numpy as np

from utils.fast_converge import FastConvergence


def impedance(car_work, car_leisure, transit):
    return {"aht": {"time": {
        "car_work": np.array([[car_work]], dtype=float),
        "car_leisure": np.array([[car_leisure]], dtype=float),
        "transit_work": np.array([[transit]], dtype=float),
    }}}


class FastConvergenceTest(unittest.TestCase):
    def test_relaxes_only_car_matrices_then_releases_raw_feedback(self):
        controller = FastConvergence(enabled=True)
        previous = impedance(10, 20, 30)
        assigned = impedance(14, 28, 50)
        next_input, eligible = controller.update(previous, assigned, False)
        self.assertFalse(eligible)
        self.assertEqual(next_input["aht"]["time"]["car_work"][0, 0], 12)
        self.assertEqual(next_input["aht"]["time"]["car_leisure"][0, 0], 24)
        self.assertEqual(next_input["aht"]["time"]["transit_work"][0, 0], 50)
        self.assertEqual(previous["aht"]["time"]["car_work"][0, 0], 10)

        raw = impedance(13, 25, 52)
        next_input, eligible = controller.update(next_input, raw, True)
        self.assertIs(next_input, raw)
        self.assertFalse(eligible)
        self.assertFalse(controller.active)

        raw_next = impedance(13.1, 25.1, 52)
        next_input, eligible = controller.update(raw, raw_next, True)
        self.assertIs(next_input, raw_next)
        self.assertTrue(eligible)

    def test_first_pass_on_final_iteration_cannot_claim_convergence(self):
        controller = FastConvergence(enabled=True)
        previous = impedance(10, 20, 30)
        assigned = impedance(14, 28, 50)
        next_input, eligible = controller.update(previous, assigned, True, is_final=True)
        self.assertIs(next_input, assigned)
        self.assertFalse(eligible)

    def test_disabled_keeps_original_feedback(self):
        controller = FastConvergence(enabled=False)
        assigned = impedance(14, 28, 50)
        next_input, eligible = controller.update(impedance(10, 20, 30), assigned, True)
        self.assertIs(next_input, assigned)
        self.assertTrue(eligible)


if __name__ == "__main__":
    unittest.main()
