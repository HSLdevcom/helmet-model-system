from __future__ import annotations
from typing import Dict, Iterable, List, Optional, Tuple, Union
import numpy # type: ignore
from collections import namedtuple
import copy
import os


MODE_TYPES = {
    "1": "AUTO",
    "2": "TRANSIT",
    "3": "AUX_TRANSIT",
    "4": "AUX_AUTO",
}


class MockProject:
    """Mock-up version of `EmmeProject`.

    Emulates key features of EMME API, so that `EmmeAssignmentModel`
    and `AssignmentPeriod` can be unit tested without EMME binding.
    """
    def __init__(self):
        self.modeller = Modeller(EmmeBank())

    def copy_scenario(self, 
                      from_scenario, 
                      scenario_id: int, 
                      scenario_title: str,
                      overwrite: bool = False, 
                      copy_paths: bool = True, 
                      copy_strategies: bool = True):
        if overwrite:
            try:
                self.modeller.emmebank.delete_scenario(scenario_id)
            except KeyError:
                pass
        scenario = self.modeller.emmebank.copy_scenario(
            from_scenario.number, scenario_id)
        scenario.title = scenario_title
        return scenario

    def import_scenario(self, scenario_dir, scenario_id, scenario_title):
        scenario = self.modeller.emmebank.create_scenario(scenario_id)
        scenario.title = scenario_title
        for file_name in os.listdir(scenario_dir):
            if file_name.startswith("modes"):
                self.mode_transaction(
                    os.path.join(scenario_dir, file_name), scenario=scenario)
        for file_name in os.listdir(scenario_dir):
            if file_name.startswith("base_network"):
                self.base_network_transaction(
                    os.path.join(scenario_dir, file_name), scenario=scenario)
        for file_name in os.listdir(scenario_dir):
            if file_name.startswith("vehicles"):
                self.vehicle_transaction(
                    os.path.join(scenario_dir, file_name), scenario=scenario)
        for file_name in os.listdir(scenario_dir):
            if file_name.startswith("transit_lines"):
                self.transit_line_transaction(
                    os.path.join(scenario_dir, file_name), scenario=scenario)
        for file_name in os.listdir(scenario_dir):
            if file_name.startswith("extra"):
                self.import_extra_attributes(
                    os.path.join(scenario_dir, file_name), scenario=scenario)

    def create_matrix(self, 
                      matrix_id: int, 
                      matrix_name, 
                      matrix_description,
                      default_value=0, 
                      overwrite=False):
        try:
            mtx = self.modeller.emmebank.create_matrix(
                matrix_id, default_value)
        except ExistenceError:
            if overwrite:
                mtx = self.modeller.emmebank.matrix(matrix_id)
                mtx.set_numpy_data(default_value)
        mtx.name = matrix_name
        mtx.description = matrix_description

    def create_extra_attribute(self, 
                               extra_attribute_type: str,
                               extra_attribute_name: str,
                               extra_attribute_description: str,
                               extra_attribute_default_value: float = 0.0,
                               overwrite: bool = False, 
                               scenario: Optional[Scenario] = None):
        try:
            scenario.create_extra_attribute(
                extra_attribute_type, extra_attribute_name,
                extra_attribute_default_value)
        except ExistenceError:
            if overwrite:
                scenario.extra_attribute(extra_attribute_name).initialize(
                    extra_attribute_default_value)

    def copy_matrix(self, from_matrix, matrix_id, matrix_name,
                    matrix_description):
        self.create_matrix(matrix_id, matrix_name, matrix_description)
        eb = self.modeller.emmebank
        eb.matrix(matrix_id).set_numpy_data(
            eb.matrix(from_matrix).get_numpy_data())

    def mode_transaction(self, transaction_file, revert_on_error=True,
                         scenario=None):
        network = scenario.get_network()
        with open(transaction_file) as f:
            while True:
                if f.readline() == "t modes\n":
                    break
            while True:
                rec = f.readline().split("'")
                if len(rec) == 3:
                    rec = rec[0].split() + [rec[1]] + rec[2].split()
                elif len(rec) <= 1:
                    rec = rec[0].split()
                else:
                    raise SyntaxError("Extra single quotes (') found in mode table")
                if not rec:
                    break
                if rec[0] == "c":
                    pass
                elif rec[0] == "d":
                    # TODO Implement deletion
                    pass
                else:
                    if rec[0] == "a":
                        mode = network.create_mode(
                            mode_type=MODE_TYPES[rec[3]], idx=rec[1])
                    elif rec[0] == "m":
                        mode = network.mode(idx=rec[1])
                    else:
                        raise SyntaxError("Unknown update code")
                    mode.description = rec[2]

    def base_network_transaction(self, transaction_file, revert_on_error=True,
                                 scenario=None):
        network = scenario.get_network()
        with open(transaction_file) as f:
            while True:
                if f.readline() == "t nodes\n":
                    break
            while True:
                line = f.readline()
                if line == "t links\n":
                    break
                rec = line.split()
                if rec[0] == "c":
                    pass
                elif rec[0] == "d":
                    # TODO Implement deletion
                    pass
                else:
                    if rec[0] == "a":
                        node = network.create_node(rec[1], is_centroid=False)
                    elif rec[0] == "a*":
                        node = network.create_node(rec[1], is_centroid=True)
                    elif rec[0] == "m":
                        node = network.node(rec[1])
                    else:
                        raise SyntaxError("Unknown update code")
                    node.x = float(rec[2])
                    node.y = float(rec[3])
                    node.data1 = float(rec[4])
                    node.data2 = float(rec[5])
                    node.data3 = float(rec[6])
                    node.label = rec[7]
            while True:
                rec = f.readline().split()
                if not rec:
                    break
                if rec[0] == "c":
                    pass
                elif rec[0] == "d":
                    # TODO Implement deletion
                    pass
                else:
                    if rec[0] == "a":
                        link = network.create_link(
                            i_node_id=rec[1], j_node_id=rec[2], modes=rec[4])
                    elif rec[0] == "m":
                        link = network.link(
                            i_node_id=rec[1], j_node_id=rec[2])
                    else:
                        raise SyntaxError("Unknown update code")
                    link.length = float(rec[3])
                    link.type = int(rec[5])
                    link.num_lanes = float(rec[6])
                    link.volume_delay_func = int(rec[7])
                    link.data1 = float(rec[8])
                    link.data2 = float(rec[9])
                    link.data3 = float(rec[10])

    def vehicle_transaction(self, transaction_file, revert_on_error=True,
                            scenario=None):
        network = scenario.get_network()
        with open(transaction_file) as f:
            while True:
                if f.readline() == "t vehicles\n":
                    break
            while True:
                rec = f.readline().split()
                if not rec:
                    break
                if rec[0] == "c":
                    pass
                elif rec[0] == "d":
                    # TODO Implement deletion
                    pass
                else:
                    if rec[0] == "a":
                        vehicle = network.create_transit_vehicle(
                            idx=int(rec[1]), mode_id=rec[3])
                    elif rec[0] == "m":
                        vehicle = network.transit_vehicle(idx=int(rec[1]))
                    else:
                        raise SyntaxError("Unknown update code")
                    vehicle.description = rec[2][1:-1]

    def transit_line_transaction(self, transaction_file, revert_on_error=True,
                            scenario=None):
        network = scenario.get_network()
        with open(transaction_file) as f:
            while True:
                if f.readline() == "t lines\n":
                    break
            rec = f.readline().replace("'", " ").split()
            while True:
                if not rec:
                    break
                if rec[0] == "c":
                    rec = f.readline().replace("'", " ").split()
                elif rec[0] == "d":
                    # TODO Implement deletion
                    rec = f.readline().replace("'", " ").split()
                else:
                    if rec[0] == "a":
                        line_id = rec[1]
                        vehicle_id = int(rec[3])
                        headway = float(rec[4])
                        itinerary = []
                        segment_data = []
                        while True:
                            segrec = f.readline().replace("'", " ").split()
                            if not segrec or segrec[0] in "amd":
                                rec = segrec
                                break
                            elif segrec[0] not in ("c", "path=no"):
                                itinerary.append(segrec[0])
                                try:
                                    symbol = segrec[1][4]
                                    segment_data.append({
                                        "allow_alightings": symbol in ">+",
                                        "allow_boardings": symbol in "<+",
                                        "transit_time_func": int(segrec[2][4:]),
                                        "data1": float(segrec[3][4:]),
                                        "data2": float(segrec[4][4:]),
                                        "data3": float(segrec[5][4:]),
                                    })
                                except IndexError:
                                    pass
                        line = network.create_transit_line(
                            line_id, vehicle_id, itinerary)
                        for data, segment in zip(segment_data, line.segments()):
                            segment.__dict__.update(data)
                    elif rec[0] == "m":
                        line = network.transit_line(idx=rec[1])
                        vehicle_id = int(rec[3])
                        headway = float(rec[4])
                    else:
                        raise SyntaxError("Unknown update code")
                    line.vehicle = vehicle_id
                    line.headway = headway

    def import_extra_attributes(self, file_path, revert_on_error=True,
                                scenario=None, import_definitions=False):
        with open(file_path) as f:
            f.readline()
            while True:
                rec = f.readline().split()
                if rec[0] == "end":
                    break
                attr_type = rec[1]
                self.create_extra_attribute(
                    attr_type, rec[0], "",
                    extra_attribute_default_value=float(rec[2]),
                    overwrite=True, scenario=scenario)
            header = f.readline().split()
            network = scenario.get_network()
            while True:
                rec = f.readline().replace("'", " ").split()
                if not rec:
                    break
                elif attr_type == "NODE":
                    node = network.node(int(rec[0]))
                    for i, attr in enumerate(header[1:], 1):
                        node[attr] = float(rec[i])
                elif attr_type == "LINK":
                    link = network.link(int(rec[0]), int(rec[1]))
                    for i, attr in enumerate(header[2:], 2):
                        link[attr] = float(rec[i])
                elif attr_type == "TRANSIT_LINE":
                    line = network.transit_line(rec[0])
                    for i, attr in enumerate(header[1:], 1):
                        line[attr] = float(rec[i])
                elif attr_type == "TRANSIT_SEGMENT":
                    link = network.link(int(rec[1]), int(rec[2]))
                    for segment in link.segments():
                        if segment.line.id == rec[0]:
                            break
                    else:
                        raise ExistenceError()
                    for i, attr in enumerate(header[3:], 3):
                        segment[attr] = float(rec[i])

    def network_calc(self, *args, **kwargs):
        pass

    def car_assignment(self, *args, **kwargs):
        report = {
            "stopping_criterion": "MAX_ITERATIONS",
            "iterations": [{"number": 1}],
        }
        return report

    def bike_assignment(self, *args, **kwargs):
        pass

    def pedestrian_assignment(self, *args, **kwargs):
        pass

    def transit_assignment(self, *args, **kwargs):
        pass

    def congested_assignment(self, transit_assignment_spec, class_names,
                             congestion_function, stopping_criteria,
                             log_worksheets, scenario, save_strategies):
        self.create_extra_attribute(
            "TRANSIT_SEGMENT", "@base_timtr", "", 1.0,
            overwrite=True, scenario=scenario)
        report = {
            "stopping_criteria": "MAX_ITERATIONS",
            "iterations": [{"number": 1}],
        }
        return report

    def matrix_results(self, *args, **kwargs):
        pass

    def network_results(self, *args, **kwargs):
        pass

    def create_extra_function_parameters(self, *args, **kwargs):
        pass


