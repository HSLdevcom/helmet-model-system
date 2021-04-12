import numpy
from collections import namedtuple


class MockProject:
    path = "c:\\xxx\\yyy"

    def __init__(self):
        self.modeller = Modeller(EmmeBank())

    def create_matrix(self, matrix_id, matrix_name, matrix_description,
                      default_value, overwrite):
        dimension = len(next(self.modeller.emmebank.scenarios()).zone_numbers)
        self.modeller.emmebank._matrices[matrix_id] = Matrix(
            matrix_id, dimension, default_value)

    def create_extra_attribute(self, extra_attribute_type,
                               extra_attribute_name,
                               extra_attribute_description,
                               extra_attribute_default_value,
                               overwrite, scenario):
        scenario.create_extra_attribute(
            extra_attribute_type, extra_attribute_name,
            extra_attribute_default_value)

    def copy_matrix(*args, **kwargs):
        pass

    def network_calc(*args, **kwargs):
        pass

    def process_functions(*args, **kwargs):
        pass

    def car_assignment(*args, **kwargs):
        report = {
            "stopping_criterion": "MAX_ITERATIONS",
            "iterations": [{"number": 1}],
        }
        return report

    def bike_assignment(*args, **kwargs):
        pass

    def pedestrian_assignment(*args, **kwargs):
        pass

    def transit_assignment(*args, **kwargs):
        pass

    def congested_assignment(*args, **kwargs):
        report = {
            "stopping_criterion": "MAX_ITERATIONS",
            "iterations": [{"number": 1}],
        }
        return report

    def matrix_results(self, *args, **kwargs):
        pass

    def network_results(self, *args, **kwargs):
        pass


Modeller = namedtuple("Modeller", "emmebank")


class EmmeBank:
    def __init__(self):
        self._scenarios = {idx: Scenario(idx) for idx in range(19, 24)}
        self._matrices = {}

    def scenario(self, idx):
        return self._scenarios[idx]

    def scenarios(self):
        return iter(self._scenarios.values())

    def matrix(self, idx):
        return self._matrices[idx]


class Scenario:
    def __init__(self, idx):
        self.id = idx
        self._network = Network()

    @property
    def zone_numbers(self):
        return sorted(self._network._centroids)

    def create_extra_attribute(self, attr_type, idx, default_value=0):
        network = self.get_network()
        network._extra_attr[attr_type][idx] = default_value
        for obj in network._objects[attr_type]():
            obj._extra_attr[idx] = default_value

    def get_network(self):
        return self._network

    def publish_network(self, network):
        self._network = network


class Matrix:
    def __init__(self, idx, dim, default_value):
        self.id = idx
        self._data = numpy.full((dim, dim), default_value, dtype=float)

    def get_numpy_data(self):
        return self._data

    def set_numpy_data(self, data):
        self._data[:,:] = data


