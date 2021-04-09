from collections import namedtuple


class MockProject:
    def __init__(self):
        Modeller = namedtuple("Modeller", "emmebank")
        self.modeller = Modeller(EmmeBank())

    def create_matrix(*args, **kwargs):
        pass

    def create_extra_attribute(*args, **kwargs):
        pass


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
        self._modes = {id: Mode(id) for id in ('c', 'b')}
        self._nodes = {id: Node(id) for id in range(1, 5)}
        self._links = {}
        link = (1, 2)
        self._links[link] = Link(*link)
        self._transit_lines = {id: TransitLine(id, self.mode('b'))
            for id in range(1, 4)}
        line = self.transit_line(1)
        line._segments.append(TransitSegment(line, self.link(*link)))

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


class Node:
    def __init__(self, id):
        self.id = id


class Link:
    def __init__(self, i_node, j_node):
        self.i_node = i_node
        self.j_node = j_node
        self.length = 3.5
        self.volume_delay_func = 1
        self._extra_attr = {
            "@truck": 5.0,
            "@trailer_truck": 3.0,
            "@hinta": 0.0,
        }
        self._segments = []

    def __getitem__(self, key):
        return self._extra_attr[key]

    def __setitem__(self, key, value):
        self._extra_attr[key] = value

    def segments(self):
        return iter(self._segments)


class TransitLine:
    def __init__(self, id, mode):
        self.id = id
        self.mode = mode
        self.headway = 5
        self.data3 = 0
        self._segments = []

    def segment(self, id):
        return self._segments[id]

    def segments(self):
        return iter(self._segments)


class TransitSegment:
    def __init__(self, line, link):
        self.line = line
        self.link = link
        link._segments.append(self)
