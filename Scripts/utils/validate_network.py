import utils.log as log
import parameters.assignment as param


def validate(network, fares=None):
    if fares is not None:
        fare_zones = {char for char in ''.join(fares["fare"])}
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
                "All zones in transit costs do not exist in node labels.")
        found_zone_share = nr_transit_zone_nodes / nr_nodes
        if found_zone_share < 0.5:
            msg = "Found transit fare zone for only {:.0%} of nodes.".format(
                found_zone_share)
            log.error(msg)
            raise ValueError(msg)
    for link in network.links():
        if network.mode('c') in link.modes:
            linktype = link.type % 100
            if (linktype not in param.roadclasses
                    and linktype not in param.custom_roadtypes
                    and linktype not in param.connector_link_types):
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
            for tp in speed:
                if speed[tp] == 0:
                    msg = "Speed is zero for time period {} on link {}".format(
                        tp, link.id)
                    log.error(msg)
                    raise ValueError(msg)
    for line in network.transit_lines():
        for hdwy in ("@hw_aht", "@hw_pt", "@hw_iht"):
            if line[hdwy] < 0.02:
                msg = "Headway missing for line {}".format(line.id)
                log.error(msg)
                raise ValueError(msg)