class Network:
    def __init__(self):
        self._modes = {}
        self._nodes = {}
        self._centroids = {}
        self._regular_nodes = {}
        self._links = {}
        self._vehicles = {}
        self._lines = {}
        self._segments = []
        self._objects = {
            "NODE": self.nodes,
            "LINK": self.links,
            "TRANSIT_LINE": self.transit_lines,
            "TRANSIT_SEGMENT": self.transit_segments,
        }
        self._extra_attr = {attr_type: {} for attr_type in self._objects}

    def mode(self, idx):
        return self._modes[idx]

    def create_mode(self, idx):
        self._modes[idx] = Mode(idx)

    def modes(self):
        return iter(self._modes.values())

    def node(self, idx):
        return self._nodes[idx]

    def nodes(self):
        return iter(self._nodes.values())

    def centroids(self):
        return iter(self._centroids.values())

    def regular_nodes(self):
        return iter(self._regular_nodes.values())

    def create_node(self, idx, is_centroid=False):
        node = Node(self, idx, is_centroid)
        self._nodes[idx] = node
        if is_centroid:
            self._centroids[idx] = node
        else:
            self._regular_nodes[idx] = node

    def link(self, i_node_id, j_node_id):
        idx = "{}-{}".format(i_node_id, j_node_id)
        return self._links[idx]

    def links(self):
        return iter(self._links.values())

    def create_link(self, i_node_id, j_node_id):
        # TODO Add modes
        idx = "{}-{}".format(i_node_id, j_node_id)
        self._links[idx] = Link(
            self, self.node(i_node_id), self.node(j_node_id))

    def transit_vehicle(self, idx):
        return self._vehicles[idx]

    def create_transit_vehicle(self, idx, mode_id):
        self._vehicles[idx] = TransitVehicle(idx, self.mode(mode_id))

    def transit_line(self, idx):
        return self._lines[idx]

    def transit_lines(self):
        return iter(self._lines.values())

    def transit_segments(self):
        return iter(self._segments)

    def create_transit_line(self, idx, transit_vehicle_id, itinerary):
        line = TransitLine(
                    self, idx, self.transit_vehicle(transit_vehicle_id))
        self._lines[idx] = line
        for i in range(len(itinerary) - 1):
            link = self.link(itinerary[i], itinerary[i + 1])
            segment = TransitSegment(self, line, link)
            self._segments.append(segment)
            line._segments.append(segment)
            link._segments.append(segment)


class Mode:
    def __init__(self, idx):
        self.id = idx


class TransitVehicle:
    def __init__(self, idx, mode):
        self.number = idx
        self.mode = mode

    @property
    def id(self):
        return str(self.number)


class NetworkObject:
    def __init__(self):
        self._extra_attr = {}
        self.id = None

    def __getitem__(self, key):
        if key in self._extra_attr:
            return self._extra_attr[key]
        else:
            return self.__dict__[key]

    def __setitem__(self, key, value):
        if key in self._extra_attr:
            self._extra_attr[key] = value
        elif key in self.__dict__:
            self.__dict__[key] = value
        else:
            raise KeyError()

    def __str__(self):
        return self.id


class Node(NetworkObject):
    def __init__(self, network, idx, is_centroid=False):
        self.network = network
        self.is_centroid = is_centroid
        self.number = idx
        self.label = ""
        self.data1 = 0.0
        self.data2 = 0.0
        self.data3 = 0.0
        self._extra_attr = network._extra_attr["NODE"].copy()

    @property
    def id(self):
        return str(self.number)


class Link(NetworkObject):
    def __init__(self, network, i_node, j_node):
        self.network = network
        self.i_node = i_node
        self.j_node = j_node
        self.length = 0
        self.volume_delay_func = 0
        self.data1 = 0.0
        self.data2 = 0.0
        self.data3 = 0.0
        self.auto_time = 0.1
        self._extra_attr = network._extra_attr["LINK"].copy()
        self._extra_attr["@hinta"] = 0.0
        self._segments = []

    @property
    def id(self):
        return "{}-{}".format(self.i_node, self.j_node)

    @property
    def reverse_link(self):
        try:
            return self.network.link(self.j_node, self.i_node)
        except KeyError:
            return None

    def segments(self):
        return iter(self._segments)


class TransitLine(NetworkObject):
    def __init__(self, network, idx, vehicle):
        self.network = network
        self.id = idx
        self.vehicle = vehicle
        self.headway = 9999
        self.data3 = 0.0
        self._extra_attr = network._extra_attr["TRANSIT_LINE"].copy()
        self._segments = []

    @property
    def mode(self):
        return self.vehicle.mode

    def segment(self, idx):
        return self._segments[idx]

    def segments(self):
        return iter(self._segments)


class TransitSegment(NetworkObject):
    def __init__(self, network, line, link):
        self.network = network
        self.line = line
        self.link = link
        self.transit_time_func = 0
        self._extra_attr = network._extra_attr["TRANSIT_SEGMENT"].copy()
        self._extra_attr["@base_timtr"] = 0.0

    @property
    def id(self):
        return "{}-{}".format(self.line, self.link)

    @property
    def i_node(self):
        return self.link.i_node

    @property
    def j_node(self):
        return self.link.j_node
