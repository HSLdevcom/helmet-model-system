import bisect

import numpy

import utils.log as log
import parameters.assignment as param
import assignment.datatypes.transit_fare as transit_fare


EMME_AUTO_MODE = "AUTO"
EMME_AUX_AUTO_MODE = "AUX_AUTO"
EMME_TRANSIT_MODE = "TRANSIT"
EMME_AUX_TRANSIT_MODE = "AUX_TRANSIT"
EXTERNAL_RAILWAY_CENTROIDS = set(range(34300, 34400))
MAX_BIKE_INFRASTRUCTURE_CLASS = 4
MAX_LINK_LENGTH = 200 # km

def validate(network, fares: transit_fare.TransitFareZoneSpecification|None=None):
    """Validate EMME network in terms of HELMET compatibility.

    Check that:
    - all auto links have volume-delay functions defined
    - all tram links have speed defined
    - all transit lines have headways defined
    - a majority of nodes has transit fare zone defined (optional)

    Parameters
    ----------
    network : inro.emme.network.Network
        Network to be validated
    fares : assignment.datatypes.transit_fare.TransitFareZoneSpecification
            Transit fare zone specification (optional)
    """
    num_errors = 0
    if fares is not None:
        num_errors += validate_fares(network, fares)
    num_errors += validate_transit(network)
    num_errors += validate_modes(network)
    num_errors += validate_centroids(network)
    num_errors += validate_links(network)
    
    if num_errors > 0:
        msg = f"Network validation failed with {num_errors} error(s)"
        log.error(msg)
        raise ValueError(msg)

def validate_fares(network, fares: transit_fare.TransitFareZoneSpecification):
    fare_zones = fares.transit_fare_zones
    log.debug("Zonedata has fare zones {}".format(', '.join(fare_zones)))
    transit_zones = set()
    nr_transit_zone_nodes = 0
    nr_nodes = 0
    # check that fare zones exist in network
    for node in network.nodes():
        nr_nodes += 1
        if node.label in fare_zones:
            nr_transit_zone_nodes += 1
        transit_zones.add(node.label)
    log.debug("Network has fare zones {}".format(', '.join(transit_zones)))
    if fare_zones > transit_zones:
        log.warn(
            "Some zones in transit costs do not exist in node labels.")
    found_zone_share = nr_transit_zone_nodes / nr_nodes
    if found_zone_share < 0.5:
        msg = "Found transit fare zone for only {:.0%} of nodes.".format(
            found_zone_share)
        log.error(msg)
        return 1
    return 0

def validate_modes(network):
    errors = 0
    errors += validate_mode(network, param.main_mode, EMME_AUTO_MODE)
    for m in list(param.assignment_modes.values()) + [param.bike_mode]:
        errors += validate_mode(network, m, EMME_AUX_AUTO_MODE)
    for m in param.transit_modes:
        errors += validate_mode(network, m, EMME_TRANSIT_MODE)
    for m in param.aux_modes:
        errors += validate_mode(network, m, EMME_AUX_TRANSIT_MODE)
    return errors

def validate_mode(network, m, mode_type):
    mode = network.mode(m)
    if mode is None or mode.type != mode_type:
        msg = f"{m} is not {mode_type} mode"
        log.error(msg)
        return 1
    return 0

def validate_centroids(network):
    # Make sure that cars, pedestrians cyclists can access all centroids
    unaccessible_centroids = []
    required_modes = {'a', 'f', 'c'}  # Modes for pedestrians, cyclists, and cars
    for centroid in network.centroids():
        if centroid.number in EXTERNAL_RAILWAY_CENTROIDS:
            continue  # Skip external railway centroids
        accessible_modes = {mode.id for link in centroid.incoming_links() for mode in link.modes}
        if not required_modes.issubset(accessible_modes):
            unaccessible_centroids.append(centroid.id)
    if unaccessible_centroids:
        msg = f"Centroids {unaccessible_centroids} are not accessible by pedestrians, cyclists and/or passenger cars."
        log.error(msg)
        return 1
    return 0

