from utils.calc_noise import NoiseModel


def print_links(network, resultdata):
    """Dump link attributes with wkt coordinates to file.

    Includes noise calculation (works well only when morning peak hour
    is assigned in the same EMME skenario). Noise calculation could be
    removed from here if noise extra attribute would be added.

    Parameters
    ----------
    network : inro.emme.network.Network
        Network where whole-day results are stored
    """
    attr_names = network.attributes("LINK")
    resultdata.print_line(
        "Link\tnode_i\tnode_j" + "\t".join(attr_names) + "\tNoise_zone_width", "links")
    noisemodel = NoiseModel(
        network, ("@car_work_vrk", "@car_leisure_vrk", "@van_vrk"),
        ("@truck_vrk", "@trailer_truck_vrk"))
    for link in network.links():
        wkt = "LINESTRING ({} {}, {} {})".format(
            link.i_node.x, link.i_node.y, link.j_node.x, link.j_node.y)
        attrs = "\t".join([str(link[attr]) for attr in attr_names])
        noise_zone_width = noisemodel.calc_noise(link)
        resultdata.print_line(
            wkt + "\t" + str(link.i_node.id) + "\t" + str(link.j_node.id) + "\t" + attrs + "\t" + str(noise_zone_width), "links")
    resultdata.flush()
