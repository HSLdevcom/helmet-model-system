import parameters.assignment as param

def add_bus_stops(network):
    """This function loads the noboa and noali parameter according to the Helmet specs for trams and buses, including VALLU-lines. """
    for line in network.transit_lines():
        if line.mode.id in param.stop_codes:
            stop_codes = param.stop_codes[line.mode.id]
            for segment in line.segments():
                is_stop = segment.i_node.data2 in stop_codes
                if line.mode.id in "de":
                    # Non-HSL bus lines
                    not_hsl = segment.i_node.label not in param.hsl_area
                    if line.id[-1] == '1':
                        # Line starts in HSL area
                        segment.allow_alightings = not_hsl and is_stop
                        segment.allow_boardings = is_stop
                    elif line.id[-1] == '2':
                        # Line ends in HSL area
                        segment.allow_alightings = is_stop
                        segment.allow_boardings = not_hsl and is_stop
                    else:
                        raise ValueError(
                            "Unknown direction code for line " + line.id)
                else:
                    segment.allow_alightings = is_stop
                    segment.allow_boardings = is_stop
    return network

def add_noboa_noali(network):
    """ This function emulates loading the network into the scenario via transactions. It handles buses, trams, metros and trains. Ferries remain as noboa=0 everywhere. """
    for line in network.transit_lines():
        if line.mode.id in param.stop_codes:
            stop_codes = param.stop_codes[line.mode.id]
            for segment in line.segments():
                is_stop = segment.i_node.data2 in stop_codes
                segment.allow_alightings = is_stop
                segment.allow_boardings = is_stop
        elif line.mode.id in ['m','r']:
            for segment in line.segments():
                is_stop = segment.data1 > 0
                segment.allow_alightings = is_stop
                segment.allow_boardings = is_stop
                print(segment.id, is_stop)

    return network