def validate_links(network):
    errors = 0
    unofficial_nodes = set()
    disallowed_modes = set()
    interval_data = []

    for modes, ranges in param.official_node_numbers.items():
        allowed_ids = set(modes)
        for start, end in ranges:
            interval_data.append((start, end, allowed_ids))
    interval_data.sort(key=lambda x: x[0])
    log.debug("Official node number intervals: {}".format(', '.join(str(i) for i in interval_data)))

    nr_links = 0
    nr_zero_gradients = 0

    tram_mode = network.mode('t')
    light_rail_mode = network.mode('p')
    main_mode = network.mode(param.main_mode)
    
    for link in network.links():
        nr_links += 1
        if not link.modes:
            msg = f"No modes defined for link {link.id}. At minimum mode h and one more mode needs to be defined for the simulation to work"
            log.error(msg)
            errors += 1
        if main_mode in link.modes and len(link.modes) == 1:
            msg = f"Only {param.main_mode} mode defined for link {link.id}. At minimum mode h and one more mode needs to be defined for the simulation to work"
            log.error(msg)
            errors += 1
        if link.type == 100:
            msg = f"Link id {link.id} type must not be 100, please refer to the helmet-docs manual"
            log.error(msg)
            errors += 1
        if link.type == 999:
            msg = f"Link id {link.id} type must not be 999, please refer to the helmet-docs manual"
            log.error(msg)
            errors += 1
        if link.length > MAX_LINK_LENGTH:
            msg = f"Link id {link.id} has length {link.length} km. Project settings might be incorrect"
            log.warn(msg)
        
        linktype = link.type % 100
        if (linktype != 70 and link.length == 0): 
            msg = f"Link {link.id} has zero length. Link length can be zero only if linktype is 70. (vaihtokävelyt)"
            log.error(msg)
            errors += 1
        if (linktype == 1):
            msg = f"Link type 1 for link {link.id}. Link type 1 is out of use in Helmet 4+ versions"
            log.error(msg)
            errors += 1
        for mode in link.modes:  # TODO: Should check all modes, like walking, biking and rail modes
            if mode.id in param.main_mode: 
                continue
            elif str(mode.id) in "cvkybgdew":
                if linktype == None or linktype == 0:
                    msg = f"Link type missing for link {link.id} with modes {str(link.modes)}"
                    log.error(msg)
                    errors += 1
                if (linktype not in param.roadclasses
                        and linktype not in param.custom_roadtypes):
                    msg = f"Link type for link {link.id} with type {link.type} and modes {str(link.modes)} is invalid"
                    log.error(msg)
                    errors += 1
                break
        if tram_mode in link.modes or light_rail_mode in link.modes:
            speedstr = str(int(link.data1)).zfill(6)
            speed = {
                "aht": int(speedstr[:-4]),
                "pt": int(speedstr[-4:-2]),
                "iht": int(speedstr[-2:]),
            }
            for timeperiod in speed:
                if speed[timeperiod] == 0:
                    msg = "Speed is zero for time period {} on link {}".format(
                        timeperiod, link.id)
                    log.error(msg)
                    errors += 1
        
        if (link.i_node.is_centroid or link.j_node.is_centroid) and link.type not in param.connector_link_types:
            msg = f"Link {link.id} is a connector and must be one of the connector link types: {param.connector_link_types}"
            log.error(msg)
            errors += 1

        if link.i_node.is_centroid and link.j_node.is_centroid:
            msg = f"Link {link.id} is leading directly from centroid node {link.i_node.number} to centroid node {link.j_node.number}. This is not allowed."
            log.error(msg)
            errors += 1
        
        for node in (link.i_node, link.j_node): 
            matched = False

            for start, end, allowed_modes in interval_data:
                if start <= node.number <= end:
                    matched = True
                    link_mode_ids = {m.id for m in link.modes}
                    if not link_mode_ids.issubset(allowed_modes):
                        disallowed_modes.add(node.id)
                    break

            if not matched:
                unofficial_nodes.add(node.id)
        
        if link["@pyoratieluokka"] > MAX_BIKE_INFRASTRUCTURE_CLASS:
            msg = "Link {} with modes {} has attribute @pyoratieluokka set to {}. Maximum is 4.".format(link.id,str(link.modes),link["@pyoratieluokka"])
            log.error(msg)
            errors += 1

        try:
            gradient = link["@kaltevuus"]
            if gradient == 0 and link.i_node.is_centroid == False and link.j_node.is_centroid == False:
                nr_zero_gradients += 1
        except KeyError:
            if nr_links == 1:
                msg ="Gradients not defined. Use an extra_links file with @kaltevuus, \
                        or create extra attribute @kaltevuus using modeller. \
                        @kaltevuus is used to model the effect of hills on bicycle route choice. \
                        You can also use the node extra attribute @korkeus to model hills, \
                        but it also requires @kaltevuus to be defined on links. \
                        For more information, see the documentation by clicking the question mark button above."
                log.warn(msg)
    
    zero_gradient_share = nr_zero_gradients / nr_links
    if zero_gradient_share > 0.2:
        msg = f"Gradients missing for {zero_gradient_share:.0%} of links."
        log.warn(msg)

    if unofficial_nodes:
        msg = f"Node number(s) {', '.join(unofficial_nodes)} not consistent with official HSL network."
        log.warn(msg)
    if disallowed_modes:
        msg = f"Node number(s) {', '.join(disallowed_modes)} has disallowed modes."
        log.warn(msg)
    return errors

    
