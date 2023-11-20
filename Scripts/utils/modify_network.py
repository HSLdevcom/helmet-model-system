import parameters.assignment as param

# Utility functions that modify a network. Functions take a network as input and return the modified network

def add_bus_stops(network):
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