Modeller = namedtuple("Modeller", "emmebank")


class EmmeBank:
    def __init__(self):
        self._scenarios = {}
        self._matrices = {}
        self._functions = {}

    def scenario(self, idx: int):
        if idx in self._scenarios:
            return self._scenarios[idx]

    def scenarios(self):
        return iter(self._scenarios.values())

    def create_scenario(self, idx: int):
        if idx in self._scenarios:
            raise ExistenceError("Scenario already exists: {}".format(idx))
        else:
            scenario = Scenario(idx)
            self._scenarios[idx] = scenario
            return scenario

    def copy_scenario(self, source_id: int, destination_id: int):
        if self.scenario(source_id) is None:
            raise ExistenceError("Scenario does not exist: {}".format(
                source_id))
        else:
            dest = self.create_scenario(destination_id)
            dest.publish_network(
                copy.deepcopy(self.scenario(source_id).get_network()))
            return dest

    def delete_scenario(self, idx: int):
        del self._scenarios[idx]

    def matrix(self, idx: int):
        if idx in self._matrices:
            return self._matrices[idx]

    def create_matrix(self, idx: int, default_value=0.0):
        if idx in self._matrices:
            raise ExistenceError("Matrix already exists: {}".format(idx))
        else:
            matrix = Matrix(
                idx, len(next(self.scenarios()).zone_numbers), default_value)
            self._matrices[idx] = matrix
            return matrix

    def function(self, idx: int):
        if idx in self._functions:
            return self._functions[idx]

    def functions(self):
        return iter(self._functions.values())

    def create_function(self, idx: int, expression: Dict[str,str]):
        if idx in self._functions:
            raise ExistenceError("Function already exists: {}".format(idx))
        else:
            func = Function(idx, expression)
            self._functions[idx] = func
            return func

    def delete_function(self, idx: int):
        try:
            del self._functions[idx]
        except KeyError:
            raise ExistenceError("Function does not exist: {}".format(idx))