def validate_transit(network):
    """Validate transit network in terms of HELMET compatibility.

    Check that:
    - all transit lines have headways defined
    - all rail links have speed defined
    """
    errors = 0
    headways_missing = []
    hdw_attrs = [f"@hw_{tp}" for tp in param.time_periods]
    for line in network.transit_lines():
        # Check headways
        for hdwy in hdw_attrs:
            if line[hdwy] < 0.02:
                headways_missing.append(line.id)
        # Check speeds for rail lines         
        if line.mode.id in "mrj":
            # TODO: Test this improvement: Instead of checking only the last segment before the stop, check all segments between stops and make sure at least one of them has a speed greater than zero
            # speed_zero = True
            # for seg in line.segments():
            #     if seg.number == 0:
            #         first_stop = seg.id
            #     elif seg.number > 0 and (seg.allow_boardings == 1 or seg.allow_alightings == 1):
            #         if speed_zero:
            #             msg = f"One of the segments between stops {first_stop} and {seg.id} on line {line.id} must have a speed greater than zero."
            #             log.error(msg)
            #             errors += 1
            #         speed_zero = True
            #         first_stop = seg.id
            #     if seg.data1 > 0:  # The stop is at the first node of the segment, so the speed of the segment is after the stop, and so should the check be.
            #         speed_zero = False
            # TODO: Instead of checking the last segment, check all segments between stops and make sure at least one of them has a speed greater than zero
            for seg1, seg2 in zip(list(line.segments()), list(line.segments())[1:]):
                if seg1.data1 == 0 and (seg2.allow_boardings == 1 or seg2.allow_alightings == 1):
                    msg = "Segment id {} must not have zero speed if the next segment has boarding/alighting allowed.".format(seg1.id)
                    log.error(msg)
                    errors += 1
                if seg1.data1 != 0 and (seg2.allow_boardings == 0 and seg2.allow_alightings == 0):
                    msg = "Segment id {} must have zero speed if the next segment forbids boarding/alighting.".format(seg1.id)
                    log.error(msg)
                    errors += 1
        try:  # Only check for custom line issues if it is being used
            if line["@custom_line"] not in [0, 1]:
                msg = "Line {} has @custom_line extra attribute set to {}. If used, it must be either 0 or 1.".format(line.id, line["@custom_line"])
                log.error(msg)
                errors += 1
            elif line.mode.id in "mrj" and line["@custom_line"] == 1:
                msg = "Line {} is a rail line and cannot be marked as a custom line.".format(line.id)
                log.error(msg)
                errors += 1
            if line["@custom_line"] == 1:
                for segment in line.segments():
                    if segment.data3 > 120 or segment.data3 < 0:
                        msg = f"Segment {segment.id} of line {line.id} has @custom_line set to 1 and ul3 (segment speed) set to {segment.data3} km/h. The speed must be between 1 and 120 km/h. Set the speed to 0 to follow the speed of other lines of the same type."
                        log.error(msg)
                        errors += 1
                    elif segment.data3 > 100 or segment.data3 < 10:
                        msg = f"Segment {segment.id} of line {line.id} has @custom_line set to 1 and ul3 (segment speed) set to {segment.data3} km/h. The speed is outside the recommended range of 10-100 km/h."
                        log.warn(msg)
        except KeyError:
            pass

        
    if headways_missing:
        msg = "Headway(s) missing for line(s) {}".format(headways_missing)
        log.error(msg)
        errors += 1
    return errors

