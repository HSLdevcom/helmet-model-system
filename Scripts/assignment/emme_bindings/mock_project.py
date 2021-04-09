from collections import namedtuple


class MockProject:
    def __init__(self):
        Modeller = namedtuple("Modeller", "emmebank")
        self.modeller = Modeller(EmmeBank())

    def create_matrix(*args, **kwargs):
        pass

    def create_extra_attribute(self, extra_attribute_type,
                               extra_attribute_name,
                               extra_attribute_description,
                               extra_attribute_default_value,
                               overwrite, scenario):
        network = scenario.get_network()
        if extra_attribute_type == "NODE":
            attr_dict = Node._extra_attr_template
        elif extra_attribute_type == "LINK":
            attr_dict = Link._extra_attr_template
        elif extra_attribute_type == "TRANSIT_LINE":
            attr_dict = TransitLine._extra_attr_template
        elif extra_attribute_type == "TRANSIT_SEGMENT":
            attr_dict = TransitSegment._extra_attr_template
        attr_dict[extra_attribute_name] = extra_attribute_default_value


class EmmeBank:
    def __init__(self):
        self._scenarios = {id: Scenario(id) for id in range(19, 24)}

    def scenario(self, id):
        return self._scenarios[id]

    def scenarios(self):
        return iter(self._scenarios.values())


class Scenario:
    def __init__(self, id):
        self.id = id
        self._network = Network()

    def get_network(self):
        return self._network

    def publish_network(self, network):
        self._network = network


class Network:
    def __init__(self):
        self._modes = {}
        self._nodes = {}
        self._links = {}
        self._transit_lines = {}

    def mode(self, id):
        return self._modes[id]

    def modes(self):
        return iter(self._modes.values())

    def node(self, id):
        return self._nodes[id]

    def link(self, i_node_id, j_node_id):
        return self._links[(i_node_id, j_node_id)]

    def links(self):
        return iter(self._links.values())

    def transit_line(self, id):
        return self._transit_lines[id]

    def transit_lines(self):
        return iter(self._transit_lines.values())


class Mode:
    def __init__(self, id):
        self.id = id


class NetworkObject:
    def __getitem__(self, key):
        return self._extra_attr[key]

    def __setitem__(self, key, value):
        self._extra_attr[key] = value


class Node(NetworkObject):
    _extra_attr_template = {}

    def __init__(self, id):
        self.id = id
        self._extra_attr = self._extra_attr_template.copy()


class Link(NetworkObject):
    _extra_attr_template = {}

    def __init__(self, i_node, j_node, length):
        self.i_node = i_node
        self.j_node = j_node
        self.length = length
        self.volume_delay_func = 0
        self._extra_attr = self._extra_attr_template.copy()
        self["@hinta"] = 0.0
        self._segments = []

    def segments(self):
        return iter(self._segments)


class TransitLine(NetworkObject):
    _extra_attr_template = {}

    def __init__(self, id, mode, headway):
        self.id = id
        self.mode = mode
        self.headway = headway
        self.data3 = 0
        self._segments = []

    def segment(self, id):
        return self._segments[id]

    def segments(self):
        return iter(self._segments)


class TransitSegment:
    _extra_attr_template = {}

    def __init__(self, line, link):
        self.line = line
        self.link = link
        link._segments.append(self)
