from utils.calc_noise import NoiseModel
from datahandling.resultdata import ResultsData
def print_links(scenario, resultdata: ResultsData):
    """Dump link attributes with wkt coordinates to file.
    Includes noise calculation (works well only when morning peak hour
    is assigned in the same EMME skenario). Noise calculation could be
    removed from here if noise extra attribute would be added.
    Parameters
    ----------
    scenario : inro.emme.database.scenario.Scenario
        Scenario with a network where whole-day results are stored
    """
    network = scenario.get_network()
    attr_names = network.attributes("LINK")
    resultdata.print_line(
        "Link\tnode_i\tnode_j\tmodes\t" + "\t".join(attr_names) +
        "\ttransit_cap_total_aht\ttransit_cap_seated_aht"
        "\ttransit_cap_total_pt\ttransit_cap_seated_pt"
        "\ttransit_cap_total_iht\ttransit_cap_seated_iht"
        "\tNoise_zone_width", f"links_{scenario.id}")
    noisemodel = NoiseModel(
        network, ("@car_work_vrk", "@car_leisure_vrk", "@van_vrk"),
        ("@truck_vrk", "@trailer_truck_vrk"))
    for link in network.links():
        # link.modes is a frozenset of modes objects, we want a string of identifiers
        modes = "".join([mode.id for mode in link.modes])
        wkt = "LINESTRING ({} {}, {} {})".format(
            link.i_node.x, link.i_node.y, link.j_node.x, link.j_node.y)
        attrs = "\t".join([str(link[attr]) for attr in attr_names])
        noise_zone_width = noisemodel.calc_noise(link)
        transit_cap_total_aht, transit_cap_seated_aht, transit_cap_total_pt, transit_cap_seated_pt, transit_cap_total_iht, transit_cap_seated_iht = linkwise_transit_capacity(link)
        attrs += f"\t{transit_cap_total_aht}\t{transit_cap_seated_aht}\t{transit_cap_total_pt}\t{transit_cap_seated_pt}\t{transit_cap_total_iht}\t{transit_cap_seated_iht}"
        resultdata.print_line(
            wkt + "\t" + str(link.i_node.id) + "\t" + str(link.j_node.id)+ "\t" + modes + "\t" + attrs + "\t" + str(noise_zone_width), f"links_{scenario.id}")
    resultdata.flush()

def linkwise_transit_capacity(link):
    """Calculate linkwise transit capacity.
    Parameters
    ----------
    link : inro.emme.network.link.Link
        Link for which transit capacity is calculated
    Returns
    -------
    float
        Transit total capacity (passengers per hour)
    float
        Transit seated capacity (passengers per hour)
    float
        Transit total capacity (passengers per hour)
    float
        Transit seated capacity (passengers per hour)
    float
        Transit total capacity (passengers per hour)
    float
        Transit seated capacity (passengers per hour)
    """
    link_total_capacity_aht = 0.0
    link_seated_capacity_aht = 0.0
    link_total_capacity_pt = 0.0
    link_seated_capacity_pt = 0.0
    link_total_capacity_iht = 0.0
    link_seated_capacity_iht = 0.0
    for time_period in ["aht", "pt", "iht"]:
        for transit_segment in link.segments():
            vehicle_seated_capacity = transit_segment.line.vehicle.seated_capacity
            vehicle_total_capacity = transit_segment.line.vehicle.total_capacity
            if time_period == "aht":
                link_total_capacity_aht += (60/transit_segment.line[f"@hw_{time_period}"]) * vehicle_total_capacity if 0 < transit_segment.line[f"@hw_{time_period}"] < 999 else 0
                link_seated_capacity_aht += (60/transit_segment.line[f"@hw_{time_period}"]) * vehicle_seated_capacity if 0 < transit_segment.line[f"@hw_{time_period}"] < 999 else 0
            elif time_period == "pt":
                link_total_capacity_pt += (60/transit_segment.line[f"@hw_{time_period}"]) * vehicle_total_capacity if 0 < transit_segment.line[f"@hw_{time_period}"] < 999 else 0
                link_seated_capacity_pt += (60/transit_segment.line[f"@hw_{time_period}"]) * vehicle_seated_capacity if 0 < transit_segment.line[f"@hw_{time_period}"] < 999 else 0
            elif time_period == "iht":
                link_total_capacity_iht += (60/transit_segment.line[f"@hw_{time_period}"]) * vehicle_total_capacity if 0 < transit_segment.line[f"@hw_{time_period}"] < 999 else 0
                link_seated_capacity_iht += (60/transit_segment.line[f"@hw_{time_period}"]) * vehicle_seated_capacity if 0 < transit_segment.line[f"@hw_{time_period}"] < 999 else 0
    return round(link_total_capacity_aht), round(link_seated_capacity_aht), round(link_total_capacity_pt), round(link_seated_capacity_pt), round(link_total_capacity_iht), round(link_seated_capacity_iht)
 
