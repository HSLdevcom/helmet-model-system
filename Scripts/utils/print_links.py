def print_links(network, resultdata):
    attr_names = network.attributes("LINK")
    resultdata.print_line("Link\t" + "\t".join(attr_names), "links")
    for link in network.links():
        wkt = "LINESTRING ({} {}, {} {})".format(
            link.i_node.x, link.i_node.y, link.j_node.x, link.j_node.y)
        attrs = "\t".join([str(link[attr]) for attr in attr_names])
        resultdata.print_line(wkt + "\t" + attrs, "links")
    resultdata.flush()
