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

def add_bus_stops(network):
    # Initialize an empty dictionary to store line IDs and maximum stop distances
    data = {"line_id": [], "maximum_stop_distance": [], "is_motorway": [], "loops": []}
    high_distance_lines = []
    looped_lines = []

    for line in network.transit_lines():
        if line.mode.id in param.stop_codes:
            stop_codes = param.stop_codes[line.mode.id]
            stop_distance = 0
            max_stop_distance = 0
            is_motorway = 0
            loop = 0

            for segment in line.segments():
                if segment.loop_index > 1 and loop == 0:
                    loop = 1
                    looped_lines.append(line.id)
                segment_length = segment.link.length
                linktype = segment.link.type % 100
                if linktype in param.roadclasses and is_motorway == 0:
                    # Car link with standard attributes
                    roadclass = param.roadclasses[linktype]
                    if roadclass.type == "motorway":
                        is_motorway = 1

                stop_distance += segment_length
                is_stop = segment.i_node.data2 in stop_codes

                if is_stop:
                    if stop_distance > max_stop_distance:
                        max_stop_distance = stop_distance
                    stop_distance = 0

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

            # Append data for the current line
            data["line_id"].append(line.id)
            data["maximum_stop_distance"].append(max_stop_distance)
            data["is_motorway"].append(is_motorway)
            data["loops"].append(loop)

            if line.mode.id in "bg" and max_stop_distance > 3 and not is_motorway: # and int(line.id[0]) < 6
                log.debug(f"Line: {line.id},\t Maximum distance between consecutive stops: {max_stop_distance:.2f}")
                high_distance_lines.append(line.id)

    # TODO: Print to results folder
    max_stop_distances = pd.DataFrame(data)

    if high_distance_lines:
        log.info(f"{len(high_distance_lines)} HSL line(s) have a maximum stop distance greater than 3 km and no motorway sections.")
    
    if looped_lines:
        log.warn(f"Line(s) {looped_lines} traverse over the same links multiple times.")

    return network
