import numpy
from collections import namedtuple


class MockProject:
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
        extra_attr = scenario.get_network()._extra_attr[extra_attribute_type]
        extra_attr[extra_attribute_name] = extra_attribute_default_value

    def matrix_results(self, *args, **kwargs):
        pass

    def transit_assignment(self, *args, **kwargs):
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

    def get_network(self):
        return self._network

    def publish_network(self, network):
        self._network = network


class Matrix:
    def __init__(self, idx, dim, default_value):
        self.id = idx
        self._data = numpy.full((dim, dim), default_value)

    def get_numpy_data(self):
        return self._data

    def set_numpy_data(self, data):
        self._data[:,:] = data


class Network:
    def __init__(self):
        self._modes = {}
        self._nodes = {}
        self._centroids = {}
        self._links = {}
        self._transit_lines = {}
        self._extra_attr = {
            "NODE": {},
            "LINK": {},
            "TRANSIT_LINE": {},
            "TRANSIT_SEGMENT": {},
        }

    def mode(self, idx):
        return self._modes[idx]

    def modes(self):
        return iter(self._modes.values())

    def node(self, idx):
        return self._nodes[idx]

    def nodes(self):
        return iter(self._nodes.values())

    def centroids(self):
        return iter(self._centroids.values())

    def create_node(self, idx, is_centroid=False):
        node = Node(self, idx, is_centroid)
        self._nodes[idx] = node
        if is_centroid:
            self._centroids[idx] = node

    def link(self, i_node_id, j_node_id):
        return self._links[(i_node_id, j_node_id)]

    def links(self):
        return iter(self._links.values())

    def transit_line(self, idx):
        return self._transit_lines[idx]

    def transit_lines(self):
        return iter(self._transit_lines.values())


class Mode:
    def __init__(self, idx):
        self.id = idx


class NetworkObject:
    def __init__(self):
        self._extra_attr = {}

    def __getitem__(self, key):
        return self._extra_attr[key]

    def __setitem__(self, key, value):
        self._extra_attr[key] = value


class Node(NetworkObject):
    def __init__(self, network, idx, is_centroid=False):
        self.network = network
        self.is_centroid = is_centroid
        self.id = str(idx)
        self.number = idx
        self.label = ""
        self.data1 = 0
        self._extra_attr = network._extra_attr["NODE"].copy()


class Link(NetworkObject):
    def __init__(self, network, i_node, j_node, length):
        self.network = network
        self.id = "{}-{}".format(i_node, j_node)
        self.i_node = network.node(i_node)
        self.j_node = network.node(j_node)
        self.length = length
        self.volume_delay_func = 0
        self._extra_attr = network._extra_attr["LINK"].copy()
        self["@hinta"] = 0.0
        self._segments = []

    def segments(self):
        return iter(self._segments)


class TransitLine(NetworkObject):
    def __init__(self, network, idx, mode, headway):
        self.network = network
        self.id = idx
        self.mode = mode
        self.headway = headway
        self.data3 = 0
        self._extra_attr = network._extra_attr["TRANSIT_LINE"].copy()
        self._segments = []

    def segment(self, idx):
        return self._segments[idx]

    def segments(self):
        return iter(self._segments)


class TransitSegment:
    def __init__(self, network, line, link):
        self.network = network
        self.line = line
        self.link = link
        self._extra_attr = network._extra_attr["TRANSIT_SEGMENT"].copy()
        line._segments.append(self)
        link._segments.append(self)
