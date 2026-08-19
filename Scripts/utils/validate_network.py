import bisect

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
    data = {"line_id": [], "maximum_stop_distance": [], "is_motorway": [], "loops": []}
    high_distance_lines = []
    looped_lines = []
    headways_missing = []
    hdw_attrs = [f"@hw_{tp}" for tp in param.time_periods]

    whitelist_segments = whitelist_segments = set(["174173-173862","173862-174376","174376-174378","174378-322531",
                                 "322531-173993","82372-83961","322451-322454","321225-322093",
                                 "53199-56670","230810-231182","231182-40353","40353-40352",
                                 "40352-231178","231178-231064","321174-321227", "194395-194397", 
                                 "194397-194395", "212415-204085", "204085-213798","93047-93048"])
    whitelist_line_ids = set(["1094A1"])

    for line in network.transit_lines():
        # Check headways
        for hdwy in hdw_attrs:
            if line[hdwy] < 0.02:
                headways_missing.append(line.id)

        stop_distance = 0
        max_stop_distance = 0
        is_motorway = 0
        loop = 0
        stop_codes = param.stop_codes[line.mode.id]

        for segment in line.segments():
            # Check looped lines
            if segment.loop_index > 1 and loop == 0 and segment.link.id not in whitelist_segments:
                loop += 1

                log.debug(segment.link.id + " is looped in line " + line.id)
                if (line.id not in whitelist_line_ids) and (line.id not in looped_lines):
                    looped_lines.append(line.id)

            # Check 
            segment_length = segment.link.length
            linktype = segment.link.type % 100
            if linktype in param.roadclasses and is_motorway == 0:
                # Car link with standard attributes
                roadclass = param.roadclasses[linktype]
                if roadclass.type == "motorway":
                    is_motorway = 1

            stop_distance += segment_length
            is_stop = segment.i_node.data2 in stop_codes

            if is_stop:
                if stop_distance > max_stop_distance:
                    max_stop_distance = stop_distance
                stop_distance = 0

        # Append data for the current line
        data["line_id"].append(line.id)
        # Lines in Kirkkonummi (line id starts with 6) have weird stop period
        if line.id.startswith("6"):
            max_stop_distance = 0
        data["maximum_stop_distance"].append(max_stop_distance)
        data["is_motorway"].append(is_motorway)
        data["loops"].append(loop)

        if line.mode.id in "bg" and max_stop_distance > 5 and not is_motorway: # and int(line.id[0]) < 6
            log.debug(f"Line: {line.id},\t Maximum distance between consecutive stops: {max_stop_distance:.2f}")
            high_distance_lines.append(line.id)

        # Check speeds for rail lines         
        if line.mode.id in "mrj":
            # TODO: Test this improvement: Instead of checking only the last segment before the stop, check all segments between stops and make sure at least one of them has a speed greater than zero
            # speed_zero = True
            # for seg in line.segments():
            #     if seg.number == 0:
            #         first_stop = seg.id
            #     if seg.data1 > 0:
            #         speed_zero = False
            #     if seg.number > 0 and (seg.allow_boardings == 1 or seg.allow_alightings == 1):
            #         if speed_zero:
            #             msg = f"One of the segments between stops {first_stop} and {seg.id} on line {line.id} must have a speed greater than zero."
            #             log.error(msg)
            #             errors += 1
            #         speed_zero = True
            #         first_stop = seg.id
            # TODO: Instead of checking the last segment, check all segments between stops and make sure at least one of them has a speed greater than zero
            for seg1, seg2 in zip(list(line.segments()), list(line.segments())[1:]):
                if seg1.data1 == 0 and (seg2.allow_boardings == 1 or seg2.allow_alightings == 1):
                    msg = "Segment id {} must not have zero speed if the next segment has boarding/alighting allowed".format(seg1.id)
                    log.error(msg)
                    errors += 1
                if seg1.data1 != 0 and (seg2.allow_boardings == 0 and seg2.allow_alightings == 0):
                    msg = "Segment id {} must not have non-zero speed if the next segment has boarding/alighting disallowed".format(seg1.id)
                    log.error(msg)
                    errors += 1

    # Report missing headways
    if headways_missing:
        msg = "Headway(s) missing for line(s) {}".format(headways_missing)
        log.error(msg)
        errors += 1
    # Report long stop distances
    # TODO: Print to results folder
    # max_stop_distances = pd.DataFrame(data)
    if high_distance_lines:
        log.info(f"{len(high_distance_lines)} HSL line(s) have a maximum stop distance greater than 5 km and no motorway sections.")
    # Report looped lines
    if looped_lines:
        log.warn(f"Line(s) {looped_lines} traverse over the same links multiple times.")

    return errors

