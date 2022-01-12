import bisect

import utils.log as log
import parameters.assignment as param


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
    modesets = []
    intervals = []
    for modes in param.official_node_numbers:
        modesets.append({network.mode(m) for m in modes})
        intervals += param.official_node_numbers[modes]
    unofficial_nodes = set()
    for link in network.links():
        if network.mode('c') in link.modes:
            linktype = link.type % 100
            if (linktype not in param.roadclasses
                    and linktype not in param.custom_roadtypes):
                msg = "Link type missing for link {}".format(link.id)
                log.error(msg)
                raise ValueError(msg)
        if network.mode('t') in link.modes:
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
    for line in network.transit_lines():
        for hdwy in ("@hw_aht", "@hw_pt", "@hw_iht"):
            if line[hdwy] < 0.02:
                msg = "Headway missing for line {}".format(line.id)
                log.error(msg)
                raise ValueError(msg)
