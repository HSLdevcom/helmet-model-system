import pandas
from math import log10

import utils.log as log
from utils.zone_interval import belongs_to_area, faulty_kela_code_nodes
import parameters.assignment as param
import parameters.zone as zone_param
from assignment.abstract_assignment import AssignmentModel
from assignment.assignment_period import AssignmentPeriod


class EmmeAssignmentModel(AssignmentModel):
    """
    Emme assignment definition.

    Parameters
    ----------
    emme_context : assignment.emme_bindings.emme_project.EmmeProject
        Emme projekt to connect to this assignment
    first_scenario_id : int
        Id fo EMME scenario where network is stored and modified.
    separate_emme_scenarios : bool (optional)
        Whether four new scenarios will be created in EMME
        (with ids following directly after first scenario id)
        for storing time-period specific network results:
        day, morning rush hour, midday hour and afternoon rush hour.
    save_matrices : bool (optional)
        Whether matrices will be saved in Emme format for all time periods.
        If false, Emme matrix ids 0-99 will be used for all time periods.
    time_periods : list of str (optional)
            Time period names, default is aht, pt, iht
    first_matrix_id : int (optional)
        Where to save matrices (if saved),
        300 matrix ids will be reserved, starting from first_matrix_id.
        Default is 100(-399).
    """
    def __init__(self, emme_context, first_scenario_id,
                 separate_emme_scenarios=False, save_matrices=False,
                 time_periods=param.time_periods, first_matrix_id=100):
        self.separate_emme_scenarios = separate_emme_scenarios
        self.save_matrices = save_matrices
        self.time_periods = time_periods
        self.first_matrix_id = first_matrix_id if save_matrices else 0
        self.emme_project = emme_context
        self.mod_scenario = self.emme_project.modeller.emmebank.scenario(
            first_scenario_id)

    def prepare_network(self, car_dist_unit_cost=None):
        """Create matrices, extra attributes and calc background variables.

        Parameters
        ----------
        car_dist_unit_cost : float (optional)
            Car cost per km in euros
        """
        self._add_bus_stops()
        if self.separate_emme_scenarios:
            self.day_scenario = self.emme_project.copy_scenario(
                self.mod_scenario, self.mod_scenario.number + 1,
                self.mod_scenario.title + '_' + "vrk",
                overwrite=True, copy_paths=False, copy_strategies=False)
        else:
            self.day_scenario = self.mod_scenario
        matrix_types = tuple({mtx_type for ass_class
            in param.emme_matrices.values() for mtx_type in ass_class})
        id_ten = {result_type: 10*i for i, result_type
            in enumerate(matrix_types + param.transit_classes)}
        self.assignment_periods = []
        for i, tp in enumerate(self.time_periods):
            if self.separate_emme_scenarios:
                scen_id = self.mod_scenario.number + i + 2
                self.emme_project.copy_scenario(
                    self.mod_scenario, scen_id,
                    self.mod_scenario.title + '_' + tp,
                    overwrite=True, copy_paths=False, copy_strategies=False)
            else:
                scen_id = self.mod_scenario.number
            if i == 0 or self.save_matrices:
                emme_matrices = self._create_matrices(
                    tp, 100*i + self.first_matrix_id, id_ten)
            self.assignment_periods.append(AssignmentPeriod(
                tp, scen_id, self.emme_project, emme_matrices,
                separate_emme_scenarios=self.separate_emme_scenarios))
        self._create_attributes(self.day_scenario, self._extra)
        for ap in self.assignment_periods:
            if car_dist_unit_cost is not None:
                ap.dist_unit_cost = car_dist_unit_cost
            ap.prepare(self._create_attributes(ap.emme_scenario, ap.extra))
        for idx in param.volume_delay_funcs:
            try:
                self.emme_project.modeller.emmebank.delete_function(idx)
            except Exception:
                pass
            self.emme_project.modeller.emmebank.create_function(
                idx, param.volume_delay_funcs[idx])

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
        """List of all zone numbers."""
        return self.mod_scenario.zone_numbers

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
        for ap in self.assignment_periods:
            ap.transit_results_links_nodes()
        for transit_class in param.transit_classes:
            for res in param.segment_results:
                self._transit_segment_24h(
                    transit_class, param.segment_results[res])
                if res != "transit_volumes":
                    self._node_24h(
                        transit_class, param.segment_results[res])
        ass_classes = list(param.emme_matrices) + ["bus", "aux_transit"]
        ass_classes.remove("walk")
        for ass_class in ass_classes:
            self._link_24h(ass_class)

        # Aggregate and print vehicle kms and link lengths
        kms = dict.fromkeys(ass_classes, 0.0)
        vdfs = {param.roadclasses[linktype].volume_delay_func
            for linktype in param.roadclasses}
        vdfs.add(0) # Links with car traffic prohibited
        vdf_kms = {ass_class: pandas.Series(0.0, vdfs)
            for ass_class in ass_classes}
        areas = zone_param.area_aggregation
        area_kms = {ass_class: pandas.Series(0.0, areas)
            for ass_class in ass_classes}
        vdf_area_kms = {vdf: pandas.Series(0.0, areas) for vdf in vdfs}
        #The following line only works well in Python 3.7+
        linktypes = list(dict.fromkeys(param.roadtypes.values())) + list(dict.fromkeys(param.railtypes.values()))
        linklengths = pandas.Series(0.0, linktypes)
        soft_modes = param.transit_classes + ("bike",)
        network = self.day_scenario.get_network()
        for link in network.links():
            linktype = link.type % 100
            if linktype in param.roadclasses:
                vdf = param.roadclasses[linktype].volume_delay_func
            elif linktype in param.custom_roadtypes:
                vdf = linktype - 90
            else:
                vdf = 0
            area = belongs_to_area(link.i_node)
            for ass_class in ass_classes:
                veh_kms = link[self._extra(ass_class)] * link.length
                kms[ass_class] += veh_kms
                if vdf in vdfs:
                    vdf_kms[ass_class][vdf] += veh_kms
                if area in areas:
                    area_kms[ass_class][area] += veh_kms
                if (vdf in vdfs
                        and area in vdf_area_kms[vdf]
                        and ass_class not in soft_modes):
                    vdf_area_kms[vdf][area] += veh_kms
            if vdf == 0 and linktype in param.railtypes:
                linklengths[param.railtypes[linktype]] += link.length
            else:
                linklengths[param.roadtypes[vdf]] += link.length / 2
        if faulty_kela_code_nodes:
            s = "Municipality KELA code not found for nodes: " + ", ".join(
                faulty_kela_code_nodes)
            log.warn(s)
        resultdata.print_line("\nVehicle kilometres", "result_summary")
        for ass_class in ass_classes:
            resultdata.print_line(
                "{}:\t{:1.0f}".format(ass_class, kms[ass_class]),
                "result_summary")
            resultdata.print_data(
                vdf_kms[ass_class], "vehicle_kms_vdfs.txt", ass_class)
            resultdata.print_data(
                area_kms[ass_class], "vehicle_kms_areas.txt", ass_class)
        for vdf in vdf_area_kms:
            resultdata.print_data(
                vdf_area_kms[vdf], "vehicle_kms_vdfs_areas.txt", vdf)
        resultdata.print_data(linklengths, "link_lengths.txt", "length")

        # Aggregate and print numbers of stations
        stations = pandas.Series(0, param.station_ids)
        for node in network.regular_nodes():
            for mode in param.station_ids:
                if (node.data2 == param.station_ids[mode]
                        and node[self._extra("transit_won_boa")] > 0):
                    stations[mode] += 1
                    break
        resultdata.print_data(stations, "transit_stations.txt", "number")

        # Aggregate and print transit vehicle kms
        transit_modes = [veh.description for veh in network.transit_vehicles()]
        dists = pandas.Series(0.0, transit_modes)
        times = pandas.Series(0.0, transit_modes)
        for ap in self.assignment_periods:
            network = ap.emme_scenario.get_network()
            volume_factor = param.volume_factors["bus"][ap.name]
            for line in network.transit_lines():
                mode = line.vehicle.description
                headway = line[ap.extra("hw")]
                if 0 < headway < 900:
                    departures = volume_factor * 60/headway
                    for segment in line.segments():
                        dists[mode] += departures * segment.link.length
                        times[mode] += (departures
                                        * segment[ap.extra("base_timtr")])
        resultdata.print_data(dists, "transit_kms.txt", "dist")
        resultdata.print_data(times, "transit_kms.txt", "time")

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
        fares : assignment.datatypes.transit_fare.TransitFareZoneSpecification
            Transit fare zone specification
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
                idx = ap.emme_matrices[transit_class]["cost"]
                emmebank.matrix(idx).set_numpy_data(cost, ap.emme_scenario.id)
            if not self.save_matrices:
                break

    def _copy_matrix(self, mtx_type, ass_class, ass_period_1, ass_period_2):
        from_mtx = ass_period_1.emme_matrices[ass_class][mtx_type]
        to_mtx = ass_period_2.emme_matrices[ass_class][mtx_type]
        self.emme_project.copy_matrix(
            from_mtx, to_mtx,
            "{}_{}_{}".format(mtx_type, ass_class, ass_period_2.name),
            "{} {}".format(to_mtx["description"], ass_period_2.name))

    def _extra(self, attr):
        """Add prefix "@" and suffix "_vrk".

        Parameters
        ----------
        attr : str
            Attribute string to modify

        Returns
        -------
        str
            Modified string
        """
        return "@{}_{}".format(attr, "vrk")

    def _add_bus_stops(self):
        network = self.mod_scenario.get_network()
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
        self.mod_scenario.publish_network(network)

    def _create_matrices(self, time_period, id_hundred, id_ten):
        """Create EMME matrices for storing demand and impedance.

        Parameters
        ----------
        time_period : str
            Time period name (aht, pt, iht)
        id_hundred : int
            A new hundred in the matrix id space marks new assignment period
        id_ten : int
            A new ten in the matrix id space marks new type of matrix

        Returns
        -------
        dict
            key : str
                Assignment class (car_work/transit_leisure/...)
            value : dict
                key : str
                    Matrix type (demand/time/cost/dist/...)
                value : str
                    EMME matrix id
        """
        tag = time_period if self.save_matrices else ""
        emme_matrices = {}
        for j, ass_class in enumerate(param.emme_matrices, start=1):
            matrix_ids = {}
            for mtx_type in param.emme_matrices[ass_class]:
                matrix_ids[mtx_type] = "mf{}".format(
                    id_hundred + id_ten[mtx_type] + j)
                description = f"{mtx_type}_{ass_class}_{tag}"
                default_value = 0 if mtx_type == "demand" else 999999
                self.emme_project.create_matrix(
                    matrix_id=matrix_ids[mtx_type],
                    matrix_name=description, matrix_description=description,
                    default_value=default_value, overwrite=True)
            if ass_class in param.transit_classes:
                for subset, parts in param.transit_impedance_matrices.items():
                    matrix_ids[subset] = {}
                    for mtx_type, longer_name in parts.items():
                        id = f"mf{id_hundred + id_ten[ass_class] + j}"
                        matrix_ids[subset][longer_name] = id
                        matrix_ids[longer_name] = id
                        description = f"{mtx_type}_{ass_class}_{tag}"
                        self.emme_project.create_matrix(
                            matrix_id=id, matrix_name=description,
                            matrix_description=description,
                            default_value=999999, overwrite=True)
            emme_matrices[ass_class] = matrix_ids
        return emme_matrices

    def _create_attributes(self, scenario, extra):
        """Create extra attributes needed in assignment.

        Parameters
        ----------
        scenario : inro.modeller.emmebank.scenario
            Emme scenario to create attributes for
        extra : function
            Small helper function which modifies string
            (e.g., self._extra)
        """
        # Create link attributes
        for ass_class in list(param.emme_matrices) + ["bus"]:
            self.emme_project.create_extra_attribute(
                "LINK", extra(ass_class), ass_class + " volume",
                overwrite=True, scenario=scenario)
        for attr in ("total_cost", "toll_cost", "car_time", "aux_transit"):
            self.emme_project.create_extra_attribute(
                "LINK", extra(attr), attr,
                overwrite=True, scenario=scenario)
        # Create node and transit segment attributes
        attr = param.segment_results
        seg_results = {tc: {res: extra(tc[:11]+"_"+attr[res])
                for res in param.segment_results}
            for tc in param.transit_classes}
        for tc in param.transit_classes:
            for res in param.segment_results:
                self.emme_project.create_extra_attribute(
                    "TRANSIT_SEGMENT", seg_results[tc][res],
                    tc+" "+res, overwrite=True, scenario=scenario)
                if res != "transit_volumes":
                    self.emme_project.create_extra_attribute(
                        "NODE", extra(tc[:10]+"n_"+attr[res]),
                        tc+" "+res, overwrite=True, scenario=scenario)
        self.emme_project.create_extra_attribute(
            "TRANSIT_SEGMENT", param.extra_waiting_time["penalty"],
            "wait time st.dev.", overwrite=True, scenario=scenario)
        self.emme_project.create_extra_attribute(
            "TRANSIT_SEGMENT", "@" + param.congestion_cost,
            "transit congestion cost", overwrite=True, scenario=scenario)
        self.emme_project.create_extra_attribute(
            "TRANSIT_SEGMENT", "@" + param.uncongested_transit_time,
            "uncongested transit time", overwrite=True, scenario=scenario)
        self.emme_project.create_extra_attribute(
            "TRANSIT_SEGMENT", extra(param.uncongested_transit_time),
            "uncongested transit time", overwrite=True, scenario=scenario)
        log.debug("Created extra attributes for scenario {}".format(
            scenario))
        return seg_results

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
            light_modes = (
                self._extra("car_work"),
                self._extra("car_leisure"),
                self._extra("van"),
            )
            traffic = sum([link[mode] for mode in light_modes])
            rlink = link.reverse_link
            if rlink is None:
                reverse_traffic = 0
            else:
                reverse_traffic = sum([rlink[mode] for mode in light_modes])
            cross_traffic = (param.years_average_day_factor
                             * param.share_7_22_of_day
                             * (traffic+reverse_traffic))
            heavy = (link[self._extra("truck")]
                     + link[self._extra("trailer_truck")])
            traffic = max(traffic, 0.01)
            heavy_share = heavy / (traffic+heavy)

            # Calculate speed
            link = morning_network.link(link.i_node, link.j_node)
            rlink = link.reverse_link
            if reverse_traffic > 0:
                speed = (60 * 2 * link.length
                         / (link["@car_time_aht"]+rlink["@car_time_aht"]))
            else:
                speed = (0.3*(60*link.length/link["@car_time_aht"])
                         + 0.7*link.data2)
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

    def _link_24h(self, attr):
        """ 
        Sums and expands link volumes to 24h.

        Parameters
        ----------
        attr : str
            Attribute name that is usually key in param.emme_demand_mtx
        """
        networks = {ap.name: ap.emme_scenario.get_network()
            for ap in self.assignment_periods}
        extras = {ap.name: ap.extra(attr) for ap in self.assignment_periods}
        network = self.day_scenario.get_network()
        extra = self._extra(attr)
        # save link volumes to result network
        for link in network.links():
            day_attr = 0
            for tp in networks:
                try:
                    tp_link = networks[tp].link(link.i_node, link.j_node)
                    day_attr += (tp_link[extras[tp]]
                                 * param.volume_factors[attr][tp])
                except (AttributeError, TypeError):
                    pass
            link[extra] = day_attr
        self.day_scenario.publish_network(network)
        log.info("Link attribute {} aggregated to 24h (scenario {})".format(
            extra, self.day_scenario.id))

    def _node_24h(self, transit_class, attr):
        """ 
        Sums and expands node attributes to 24h.

        Parameters
        ----------
        transit_class : str
            Transit class (transit_work/transit_leisure)
        attr : str
            Attribute name that is usually in param.segment_results
        """
        attr = transit_class[:10] + 'n_' + attr
        networks = {ap.name: ap.emme_scenario.get_network()
            for ap in self.assignment_periods}
        extras = {ap.name: ap.extra(attr) for ap in self.assignment_periods}
        network = self.day_scenario.get_network()
        extra = self._extra(attr)
        # save node volumes to result network
        for node in network.nodes():
            day_attr = 0
            for tp in networks:
                try:
                    tp_node = networks[tp].node(node.id)
                    day_attr += (tp_node[extras[tp]]
                                 * param.volume_factors[transit_class][tp])
                except (AttributeError, TypeError):
                    pass
            node[extra] = day_attr
        self.day_scenario.publish_network(network)
        log.info("Node attribute {} aggregated to 24h (scenario {})".format(
            extra, self.day_scenario.id))

    def _transit_segment_24h(self, transit_class, attr):
        """ 
        Sums and expands transit attributes to 24h.

        Parameters
        ----------
        transit_class : str
            Transit class (transit_work/transit_leisure)
        attr : str
            Attribute name that is usually in param.segment_results
        """
        attr = transit_class[:11] + '_' + attr
        networks = {ap.name: ap.emme_scenario.get_network()
            for ap in self.assignment_periods}
        extras = {ap.name: ap.extra(attr) for ap in self.assignment_periods}
        network = self.day_scenario.get_network()
        extra = self._extra(attr)
        # save segment volumes to result network
        for segment in network.transit_segments():
            day_attr = 0
            for tp in networks:
                try:
                    tp_segment = networks[tp].transit_line(
                        segment.line.id).segment(segment.number)
                    day_attr += (tp_segment[extras[tp]]
                                 * param.volume_factors[transit_class][tp])
                except (AttributeError, TypeError):
                    pass
            segment[extra] = day_attr
        self.day_scenario.publish_network(network)
        log.info("Transit attribute {} aggregated to 24h (scenario {})".format(
            extra, self.day_scenario.id))
