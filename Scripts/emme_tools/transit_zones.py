import json
import os

import inro.modeller as _m
from shapely.geometry import shape, Point

class TransitZones(_m.Tool()):
    transit_zones = _m.Attribute(str)
    percent = 0

    def __init__(self):
        """Tool with click-button that can be imported in the Modeller GUI.
        """
        self.tool_run_msg = ""

    def page(self):
        pb = _m.ToolPageBuilder(self)
        pb.title = "Reassign transit zones"
        pb.add_select_file(
            "transit_zones", "file", start_path="",
            title="Transit zone area file:"
        )
        if self.tool_run_msg:
            pb.add_html(self.tool_run_msg)
        return pb.render()

    def run(self):
        self()

    def __call__(self):
        """Reassign transit zones for current scenario.
        """
        scen = _m.Modeller().scenario
        network = scen.get_network()
        if not os.path.exists(self.transit_zones):
            self.write(f"Error: File '{self.transit_zones}' does not exist.")
            return
        try:
            with open(self.transit_zones, "r", encoding="utf-8") as file:
                geojson_data = json.load(file)
        except json.JSONDecodeError:
            self.write(f"Error: File '{self.transit_zones}' is not a valid JSON file.")
            return
        num_features = len(geojson_data["features"])
        increment = 100/num_features

        transit_zone_labels = set()
        processed_nodes = 0
        # Access features
        try:
            for feature in geojson_data["features"]:
                zone = feature["properties"]["zone"]  # Access attributes
                transit_zone_labels.add(zone)
                geometry = shape(feature["geometry"])  # Convert geometry to Shapely object
                for node in network.nodes():
                    if Point(node.x, node.y).within(geometry):
                        node.label = zone
                        processed_nodes += 1
                self.percent += increment
        except KeyError:
            self.write("The provided GeoJSON has an invalid format.")
            return
        _m.Modeller().scenario.publish_network(network)
        msg = f"Transit zones for scenario {scen.id} created successfully. Processed {len(transit_zone_labels)} zones and {processed_nodes} nodes."
        self.write(msg)
        self.tool_run_msg = _m.PageBuilder.format_info(msg)

    def percent_completed(self):
        return (0, 100, self.percent)


    def write(self, message):
        _m.logbook_write(message)

    def flush(self):
        """Flush the logbook (i.e., do nothing)."""
        pass