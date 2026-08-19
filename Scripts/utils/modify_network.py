import pandas as pd
import parameters.assignment as param

# Fallback logger for use within EMME
try:
    import utils.log as log
except ImportError:
    class FallbackLogger:
        def info(self, message):
            print(f"[INFO] {message}")

        def debug(self, message):
            print(f"[DEBUG] {message}")

        def warn(self, message):
            print(f"[WARN] {message}")

    log = FallbackLogger()

# Utility functions that modify a network. Functions take a network as input and return the modified network

def calculate_gradients(network):
    printed_times = 0
    for link in network.links():
        if link['@kaltevuus'] == 0 and not link.i_node.is_centroid and not link.j_node.is_centroid:
            try:
                if link.i_node['@korkeus'] != 0 and link.j_node['@korkeus'] != 0:
                    gradient = ((link.i_node['@korkeus'] - link.j_node['@korkeus']) / link.length)*0.1
                    link['@kaltevuus'] = gradient
                    if gradient > 0:
                        log.debug(f"Calculated @kaltevuus for link {link.id}: {gradient}")
            except KeyError:
                if printed_times<5:
                    log.info("@korkeus extra_attribute has not been defined. Skipping adjustment of @kaltevuus values")
                printed_times += 1
    return network

def add_bus_stops(network):
    # Initialize an empty dictionary to store line IDs and maximum stop distances
    
    for line in network.transit_lines():
        if line.mode.id in param.stop_codes:
            stop_codes = param.stop_codes[line.mode.id]
            for segment in line.segments():

                is_stop = segment.i_node.data2 in stop_codes
                segment.dwell_time = 0.01 * is_stop

                if line.mode.id in "de":

                    not_hsl = segment.i_node.label not in param.hsl_area
                    if line.id[-1] == '1':
                        segment.allow_alightings = not_hsl and is_stop
                        segment.allow_boardings = is_stop
                    elif line.id[-1] == '2':
                        segment.allow_alightings = is_stop
                        segment.allow_boardings = not_hsl and is_stop
                    elif line.id[-1] == '3':
                        segment.allow_alightings = is_stop
                        segment.allow_boardings = is_stop
                    else:
                        raise ValueError(
                            "Unknown direction code for line " + line.id)
                else:
                    segment.allow_alightings = is_stop
                    segment.allow_boardings = is_stop

    return network