class Scenario:
    def __init__(self, idx: int):
        self.id = str(idx)
        self.number = int(idx)
        self.title = ""
        self._network = Network()

    @property
    def zone_numbers(self):
        return sorted(self._network._centroids)

    def extra_attribute(self, idx: int):
        network = self.get_network()
        for attr_type in network._extra_attr:
            if idx in network._extra_attr[attr_type]:
                return network._extra_attr[attr_type][idx]

    def create_extra_attribute(self, 
                               attr_type, 
                               idx: int, 
                               default_value: float=0.0):
        network = self.get_network()
        if idx in network._extra_attr[attr_type]:
            raise ExistenceError("Extra attribute already exists: {}".format(
                idx))
        else:
            network._extra_attr[attr_type][idx] = ExtraAttribute(
                idx, attr_type, default_value, self)
            for obj in network._objects[attr_type]():
                obj._extra_attr[idx] = default_value

    def get_network(self):
        return self._network

    def publish_network(self, network):
        self._network = network


class ExtraAttribute:
    def __init__(self, name, attr_type, default_value, scenario):
        if len(name) > 20 or name[0] != '@':
            raise ArgumentError("Invalid extra attribute ID: {}".format(name))
        self.name = name
        self.type = attr_type
        self.default_value = default_value
        self.scenario = scenario

    def initialize(self, value=0.0):
        self.default_value = value
        network = self.scenario.get_network()
        for obj in network._objects[self.type]():
            obj[self.name] = value


