import os
import sys
import logging


import inro.modeller as _m

# TODO Could this be done more elegantly?
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),"../"))
from assignment.emme_assignment import EmmeAssignmentModel
import utils.modify_network as mnw


class LinkPrinting(_m.Tool()):
    results_path = _m.Attribute(str)

    def __init__(self):
        """Tool with click-button that can be imported in the Modeller GUI.
        """
        self.tool_run_msg = ""
        sh = logging.StreamHandler(stream=self)
        logging.getLogger().addHandler(sh)

    def page(self):
        pb = _m.ToolPageBuilder(self)
        pb.title = "Run bus stop macro"
        if self.tool_run_msg:
            pb.add_html(self.tool_run_msg)
        return pb.render()

    def run(self):
        self()

    def __call__(self):
        """Implement bus stopping behaviour for current scenario.
        """
        scen = _m.Modeller().scenario
        modified_network = mnw.add_bus_stops(scen.get_network())
        _m.Modeller().scenario.publish_network(modified_network)
        msg = "Bus stops for scenario {} assigned successfully.".format(
            scen.id)
        self.write(msg)

        self.tool_run_msg = _m.PageBuilder.format_info(msg)

    def write(self, message):
        _m.logbook_write(message)

    def flush(self):
        """Flush the logbook (i.e., do nothing)."""
        pass
