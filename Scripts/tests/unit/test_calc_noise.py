import unittest

from utils.calc_noise import NoiseModel


class MockLink:
    def __init__(
        self, i_node, j_node, attributes, length=1.0, data2=50.0
    ):
        self.i_node = i_node
        self.j_node = j_node
        self.attributes = attributes
        self.length = length
        self.data2 = data2
        self.reverse_link = None
        self.id = "{}-{}".format(i_node, j_node)

    def __getitem__(self, key):
        return self.attributes[key]


class MockNetwork:
    def __init__(self, links):
        self.links = {
            (link.i_node, link.j_node): link for link in links
        }

    def link(self, i_node, j_node):
        return self.links.get((i_node, j_node))


class NoiseModelTest(unittest.TestCase):
    def test_reverse_only_traffic_does_not_read_forward_travel_time(self):
        day_link = MockLink(
            1, 2, {"light": 0.0, "heavy": 0.0, "@kaltevuus": 0.0}
        )
        day_reverse_link = MockLink(
            2, 1, {"light": 10000.0, "heavy": 0.0}
        )
        day_link.reverse_link = day_reverse_link
        day_reverse_link.reverse_link = day_link

        morning_link = MockLink(
            1, 2, {"@kaltevuus": 0.0}, data2=50.0
        )
        morning_reverse_link = MockLink(
            2,
            1,
            {"@car_time_aht": 1.0, "@kaltevuus": 0.0},
            length=1.0,
            data2=50.0,
        )
        morning_link.reverse_link = morning_reverse_link
        morning_reverse_link.reverse_link = morning_link

        model = NoiseModel(
            MockNetwork((morning_link, morning_reverse_link)),
            ("light",),
            ("heavy",),
        )

        width = model.calc_noise(day_link)

        self.assertIsInstance(width, float)
        self.assertGreater(width, 0.0)

    def test_zero_traffic_has_no_noise_zone(self):
        link = MockLink(
            1,
            2,
            {"light": 0.0, "heavy": 0.0, "@kaltevuus": 0.0},
        )
        reverse_link = MockLink(
            2, 1, {"light": 0.0, "heavy": 0.0}
        )
        link.reverse_link = reverse_link

        model = NoiseModel(MockNetwork(()), ("light",), ("heavy",))

        self.assertEqual(model.calc_noise(link), 0.0)


if __name__ == "__main__":
    unittest.main()