class Matrix:
    def __init__(self, idx: int, dim: int, default_value: Union[int, float]):
        self.id = idx
        self._data = numpy.full((dim, dim), default_value, dtype=float)
        self._name = ""
        self._description = ""

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, matrix_name):
        if len(matrix_name) > 40:
            raise ArgumentError(
                "matrix_name: expected a string with maximum length 40")
        else:
            self._name = matrix_name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, matrix_description):
        if len(matrix_description) > 80:
            raise ArgumentError(
                "matrix_description: expected a string with maximum length 80")
        else:
            self._description = matrix_description

    def get_numpy_data(self, scenario_id: Optional[int]=None):
        return self._data

    def set_numpy_data(self, data, scenario_id: Optional[int]=None):
        self._data[:,:] = data


class Function:
    def __init__(self, idx: int, expression: Dict[str,str]):
        self.id = idx
        self.expression = expression


class Network:
    def __init__(self):
        self._modes = {}
        self._nodes = {}
        self._centroids = {}
        self._regular_nodes = {}
        self._links = {}
        self._vehicles = {}
        self._lines = {}
        self._objects = {
            "NODE": self.nodes,
            "LINK": self.links,
            "TRANSIT_LINE": self.transit_lines,
            "TRANSIT_SEGMENT": self.transit_segments,
        }
        self._extra_attr = {attr_type: {} for attr_type in self._objects}

    def mode(self, idx: int) -> 'Mode':
        if idx in self._modes:
            return self._modes[idx]

    def modes(self) -> Iterable:
        return iter(self._modes.values())

    def create_mode(self, mode_type: str, idx: str) -> 'Mode':
        if not isinstance(idx, str) or len(idx) != 1:
            raise Exception("Invalid mode ID: " + idx)
        mode = Mode(idx, mode_type)
        self._modes[idx] = mode
        return mode

    def node(self, idx: int) -> 'Node':
        idx = int(idx)
        if idx in self._nodes:
            return self._nodes[idx]

    def nodes(self) -> Iterable:
        return iter(self._nodes.values())

    def centroids(self) -> Iterable:
        return iter(self._centroids.values())

    def regular_nodes(self) -> Iterable:
        return iter(self._regular_nodes.values())

    def create_node(self, idx: int, is_centroid: bool) -> 'Node':
        idx = int(idx)
        node = Node(self, idx, is_centroid)
        self._nodes[idx] = node
        if is_centroid:
            self._centroids[idx] = node
        else:
            self._regular_nodes[idx] = node
        return node

    def link(self, i_node_id: int, j_node_id: int) -> 'Link':
        idx = "{}-{}".format(i_node_id, j_node_id)
        if idx in self._links:
            return self._links[idx]

    def links(self) -> Iterable:
        return iter(self._links.values())

    def create_link(self, i_node_id: int, j_node_id: int, modes: str) -> 'Link':
        modes = [self.mode(str(mode)) for mode in modes]
        link = Link(
            self, self._nodes[int(i_node_id)], self._nodes[int(j_node_id)],
            modes)
        self._links["{}-{}".format(i_node_id, j_node_id)] = link
        return link

    def transit_vehicle(self, idx: int) -> 'TransitVehicle':
        if idx in self._vehicles:
            return self._vehicles[idx]

    def transit_vehicles(self) -> Iterable:
        return iter(self._vehicles.values())

    def create_transit_vehicle(self, idx: int, mode_id: str) -> 'TransitVehicle':
        vehicle = TransitVehicle(idx, self.mode(mode_id))
        self._vehicles[idx] = vehicle
        return vehicle

    def transit_line(self, idx) -> 'TransitLine':
        if idx in self._lines:
            return self._lines[idx]

    def transit_lines(self) -> Iterable['TransitLine']:
        return iter(self._lines.values())

    def transit_segments(self, include_hidden=False) -> Tuple['Segment']:
        return (segment for line in self.transit_lines()
            for segment in line.segments(include_hidden))

    def create_transit_line(self, idx: str, transit_vehicle_id: int, itinerary: List[List[str]]) -> 'TransitLine':
        line = TransitLine(self, idx, transit_vehicle_id)
        self._lines[idx] = line
        for i in range(len(itinerary) - 1):
            link = self.link(itinerary[i], itinerary[i + 1])
            segment = TransitSegment(self, line, link)
            line._segments.append(segment)
            link._segments.append(segment)
        line._segments.append(
            HiddenSegment(self, line, self.node(itinerary[-1])))
        return line


