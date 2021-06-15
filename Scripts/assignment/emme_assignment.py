import numpy
import pandas
from math import log10

import utils.log as log
from utils.zone_interval import belongs_to_area, faulty_kela_code_nodes
import parameters.assignment as param
import parameters.zone as zone_param
from abstract_assignment import AssignmentModel
from assignment_period import AssignmentPeriod


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
        self.first_matrix_id = first_matrix_id if save_matrices else 0
        self.emme_project = emme_context
        self.assignment_periods = [AssignmentPeriod(
                tp, first_scenario_id + i + 2, first_scenario_id,
                emme_context, save_matrices=save_matrices)
            for i, tp in enumerate(["aht", "pt", "iht"])]
        # default value for dist, modelsystem sets new from zonedata
        self.dist_unit_cost = param.dist_unit_cost
        self.day_scenario = self.emme_project.modeller.emmebank.scenario(
            first_scenario_id + 1)

    def prepare_network(self):
        """Create matrices, extra attributes and calc background variables."""
        for i, ap in enumerate(self.assignment_periods):
            tag = ap.name if self.save_matrices else ""
            id_hundred = 100*i + self.first_matrix_id
            for ass_class in ap.demand_mtx:
                mtx = ap.demand_mtx[ass_class]
                mtx["id"] = "mf{}".format(id_hundred + mtx["id"])
                self.emme_project.create_matrix(
                    matrix_id=mtx["id"],
                    matrix_name="demand_{}_{}".format(ass_class, tag),
                    matrix_description="{} {}".format(mtx["description"], tag),
                    default_value=0, overwrite=True)
            for mtx_type in ap.result_mtx:
                mtx = ap.result_mtx[mtx_type]
                for ass_class in mtx:
                    mtx[ass_class]["id"] = "mf{}".format(
                        id_hundred + mtx[ass_class]["id"])
                    self.emme_project.create_matrix(
                        matrix_id=mtx[ass_class]["id"],
                        matrix_name="{}_{}_{}".format(mtx_type, ass_class, tag),
                        matrix_description="{} {}".format(
                            mtx[ass_class]["description"], tag),
                        default_value=999999, overwrite=True)
            if not self.save_matrices:
                break
        self._create_attributes(
            self.assignment_periods[0].bike_scenario, param.bike_attributes)
        self._create_attributes(self.day_scenario, param.emme_attributes)
        for ap in self.assignment_periods:
            ap.prepare()

    def init_assign(self, demand):
        ap0 = self.assignment_periods[0]
        ap0.assign(demand, iteration="init")
        if self.save_matrices:
            for ap in self.assignment_periods[1:]:
                self._copy_matrix("time", "bike", ap0, ap)
                self._copy_matrix("dist", "bike", ap0, ap)
                self._copy_matrix("time", "walk", ap0, ap)
                self._copy_matrix("dist", "walk", ap0, ap)

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

    def aggregate_results(self, resultdata):
        """Aggregate results to 24h and print vehicle kms.

        Parameters
        ----------
        resultdata : datahandling.resultdata.Resultdata
            Result data container to print to
        """
        # Aggregate results to 24h
        ass_classes = list(param.assignment_modes) + ["bus"]
        for ass_class in ass_classes:
            self._auto_link_24h(ass_class)
        for transit_class in param.transit_classes:
            self._transit_segment_24h(transit_class, "vol")
            self._transit_segment_24h(transit_class, "boa")
            self._transit_segment_24h(transit_class, "trb")
        self._bike_link_24h()
        for ap in self.assignment_periods:
            self._transit_results_links_nodes(ap.emme_scenario)
        self._transit_results_links_nodes(self.day_scenario)

        # Aggregate and print vehicle kms
        vdfs = param.volume_delays_funcs
        vdf_kms = {ass_class: pandas.Series(0.0, vdfs)
            for ass_class in ass_classes}
        areas = zone_param.area_aggregation
        area_kms = {ass_class: pandas.Series(0.0, areas)
            for ass_class in ass_classes}
        vdf_area_kms = {vdf: pandas.Series(0.0, areas) for vdf in vdfs}
        network = self.day_scenario.get_network()
        for link in network.links():
            if link.volume_delay_func <= 5:
                vdf = link.volume_delay_func
            else:
                # Links with bus lane
                vdf = link.volume_delay_func - 5
            if vdf in vdfs:
                for ass_class in vdf_kms:
                    vdf_kms[ass_class][vdf] += link['@'+ass_class] * link.length
            area = belongs_to_area(link.i_node)
            if area in areas:
                for ass_class in area_kms:
                    area_kms[ass_class][area] += link['@'+ass_class] * link.length
            if vdf in vdfs and area in vdf_area_kms[vdf]:
                for ass_class in ass_classes:
                    vdf_area_kms[vdf][area] += link['@'+ass_class] * link.length
        if faulty_kela_code_nodes:
            s = "Municipality KELA code not found for nodes:"
            for node in faulty_kela_code_nodes:
                s += " {}".format(node)
            log.warn(s)
        for ass_class in vdf_kms:
            resultdata.print_data(
                vdf_kms[ass_class], "vehicle_kms_vdfs.txt", ass_class)
        for ass_class in area_kms:
            resultdata.print_data(
                area_kms[ass_class], "vehicle_kms_areas.txt", ass_class)
        for vdf in vdf_area_kms:
            resultdata.print_data(
                vdf_area_kms[vdf], "vehicle_kms_vdfs_areas.txt", vdf)

        # Aggregate and print numbers of stations
        stations = pandas.Series(0, param.station_ids)
        for node in network.regular_nodes():
            for mode in param.station_ids:
                if (node.data2 == param.station_ids[mode]
                        and node["@transit_boa"] > 0):
                    stations[mode] += 1
                    break
        resultdata.print_data(stations, "transit_stations.txt", "number")

        # Aggregate and print transit vehicle kms
        transit_modes = param.transit_mode_aggregates
        transit_dists = pandas.Series(0.0, transit_modes)
        transit_times = pandas.Series(0.0, transit_modes)
        for ap in self.assignment_periods:
            network = ap.emme_scenario.get_network()
            for line in network.transit_lines():
                mode = "other"
                for modes in transit_modes:
                    if line.mode.id in transit_modes[modes]:
                        mode = modes
                        break
                for segment in line.segments():
                    if 0 < segment.line.headway < 900:
                        freq = (param.volume_factors["bus"][ap.name]
                                * (60 / segment.line.headway))
                        transit_dists[mode] += freq * segment.link.length
                        transit_times[mode] += freq * segment["@base_timtr"]
        resultdata.print_data(transit_dists, "transit_kms.txt", "dist")
        resultdata.print_data(transit_times, "transit_kms.txt", "time")

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
                fares, peripheral_cost, self.mapping)
        else:
            cost = default_cost
        for ap in self.assignment_periods:
            for transit_class in param.transit_classes:
                idx = ap.result_mtx["cost"][transit_class]["id"]
                emmebank.matrix(idx).set_numpy_data(cost)
            if not self.save_matrices:
                break

    def _copy_matrix(self, mtx_type, ass_class, ass_period_1, ass_period_2):
        from_mtx = ass_period_1.result_mtx[mtx_type][ass_class]
        to_mtx = ass_period_2.result_mtx[mtx_type][ass_class]
        self.emme_project.copy_matrix(
            from_mtx["id"], to_mtx["id"],
            "{}_{}_{}".format(mtx_type, ass_class, ass_period_2.name),
            "{} {}".format(to_mtx["description"], ass_period_2.name))
        
    def _create_attributes(self, scenario, attributes):
        """Create attributes needed in assignment."""
        for attr in attributes.keys():
            extr = self.emme_project.create_extra_attribute(
                extra_attribute_type = attributes[attr],
                extra_attribute_name = attr,
                extra_attribute_description = "HM40 results attr",
                extra_attribute_default_value = 0,
                overwrite = True,
                scenario = scenario)
        log.debug("Created extra attributes for scenario {}".format(
            scenario.id))

    def calc_noise(self):
        """Calculate noise according to Road Traffic Noise Nordic 1996.

        Returns
        -------
        pandas.Series
            Area (km2) of noise polluted zone, aggregated to area level
        """
        noise_areas = pandas.Series(0.0, zone_param.area_aggregation)
        network = self.day_scenario.get_network()
        morning_network = self.assignment_periods[0].emme_scenario.get_network()
        for link in network.links():
            # Aggregate traffic
            light_modes = ("@car_work", "@car_leisure", "@van")
            traffic = sum([link[mode] for mode in light_modes])
            rlink = link.reverse_link
            if rlink is None:
                reverse_traffic = 0
            else:
                reverse_traffic = sum([rlink[mode] for mode in light_modes])
            cross_traffic = (param.years_average_day_factor
                             * param.share_7_22_of_day
                             * (traffic+reverse_traffic))
            heavy = link["@truck"] + link["@trailer_truck"]
            traffic = max(traffic, 0.01)
            heavy_share = heavy / (traffic+heavy)

            # Calculate speed
            link = morning_network.link(link.i_node, link.j_node)
            rlink = link.reverse_link
            if reverse_traffic > 0:
                speed = 60 * 2 * link.length / (link.auto_time+rlink.auto_time)
            else:
                speed = 0.3*(60*link.length/link.auto_time) + 0.7*link.data2
            speed = max(speed, 50.0)

            # Calculate start noise
            if speed <= 90:
                heavy_correction = (10*log10((1-heavy_share)
                                    + 500*heavy_share/speed))
            else:
                heavy_correction = (10*log10((1-heavy_share)
                                    + 5.6*heavy_share*(90/speed)**3))
            start_noise = ((68 + 30*log10(speed/50)
                           + 10*log10(cross_traffic/15/1000)
                           + heavy_correction)
                if cross_traffic > 0 else 0)

            # Calculate noise zone width
            func = param.noise_zone_width
            for interval in func:
                if interval[0] <= start_noise < interval[1]:
                    zone_width = func[interval](start_noise - interval[0])
                    break

            # Calculate noise zone area and aggregate to area level
            area = belongs_to_area(link.i_node)
            if area in noise_areas:
                noise_areas[area] += 0.001 * zone_width * link.length
        return noise_areas

    def _transit_results_links_nodes(self, scenario):
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

    def _auto_link_24h(self, attr):
        """ 
        Sums and expands link volumes from different scenarios to one result scenario.
         Parameters
        ----------
        attr : str
            Attribute name thatis usually part of Parameters: link_volumes.
        """
        extra_attr = '@' + attr
        # get attr from different time periods to dictionary
        networks = {}
        for ap in self.assignment_periods:
            networks[ap.name] = ap.emme_scenario.get_network()
        network = self.day_scenario.get_network()
        # save link volumes to result network
        for link in network.links():
            day_attr = 0
            for tp in networks:
                try:
                    tp_link = networks[tp].link(link.i_node, link.j_node)
                    day_attr += (tp_link[extra_attr]
                                 * param.volume_factors[attr][tp])
                except (AttributeError, TypeError):
                    pass
            link[extra_attr] = day_attr
        self.day_scenario.publish_network(network)
        log.info("Auto attribute {} aggregated to 24h (scenario {})".format(
            extra_attr, self.day_scenario.id))

    def _transit_segment_24h(self, transit_class, attr):
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
                    day_attr += (tp_segment[extra_attr]
                                 * param.volume_factors[transit_class][tp])
                except (AttributeError, TypeError):
                    pass
            segment[extra_attr] = day_attr
        self.day_scenario.publish_network(network)
        log.info("Transit attribute {} aggregated to 24h (scenario {})".format(
            extra_attr, self.day_scenario.id))
    
    def _bike_link_24h(self):
        """ 
        Sums and expands bike volumes from different scenarios to one result scenario.
        """
        attr = "@bike_{}"
        # get attr from different time periods to dictionary
        networks = {}
        for ap in self.assignment_periods:
            networks[ap.name] = ap.bike_scenario.get_network()
        # save link volumes to result network
        day_scenario = self.assignment_periods[0].bike_scenario
        network = day_scenario.get_network()
        for link in network.links():
            day_attr = 0
            for tp in networks:
                try:
                    tp_link = networks[tp].link(link.i_node, link.j_node)
                    day_attr += (tp_link[attr.format(tp)]
                                 * param.volume_factors["bike"][tp])
                except (AttributeError, TypeError):
                    pass
            link[attr.format("day")] = day_attr
        day_scenario.publish_network(network)
        log.info("Bike attribute {} aggregated to 24h (scenario {})".format(
            attr.format("day"), day_scenario.id))
