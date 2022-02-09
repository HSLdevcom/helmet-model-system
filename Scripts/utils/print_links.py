from utils.calc_noise import NoiseModel


def print_links(network, resultdata):
    attr_names = network.attributes("LINK")
    resultdata.print_line(
        "Link\t" + "\t".join(attr_names) + "\tNoise_zone_width", "links")
    noisemodel = NoiseModel(
        network, ("@car_work", "@car_leisure", "@van"),
        ("@truck", "@trailer_truck"))
    for link in network.links():
        wkt = "LINESTRING ({} {}, {} {})".format(
            link.i_node.x, link.i_node.y, link.j_node.x, link.j_node.y)
        attrs = "\t".join([str(link[attr]) for attr in attr_names])
        noise_zone_width = noisemodel.calc_noise(link)
        resultdata.print_line(
            wkt + "\t" + attrs + "\t" + noise_zone_width, "links")
    resultdata.flush()
