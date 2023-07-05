from argparse import ArgumentTypeError
import unittest, os, pandas
from assignment.emme_bindings.mock_project import MockProject
from assignment.datatypes.transit_fare import TransitFareZoneSpecification
from assignment.mock_assignment import MockAssignmentModel
from datahandling.matrixdata import MatrixData
from utils.validate_network import validate
import parameters.assignment as param
import parameters.zone as zone_param
import copy

MODE_TYPES = {
    "1": "AUTO",
    "2": "TRANSIT",
    "3": "AUX_TRANSIT",
    "4": "AUX_AUTO",
}

time_periods = ("aht", "pt", "iht")

def add_bus_stops(network):
    for line in network.transit_lines():
        if line.mode.id in param.stop_codes:
            stop_codes = param.stop_codes[line.mode.id]
            for segment in line.segments():
                is_stop = segment.i_node.data2 in stop_codes
                if line.mode.id in "de":
                    # Non-HSL bus lines
                    not_hsl = segment.i_node.label not in param.hsl_area
                    if line.id[-1] == '1':
                        # Line starts in HSL area
                        segment.allow_alightings = not_hsl and is_stop
                        segment.allow_boardings = is_stop
                    elif line.id[-1] == '2':
                        # Line ends in HSL area
                        segment.allow_alightings = is_stop
                        segment.allow_boardings = not_hsl and is_stop
                    else:
                        raise ValueError(
                            "Unknown direction code for line " + line.id)
                else:
                    segment.allow_alightings = is_stop
                    segment.allow_boardings = is_stop

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

        # mock_result_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
        #     "..", "test_data", "Results","test")
        #ass_model = MockAssignmentModel(MatrixData(mock_result_path))
        network0 = context.modeller.emmebank.scenario(scenario_id).get_network()
        #ass_model.prepare_network(network = network0) #the number is the car cost per km

        #Mode check
        network1 = copy.deepcopy(network0)
        network1.create_mode(MODE_TYPES["3"],"h")
        self.assertRaises(ValueError, validate,
            network1,
            fares)
        
        #Link check cases
        cases = [#Link check, link type should not be one
                {"node1_centroid":False,
                  "node2_centroid":False,
                  "link_modes":"haf",
                  "link_type":1,
                  "link_length":1.0},
                #Link check, link modes must not be empty
                {"node1_centroid":False,
                  "node2_centroid":False,
                  "link_modes":"",
                  "link_type":142,
                  "link_length":1.0},
                #Link check, link modes must not be just h
                {"node1_centroid":False,
                  "node2_centroid":False,
                  "link_modes":"h",
                  "link_type":142,
                  "link_length":1.0},
                #Link check, if link type is not 70 (vaihtokävely), then length must not be zero
                {"node1_centroid":False,
                  "node2_centroid":False,
                  "link_modes":"haf",
                  "link_type":142,
                  "link_length":0},
                #Link check, link should not have type 100
                {"node1_centroid":False,
                  "node2_centroid":False,
                  "link_modes":"haf",
                  "link_type":100,
                  "link_length":1.0},
                #Link check, link should not have type 999
                {"node1_centroid":False,
                  "node2_centroid":False,
                  "link_modes":"haf",
                  "link_type":999,
                  "link_length":1.0},
                #Link check, link must not directly connect two centroids
                {"node1_centroid":True,
                  "node2_centroid":True,
                  "link_modes":"haf",
                  "link_type":142,
                  "link_length":1.0},
                  ]
        node1_id = 800900
        node2_id = 800901
        for case in cases:
            self.link_check_network(network0, fares, 
                    node1_id, case["node1_centroid"], 
                    node2_id, case["node2_centroid"], 
                    case["link_modes"],
                    case["link_type"],
                    case["link_length"])
    
        #Link check, link must have VDF if car link
        network = copy.deepcopy(network0)
        node1 = network.create_node(node1_id, False)
        node2 = network.create_node(node2_id, False)
        link = network.create_link(node1_id, node2_id, "hc")
        #Check if link type equals 1
        link.type = 142
        link.length = 1.0
        link.volume_delay_func = 0
        self.assertRaises(ValueError, validate,
            network,
            fares)   

        #Link check, tram link must have right AHT speed
        network = copy.deepcopy(network0)
        node1 = network.create_node(node1_id, False)
        node2 = network.create_node(node2_id, False)
        link = network.create_link(node1_id, node2_id, "pt")
        #Check if link type equals 1
        link.type = 2
        link.length = 1.0
        link.data1 = 1122 #meaning 001122 - aappii format, refer to network description
        self.assertRaises(ValueError, validate,
            network,
            fares)  
        
        #Link check, tram link must have right PT speed
        network = copy.deepcopy(network0)
        node1 = network.create_node(node1_id, False)
        node2 = network.create_node(node2_id, False)
        link = network.create_link(node1_id, node2_id, "pt")
        #Check if link type equals 1
        link.type = 2
        link.length = 1.0
        link.data1 = 220022
        self.assertRaises(ValueError, validate,
            network,
            fares)  
        
        #Link check, tram link must have right IHT speed
        network = copy.deepcopy(network0)
        node1 = network.create_node(node1_id, False)
        node2 = network.create_node(node2_id, False)
        link = network.create_link(node1_id, node2_id, "pt")
        #Check if link type equals 1
        link.type = 2
        link.length = 1.0
        link.data1 = 221100
        self.assertRaises(ValueError, validate,
            network,
            fares) 
        
        #Segment check, train or metro travel time us1=0 before stopping (noalin=0 or noboan=0)
        # Check line encoding, if row's @ccost=1
        network = copy.deepcopy(network0)
        itinerary = []
        itinerary.append("802113")
        itinerary.append("802114")
        itinerary.append("802115")
        line = network.create_transit_line(
                            '10101a', 7, itinerary)
        hdw_attrs = [f"@hw_{tp}" for tp in time_periods]
        for hdwy in hdw_attrs:
            line[hdwy] = 5.0
        line._segments[0].data1 = 0
        add_bus_stops(network)
        line._segments[1].noboa = 0
        # self.assertRaises(ValueError, validate,
        #     network,
        #     fares) 

        #NOT FINISHED!!!
        #NOBOA and NOALI only available after prepare_network function is run
        #NOBOAN is the NOBOA of the next segment

        #Line check, headway should not be 0,1
        network = copy.deepcopy(network0)
        itinerary = []
        itinerary.append("802113")
        itinerary.append("802114")
        line = network.create_transit_line(
                            '10101b', 7, itinerary)
        hdw_attrs = [f"@hw_{tp}" for tp in time_periods]
        for hdwy in hdw_attrs:
            line[hdwy] = 0.001
        self.assertRaises(ValueError, validate,
            network,
            fares) 
        

        
    def link_check_network(self, network0, fares, node1_id, 
                           node1_iscentroid, node2_id, node2_iscentroid, 
                           link_modes, link_type, link_length):

        network = copy.deepcopy(network0)
        node1 = network.create_node(node1_id, node1_iscentroid)
        node2 = network.create_node(node2_id, node2_iscentroid)
        link = network.create_link(node1_id, node2_id, link_modes)
        #Check if link type equals 1
        link.type = link_type
        link.length = link_length
        self.assertRaises(ValueError, validate,
            network,
            fares)

        
if __name__ == "__main__":
    EmmeAssignmentTest().test_assignment()
        