class Mode:
    def __init__(self, idx: str, mode_type: str):
        self.id = idx
        self.type = mode_type
        self.description = ""

    def __str__(self) -> str:
        return self.id


class TransitVehicle:
    def __init__(self, idx: int, mode: str):
        self.number = idx
        self.mode = mode
        self.description = ""

    @property
    def id(self) -> str:
        return str(self.number)

    def __str__(self) -> str:
        return self.id


class NetworkObject:
    def __init__(self, network: Network, extra_attr: Dict[str, Dict[str, Union['Link', 'Node', 'TransitLine', 'TransitSegment']]]):
        self.network = network
        self._extra_attr = {idx: extra_attr[idx].default_value
            for idx in extra_attr}
        self.data1 = 0.0
        self.data2 = 0.0
        self.data3 = 0.0

    @property
    def id(self):
        return None

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
    def __init__(self, 
                 network: Network, 
                 idx: int, 
                 is_centroid: bool = False):
        NetworkObject.__init__(self, network, network._extra_attr["NODE"])
        self.is_centroid = is_centroid
        self.number = idx
        self.x = 0.0
        self.y = 0.0
        self.label = ""

    @property
    def id(self):
        return str(self.number)

    def outgoing_segments(self, include_hidden=False):
        return (s for s in self.network.transit_segments(include_hidden)
            if s.i_node is self)

