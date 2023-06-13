import unittest, os, pandas
from assignment.emme_bindings.mock_project import MockProject
from assignment.datatypes.transit_fare import TransitFareZoneSpecification
from utils.validate_network import validate
import copy

MODE_TYPES = {
    "1": "AUTO",
    "2": "TRANSIT",
    "3": "AUX_TRANSIT",
    "4": "AUX_AUTO",
}

class EmmeAssignmentTest(unittest.TestCase):
    def test_assignment(self):
        context = MockProject()
        scenario_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "..", "test_data", "Network")
        scenario_id = 19
        context.import_scenario(scenario_dir, scenario_id, "test")
        fares = TransitFareZoneSpecification(pandas.DataFrame({
            "fare": {
                "A": 59,
                "AB": 109,
                "dist": 3.0,
                "start": 35,
            },
        }))
        network0 = context.modeller.emmebank.scenario(scenario_id).get_network()

        #Mode check
        network1 = copy.deepcopy(network0)
        network1.create_mode(MODE_TYPES["3"],"h")
        self.assertRaises(ValueError, validate,
            network1,
            fares)
        
        #Link check, link type should not be one
        network2 = copy.deepcopy(network0)
        node1 = network2.create_node(800900, False)
        node2 = network2.create_node(800901, False)
        link = network2.create_link(800900, 800901, "haf")
        #Check if link type equals 1
        link.type = 1
        link.length = 1.0
        self.assertRaises(ValueError, validate,
            network2,
            fares)
        
        #Link check, link modes must be h at minimum
        network3 = copy.deepcopy(network0)
        node1 = network3.create_node(800902, False)
        node2 = network3.create_node(800903, False)
        link2 = network3.create_link(800902, 800903, "")
        link2.type = 142
        link2.length = 1.0

        self.assertRaises(ValueError, validate,
            network3,
            fares)
        
        #Link check, link modes must be h at minimum
        network4 = copy.deepcopy(network0)
        node1 = network4.create_node(800904, False)
        node2 = network4.create_node(800905, False)
        link3 = network4.create_link(800904, 800905, "h")
        link3.type = 142
        link3.length = 1.0

        self.assertRaises(ValueError, validate,
            network4,
            fares)
        
        #Link check, if link type is not 70 (vaihtokävely), then length must not be zero
        network5 = copy.deepcopy(network0)
        node1 = network5.create_node(800906, False)
        node2 = network5.create_node(800907, False)
        link4 = network5.create_link(800906, 800907, "haf")
        link4.type = 142
        link4.length = 0.0

        self.assertRaises(ValueError, validate,
            network5,
            fares)

        #Link check, link should not have only mode h, because it is removed later during the assignment
        network6 = copy.deepcopy(network0)
        node1 = network6.create_node(800909, False)
        node2 = network6.create_node(800910, False)
        link5 = network6.create_link(800909, 800910, "h")
        link5.type = 142
        link5.length = 1.0

        self.assertRaises(ValueError, validate,
            network6,
            fares)
        
        #Link check, link should not have type 100
        network7 = copy.deepcopy(network0)
        node1 = network7.create_node(800911, False)
        node2 = network7.create_node(800912, False)
        link6 = network7.create_link(800911, 800912, "haf")
        link6.type = 100
        link6.length = 1.0

        self.assertRaises(ValueError, validate,
            network7,
            fares)
        
        #Link check, link should not have type 999
        network8 = copy.deepcopy(network0)
        node1 = network8.create_node(800913, False)
        node2 = network8.create_node(800914, False)
        link7 = network8.create_link(800913, 800914, "haf")
        link7.type = 999
        link7.length = 1.0

        self.assertRaises(ValueError, validate,
            network8,
            fares)
        
        #Link check, link must not directly connect two centroids
        network9 = copy.deepcopy(network0)
        node1 = network9.create_node(800915, True)
        node2 = network9.create_node(800916, True)
        link8 = network9.create_link(800915, 800916, "haf")
        link8.type = 142
        link8.length = 1.0

        self.assertRaises(ValueError, validate,
            network9,
            fares)

        
if __name__ == "__main__":
    EmmeAssignmentTest().test_assignment()
        
