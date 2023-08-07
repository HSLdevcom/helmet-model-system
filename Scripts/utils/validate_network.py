import bisect

import utils.log as log
import parameters.assignment as param


EMME_AUTO_MODE = "AUTO"
EMME_AUX_AUTO_MODE = "AUX_AUTO"
EMME_TRANSIT_MODE = "TRANSIT"
EMME_AUX_TRANSIT_MODE = "AUX_TRANSIT"

def validate(network, fares=None):
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
    if fares is not None:
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
            raise ValueError(msg)
    validate_mode(network, param.main_mode, EMME_AUTO_MODE)
    for m in param.assignment_modes.values():
        validate_mode(network, m, EMME_AUX_AUTO_MODE)
    for m in param.transit_modes:
        validate_mode(network, m, EMME_TRANSIT_MODE)
    for m in param.aux_modes + [param.bike_mode]:
        validate_mode(network, m, EMME_AUX_TRANSIT_MODE)
    modesets = []
    intervals = []
    for modes in param.official_node_numbers:
        modesets.append({network.mode(m) for m in modes})
        intervals += param.official_node_numbers[modes]
    unofficial_nodes = set()
    for link in network.links():
        if not link.modes:
            msg = "No modes defined for link {}. At minimum mode h and one more mode needs to be defined for the simulation to work".format(link.id)
            log.error(msg)
            raise ValueError(msg)
        if network.mode('h') in link.modes and len(link.modes) == 1:
            msg = "Only h mode defined for link {}. At minimum mode h and one more mode needs to be defined for the simulation to work".format(link.id)
            log.error(msg)
            raise ValueError(msg)
        if link.type == 100:
            msg = "Link id {} type must not be 100, please refer to the helmet-docs manual".format(link.id)
            log.error(msg)
            raise ValueError(msg)
        if link.type == 999:
            msg = "Link id {} type must not be 999, please refer to the helmet-docs manual".format(link.id)
            log.error(msg)
            raise ValueError(msg)
        
        linktype = link.type % 100
        if (linktype != 70 and link.length == 0): 
            msg = "Link {} has zero length. Link length can be zero only if linktype is 70. (vaihtokävelyt)".format(link.id)
            log.error(msg)
            raise ValueError(msg)
    
        if (linktype == 1):
            msg = "Link type 1 for link {}. Link type 1 is out of use in Helmet 4+ versions".format(link.id)
            log.error(msg)
            raise ValueError(msg)
        if network.mode('c') in link.modes:
            if (linktype not in param.roadclasses
                    and linktype not in param.custom_roadtypes):
                msg = "Link type missing for link {}".format(link.id)
                log.error(msg)
                raise ValueError(msg)
        if network.mode('t') in link.modes or network.mode('p') in link.modes:
            speedstr = str(int(link.data1))
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
                    raise ValueError(msg)
                
        if link.i_node.is_centroid and link.j_node.is_centroid:
            msg = "Link {} is leading directly from centroid node {} to centroid node {}. This is not allowed.".format(link.id,link.i_node.number,link.j_node.number)
            log.error(msg)
            raise ValueError(msg)
        
        for node in (link.i_node, link.j_node):
            
            i = bisect.bisect(intervals, node.number)
            if i % 2 == 0:
                # If node number is not in one of the official intervals
                unofficial_nodes.add(node.id)
            elif not link.modes <= modesets[i // 2]:
                # If link has unallowed modes
                unofficial_nodes.add(node.id)
    if unofficial_nodes:
        log.warn(
            "Node number(s) {} not consistent with official HSL network".format(
                ', '.join(unofficial_nodes)
        ))
    hdw_attrs = [f"@hw_{tp}" for tp in param.time_periods]
    for line in network.transit_lines():
        for hdwy in hdw_attrs:
            if line[hdwy] < 0.02:
                msg = "Headway missing for line {}".format(line.id)
                log.error(msg)
                raise ValueError(msg)

def validate_mode(network, m, mode_type):
    mode = network.mode(m)
    if mode is None or mode.type != mode_type:
        msg = f"{m} is not {mode_type} mode"
        log.error(msg)
        raise ValueError(msg)