def validate_network_connectivity(modeller, scenario):
    """Validate network connectivity in terms of HELMET compatibility.

    Check that:
    - all nodes are reachable from each other
    """
    errors = 0

    #Store mf1 and mf2
    mf1_old = modeller.emmebank.matrix("mf1").get_numpy_data(scenario_id=scenario.id)
    mf2_old = modeller.emmebank.matrix("mf2").get_numpy_data(scenario_id=scenario.id)

    #Define unit matrix
    mf1 = numpy.ones_like(mf1_old, dtype=numpy.float32) * 0.001 #New input
    mf2 = numpy.zeros_like(mf2_old, dtype=numpy.float32) #New output
    modeller.emmebank.matrix("mf1").set_numpy_data(mf1, scenario_id=scenario.id)
    modeller.emmebank.matrix("mf2").set_numpy_data(mf2, scenario_id=scenario.id)

    #Zone numbers
    zone_numbers = {zone: i for i, zone in enumerate(scenario.zone_numbers)}
    modes = ["car","bike","walk","transit"]
    assignment_methods = {
        "car": modeller.tool("inro.emme.traffic_assignment.sola_traffic_assignment"),
        "bike": modeller.tool("inro.emme.traffic_assignment.standard_traffic_assignment"),
        "walk": modeller.tool("inro.emme.transit_assignment.standard_transit_assignment"),
        "transit": modeller.tool("inro.emme.transit_assignment.standard_transit_assignment")
    }
    emme_specs = {
        "car": {
            "type": "STANDARD_TRAFFIC_ASSIGNMENT",
            "classes": [
                {
                "mode": "c",
                "demand": "mf1",
                "results": {
                    "od_travel_times": {
                    "shortest_paths": "mf2"
                    },
                },
                }
            ],
            "stopping_criteria": {
                "max_iterations": 1,
                "best_relative_gap": 1,
                "relative_gap": 1,
                "normalized_gap": 1
            },
            "performance_settings": {
                "number_of_processors": "max"
            }
        },
        "bike": {
            "type": "STANDARD_TRAFFIC_ASSIGNMENT",
            "classes": [
                {
                "mode": "f",
                "demand": "mf1",
                "results": {
                    "od_travel_times": {
                    "shortest_paths": "mf2"
                    },
                },
                }
            ],
            "stopping_criteria": {
                "max_iterations": 1,
                "best_relative_gap": 1,
                "relative_gap": 1,
                "normalized_gap": 1
            },
            "performance_settings": {
                "number_of_processors": "max"
            }
        },
        "walk": {
            "type": "STANDARD_TRANSIT_ASSIGNMENT",
            "modes": [
                "a",
                "s"
            ],
            "demand": "mf1",
            "waiting_time": {
                "headway_fraction": 0.01,
                "effective_headways": "hdw",
                "perception_factor": 0
            },
            "boarding_time": {
                "penalty": 0,
                "perception_factor": 0
            },
            "aux_transit_time": {
                "perception_factor": 1
            },
            "od_results": {
                "transit_times": "mf2"
            },
        },
        "transit": {
            "type": "STANDARD_TRANSIT_ASSIGNMENT",
            "modes": [
                "b",
                "d",
                "e",
                "g",
                "j",
                "m",
                "p",
                "r",
                "t",
                "w",
                "a",
                "s"
            ],
            "demand": "mf1",
            "waiting_time": {
                "headway_fraction": 0.01,
                "effective_headways": "hdw",
                "perception_factor": 0
            },
            "boarding_time": {
                "penalty": 0,
                "perception_factor": 0
            },
            "aux_transit_time": {
                "perception_factor": 1
            },
            "od_results": {
                "transit_times": "mf2"
            },
        },
        }
    Suomenlinna = 1531 #TODO: Accept other island centroids as well
    problematic = [6272,6291,19071] #test network only
    Salo_centroid = 34102 #test network only
    EXTERNAL_RAILWAY_CENTROIDS = [z for z in zone_numbers if z in set(range(34300, 34400))]
    #Make simple assignment to get impedance matrices
    mf1 = modeller.emmebank.matrix("mf1").get_numpy_data(scenario_id=scenario.id)

    for idx in param.volume_delay_funcs:
        try:
            modeller.emmebank.delete_function(idx)
        except Exception:
            pass
    
    test_func = 50
    for idx in [f"fd{test_func}", f"ft{test_func}", f"fp{test_func}"]:
        try:
            modeller.emmebank.delete_function(idx)
        except Exception:
            pass
        modeller.emmebank.create_function(
            idx, "1")

    network = scenario.get_network()
    for link in network.links():
        link.volume_delay_func = test_func
        link.num_lanes = 1
    for segment in network.transit_segments():
        segment.transit_time_func = test_func
    for turn in network.turns():
        turn.penalty_func = test_func
    
    scenario.publish_network(network)
        
    for mode in modes:
        log.info(f"Checking network connectivity for {mode}")
        assignment_methods[mode](specification=emme_specs[mode], scenario=scenario)
        is_connected = (modeller.emmebank.matrix("mf2").get_numpy_data(scenario_id=scenario.id) < 1e6) * 1

        expected_matrix = numpy.ones_like(mf1, dtype=numpy.int32) #1=connected, 0=not connected
        if mode in ["bike","walk"]:
            #TODO: Suomenlinna needs to somehow improved to allow for other island centroids as well
            expected_matrix[:,zone_numbers[Suomenlinna]] = 0
            expected_matrix[zone_numbers[Suomenlinna],:] = 0
            if len(zone_numbers) < 30: #Only test network contains these issues
                expected_matrix[:,[zone_numbers[z] for z in problematic]] = 0
                expected_matrix[[zone_numbers[z] for z in problematic],:] = 0
                expected_matrix[numpy.ix_([zone_numbers[z] for z in problematic],[zone_numbers[z] for z in problematic])] = 1
                expected_matrix[:,zone_numbers[Salo_centroid]] = 0
                expected_matrix[zone_numbers[Salo_centroid],:] = 0
        if mode in ["car","walk","bike"]:
            expected_matrix[:,[zone_numbers[z] for z in EXTERNAL_RAILWAY_CENTROIDS]] = 0
            expected_matrix[[zone_numbers[z] for z in EXTERNAL_RAILWAY_CENTROIDS],:] = 0
            #Fix diagonal
        expected_matrix[numpy.diag_indices_from(expected_matrix)] = 1
        differences = is_connected != expected_matrix
        missed_zones = {}
        if differences.any():
            for diff_pair in numpy.argwhere(differences):
                log.info(str(diff_pair))
                diff_s = scenario.zone_numbers[diff_pair[0]]
                diff_d = scenario.zone_numbers[diff_pair[1]]
                msg = "Network connectivity check failed for {mode}. The following zone pairs are not connected as expected: {diff_pair}".format(
                    mode=mode, diff_pair=[diff_s,diff_d])
                #Make errors as useful as possible
                if diff_s not in missed_zones:
                    missed_zones[diff_s] = 1
                else:
                    missed_zones[diff_s] += 1
                    if missed_zones[diff_s] > 3:
                        continue
                if diff_d not in missed_zones:
                    missed_zones[diff_d] = 1
                else:
                    missed_zones[diff_d] += 1
                    if missed_zones[diff_d] > 3:
                        continue
                log.error(msg)
                errors += 1
                if errors > 100:
                    log.error("Too many connectivity errors, stopping validation")
                    break
    
    #Restore mf1 and mf2
    modeller.emmebank.matrix("mf1").set_numpy_data(mf1_old, scenario_id=scenario.id)
    modeller.emmebank.matrix("mf2").set_numpy_data(mf2_old, scenario_id=scenario.id)

    if errors > 0:
        msg = f"Network connectivity validation failed with {errors} error(s)"
        log.error(msg)
        raise ValueError(msg)