class Link(NetworkObject):
    def __init__(self, 
                 network: Network, 
                 i_node: Node, 
                 j_node: Node, 
                 modes):
        NetworkObject.__init__(self, network, network._extra_attr["LINK"])
        self.i_node = i_node
        self.j_node = j_node
        self.modes = frozenset(modes)
        self.length = 0.0
        self.type = 1
        self.num_lanes = 1
        self.volume_delay_func = 0
        self.auto_time = 0.1
        self.aux_transit_volume = 0.0
        self._segments = []

    @property
    def id(self) -> str:
        return "{}-{}".format(self.i_node, self.j_node)

    @property
    def reverse_link(self) -> Optional[Link]:
        try:
            return self.network.link(self.j_node, self.i_node)
        except KeyError:
            return None

    def segments(self) -> Iterable:
        return iter(self._segments)


class TransitLine(NetworkObject):
    def __init__(self, network: Network, idx: str, vehicle: TransitVehicle):
        NetworkObject.__init__(
            self, network, network._extra_attr["TRANSIT_LINE"])
        self.id = idx
        self.vehicle = vehicle
        self.headway = 0.01
        self._segments = []

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, idx: str):
        self._id = idx

    @property
    def vehicle(self) -> TransitVehicle:
        return self._vehicle

    @vehicle.setter
    def vehicle(self, vehicle_id: int):
        self._vehicle = self.network._vehicles[vehicle_id]

    @property
    def mode(self) -> Mode:
        return self.vehicle.mode

    def segment(self, idx) -> 'TransitSegment':
        return self._segments[idx]

    def segments(self, include_hidden=False) -> Iterable:
        if include_hidden:
            return iter(self._segments)
        else:
            return iter(self._segments[:-1])


class TransitSegment(NetworkObject):
    def __init__(self, network: Network, line: TransitLine, link: Link):
        NetworkObject.__init__(
            self, network, network._extra_attr["TRANSIT_SEGMENT"])
        self.line = line
        self.link = link
        self.allow_alightings = False
        self.allow_boardings = False
        self.transit_time_func = 0
        self.dwell_time = 0.01

    @property
    def id(self) -> str:
        return "{}-{}".format(self.line, self.link)

    @property
    def i_node(self) -> Node:
        return self.link.i_node

    @property
    def j_node(self) -> Node:
        return self.link.j_node


class HiddenSegment(TransitSegment):
    def __init__(self, network, line, node):
        TransitSegment.__init__(self, network, line, None)
        self._node = node

    @property
    def id(self):
        return "{}-{}".format(self.line, self.i_node)

    @property
    def i_node(self):
        return self._node

    @property
    def j_node(self):
        return None


class ExistenceError(Exception):
    pass


class ArgumentError(Exception):
    pass
