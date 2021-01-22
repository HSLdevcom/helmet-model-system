import os
import numpy
import pandas
import copy

import utils.log as log
import parameters.assignment as param
import parameters.zone as zone_param
from abstract_assignment import AssignmentModel
from assignment_period import AssignmentPeriod
from datatypes.car import Car
from datatypes.car_specification import CarSpecification
from datatypes.transit import TransitSpecification
from datatypes.path_analysis import PathAnalysis


class EmmeAssignmentModel(AssignmentModel):
    """
    Emme assignment definition.

    Parameters
    ----------
    emme_context : assignment.emme_bindings.emme_project.EmmeProject
        Emme projekt to connect to this assignment
    first_scenario_id : int
        Emme scenario id for bike scenario
        Usually 19, followed by 20 (day scenario), 21 (morning scenario),
        22 (midday scenario) and 23 (afternoon scenario).
        If first scenario is set something else (e.g. 5), then following 
        scenarios are also adjusted (6, 7, 8, 9).
    demand_mtx : dict (optional)
        key : str
            Assignment class (transit_work/transit_leisure)
        value : dict
            id : str
                Emme matrix id
            description : dict
                Matrix description
    result_mtx : dict (optional)
        key : str
            Impedance type (time/cost/dist)
        value : dict
            key : str
                Assignment class (transit_work/transit_leisure)
            value : dict
                id : str
                    Emme matrix id
                description : dict
                    Matrix description
    save_matrices : bool (optional)
        Whether matrices and transit strategies will be saved in
        Emme format for all time periods.
        If false, Emme matrix ids 0-99 will be used for all time periods.
    first_matrix_id : int (optional)
        Where to save matrices (if saved),
        300 matrix ids will be reserved, starting from first_matrix_id.
        Default is 100(-399).
    """
    def __init__(self, emme_context, first_scenario_id,
                 save_matrices=False, first_matrix_id=100):
        self.save_matrices = save_matrices
        self.first_matrix_id = first_matrix_id
        self.emme_project = emme_context
        self.time_periods = {
            "aht": 0,
            "pt": 1,
            "iht": 2,
        }
        self.assignment_periods = [AssignmentPeriod(
                tp, self, first_scenario_id + self.time_periods[tp] + 2,
                emme_context, save_matrices=True)
            for tp in self.time_periods]
        if save_matrices:
            # The matrices need to be created in Emme for only one time period
            self.time_periods = {"aht": 0}
            self.first_matrix_id = 0
        # default value for dist, modelsystem sets new from zonedata
        self.dist_unit_cost = param.dist_unit_cost
        self.bike_scenario = self.emme_project.modeller.emmebank.scenario(
            first_scenario_id)
        self.day_scenario = self.emme_project.modeller.emmebank.scenario(
            first_scenario_id + 1)

    def prepare_network(self):
        """Create matrices, extra attributes and calc background variables."""
        for tp in self.time_periods:
            if self.save_matrices:
                tag = tp
            else:
                tag = ""
            id_hundred = 100*self.time_periods[tp] + self.first_matrix_id
            demand_mtx = self.assignment_periods[self.time_periods[tp]].demand_mtx
            for ass_class in demand_mtx:
                mtx = demand_mtx[ass_class]
                mtx["id"] = "mf{}".format(id_hundred + mtx["id"])
                self.emme_project.create_matrix(
                    matrix_id=mtx["id"],
                    matrix_name="demand_{}_{}".format(ass_class, tag),
                    matrix_description="{} {}".format(mtx["description"], tag),
                    default_value=0, overwrite=True)
            result_mtx = self.assignment_periods[self.time_periods[tp]].result_mtx
            for mtx_type in result_mtx:
                mtx = result_mtx[mtx_type]
                for ass_class in mtx:
                    mtx[ass_class]["id"] = "mf{}".format(
                        id_hundred + mtx[ass_class]["id"])
                    self.emme_project.create_matrix(
                        matrix_id=mtx[ass_class]["id"],
                        matrix_name="{}_{}_{}".format(mtx_type, ass_class, tag),
                        matrix_description="{} {}".format(
                            mtx[ass_class]["description"], tag),
                        default_value=999999, overwrite=True)
        self.create_attributes(self.bike_scenario, param.bike_attributes)
        self.create_attributes(self.day_scenario, param.emme_attributes)
        for ap in self.assignment_periods:
            ap.prepare()

    @property
    def zone_numbers(self):
        """Numpy array of all zone numbers.""" 
        return numpy.array(self.assignment_periods[0].emme_scenario.zone_numbers)

    @property
    def mapping(self):
        """dict: Dictionary of zone numbers and corresponding indices."""
        mapping = {}
        for idx, zone in enumerate(self.zone_numbers):
            mapping[zone] = idx
        return mapping

    @property
    def nr_zones(self):
        """int: Number of zones in assignment model."""
        return len(self.zone_numbers)
        
    def create_attributes(self, scen_id, attributes):
        """Create attributes needed in assignment."""
        emmebank = self.emme_project.modeller.emmebank
        scen = emmebank.scenario(scen_id)
        # defined in params
        for attr in attributes.keys():
            extr = self.emme_project.create_extra_attribute(
                extra_attribute_type = attributes[attr],
                extra_attribute_name = attr,
                extra_attribute_description = "HM40 results attr",
                extra_attribute_default_value = 0,
                overwrite = True,
                scenario = scen)
            log.debug("Created attr {} for scen {}".format(extr.name, scen_id))

    def transit_results_links_nodes(self, scenario):
        """ 
        Calculate and sum transit results to link and nodes.

        Parameters
        ----------
        scen_id : int
            Scenario id.
        """
        network = scenario.get_network()
        for segment in network.transit_segments():
            for transit_class in param.transit_classes:
                segment.i_node["@transit_boa"] += segment["@{}_boa".format(transit_class)]
                segment.i_node["@transit_trb"] += segment["@{}_trb".format(transit_class)]
                if segment.link is not None:
                    segment.link["@transit_vol"] += segment["@{}_vol".format(transit_class)]
        scenario.publish_network(network)

    def aggregate_results(self, resultdata):
        """Aggregate results to 24h and print vehicle kms.

        Parameters
        ----------
        resultdata : datahandling.resultdata.Resultdata
            Result data container to print to
        """
        for ass_class in param.link_volumes:
            self.auto_link_24h(ass_class)
        for transit_class in param.transit_classes:
            self.transit_segment_24h(transit_class, "vol")
            self.transit_segment_24h(transit_class, "boa")
            self.transit_segment_24h(transit_class, "trb")
        self.bike_link_24h()
        for ap in self.assignment_periods:
            self.transit_results_links_nodes(ap.emme_scenario)
        self.transit_results_links_nodes(self.day_scenario)
        freight_classes = ["van", "truck", "trailer_truck"]
        vdfs = [1, 2, 3, 4, 5]
        transit_modes = {
            "bus": "bde",
            "trunk": "g",
            "metro": "m",
            "train": "rj",
            "tram": "tp",
            "other": ""
        }
        kms = dict.fromkeys(freight_classes + ["car"])
        for ass_class in kms:
            kms[ass_class] = dict.fromkeys(vdfs, 0)
        transit_dists = dict.fromkeys(transit_modes, 0)
        transit_times = dict.fromkeys(transit_modes, 0)
        for ap in self.assignment_periods:
            network = ap.emme_scenario.get_network()
            for link in network.links():
                if link.volume_delay_func <= 5:
                    vdf = link.volume_delay_func
                else:
                    # Links with bus lane
                    vdf = link.volume_delay_func - 5
                if vdf in vdfs:
                    car_vol = link.auto_volume
                    for ass_class in freight_classes:
                        kms[ass_class][vdf] += (param.volume_factors[ass_class][ap.name]
                                                * link[param.link_volumes[ass_class]]
                                                * link.length)
                        car_vol -= link[param.link_volumes[ass_class]]
                    kms["car"][vdf] += (param.volume_factors["car"][ap.name]
                                        * car_vol * link.length)
            for line in network.transit_lines():
                mode = "other"
                for modes in transit_modes:
                    if line.mode.id in transit_modes[modes]:
                        mode = modes
                for segment in line.segments():
                    transit_dists[mode] += (param.volume_factors["bus"][ap.name]
                                            * (60 / segment.line.headway)
                                            * segment.link.length)
                    transit_times[mode] += (param.volume_factors["bus"][ap.name]
                                            * (60 / segment.line.headway)
                                            * segment["@base_timtr"])
        for ass_class in kms:
            resultdata.print_data(
                kms[ass_class].values(), "vehicle_kms.txt",
                kms[ass_class].keys(), ass_class)
        resultdata.print_data(
            transit_dists.values(), "transit_kms.txt",
            transit_dists.keys(), "dist")
        resultdata.print_data(
            transit_times.values(), "transit_kms.txt",
            transit_times.keys(), "time")

    def calc_transit_cost(self, fares, peripheral_cost, default_cost=None):
        """Calculate transit zone cost matrix.
        
        Perform multiple transit assignments.
        For each assignment, check if a specific zone has been visited
        by the OD-pair flows. For all the zones that are visited, 
        check if there is a zone combination fare that includes them all.
        If not, distance fare is applied.

        Some fares can be exclusively for municipality citizens
        (i.e., tours starting in that municipality).
        
        Parameters
        ----------
        fares : dict
            key : str
                Fare type (fare/exclusive/dist_fare/start_fare)
            value : dict
                key : str
                    Zone combination (AB/ABC/...)
                value : float/str
                    Transit fare or name of municipality
        peripheral_cost : numpy 2-d matrix
            Fixed cost matrix for peripheral zones
        default_cost : numpy 2-d matrix
            (optional) Fixed cost matrix to use instead of calculated cost
        """
        emmebank = self.emme_project.modeller.emmebank
        if default_cost is None:
            cost = self.assignment_periods[0].calc_transit_cost(
                fares, peripheral_cost)
        else:
            cost = default_cost
        for tp in self.time_periods:
            for transit_class in param.transit_classes:
                idx = self.assignment_periods[self.time_periods[tp]].result_mtx["cost"][transit_class]["id"]
                emmebank.matrix(idx).set_numpy_data(cost)

    def _copy_matrix(self, from_mtx, mtx_type, ass_class, assignment_period):
        self.emme_project.copy_matrix(
            from_mtx, assignment_period.result_mtx[mtx_type][ass_class]["id"],
            "{}_{}_{}".format(mtx_type, ass_class, assignment_period.name),
            "{} {}".format(
                assignment_period.result_mtx[mtx_type][ass_class]["description"],
                assignment_period.name))

    def auto_link_24h(self, attr):
        """ 
        Sums and expands link volumes from different scenarios to one result scenario.
         Parameters
        ----------
        attr : str
            Attribute name thatis usually part of Parameters: link_volumes.
        """
        extra_attr = param.link_volumes[attr]
        # get attr from different time periods to dictionary
        links_attr = {}
        for ap in self.assignment_periods:
            links_attr[ap.name] = {}
            network = ap.emme_scenario.get_network()
            for link in network.links():
                links_attr[ap.name][link.id] = link[extra_attr]
        # create attr to save volume
        extra_attr_day = str(param.link_volumes[attr])
        network = self.day_scenario.get_network()
        # save link volumes to result network
        for link in network.links():
            day_attr = 0
            for tp in links_attr:
                if link.id in links_attr[tp]:
                    day_attr += links_attr[tp][link.id] * param.volume_factors[attr][tp]
            link[extra_attr_day] = day_attr
        self.day_scenario.publish_network(network)
        log.info("Auto attribute {} aggregated to 24h (scenario {})".format(
            extra_attr, self.day_scenario.id))

    def transit_segment_24h(self, transit_class, attr):
        """ 
        Sums and expands transit attributes to 24h.

        Parameters
        ----------
        transit_class : str
            Transit class (transit_work/transit_leisure)
        attr : str
            Attribute name that is usually part of parameters.link_volumes
        """
        networks = {}
        for ap in self.assignment_periods:
            networks[ap.name] = ap.emme_scenario.get_network()
        extra_attr = "@{}_{}".format(transit_class, attr)
        # save link volumes to result network
        network = self.day_scenario.get_network()
        for segment in network.transit_segments():
            day_attr = 0
            for tp in networks:
                try:
                    tp_segment = networks[tp].transit_line(
                        segment.line.id).segment(segment.number)
                    day_attr += tp_segment[extra_attr] * param.volume_factors[transit_class][tp]
                except (AttributeError, TypeError):
                    pass
            segment[extra_attr] = day_attr
        self.day_scenario.publish_network(network)
        log.info("Transit attribute {} aggregated to 24h (scenario {})".format(
            extra_attr, self.day_scenario.id))
    
    def bike_link_24h(self):
        """ 
        Sums and expands bike volumes from different scenarios to one result scenario.
        """
        attr = "bike"
        # get attr from different time periods to dictionary
        links_attr = {}
        for ap in self.assignment_periods:
            extra_attr = "@{}_{}".format(attr, ap.name)
            links_attr[ap.name] = {}
            network = self.bike_scenario.get_network()
            for link in network.links():
                links_attr[ap.name][link.id] = link[extra_attr]
        # save link volumes to result network
        for link in network.links():
            day_attr = 0
            for tp in links_attr:
                if link.id in links_attr[tp]:
                    day_attr += links_attr[tp][link.id] * param.volume_factors[attr][tp]
            extra_attr = "@{}_{}".format(attr, "day")
            link[extra_attr] = day_attr
        self.bike_scenario.publish_network(network) 
        log.info("Bike attribute {} aggregated to 24h (scenario {})".format(
            extra_attr, self.bike_scenario.id))
