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
        "Link\tnode_i\tnode_j\tmodes\t" + "\t".join(attr_names) + "\tNoise_zone_width", f"links_{scenario.id}")
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
        resultdata.print_line(
            wkt + "\t" + str(link.i_node.id) + "\t" + str(link.j_node.id)+ "\t" + modes + "\t" + attrs + "\t" + str(noise_zone_width), f"links_{scenario.id}")
    resultdata.flush()
 