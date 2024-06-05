import os
import sys
import logging

import inro.modeller as _m

# TODO Could this be done more elegantly?
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),"../"))
from utils.print_links import print_links
from datahandling.resultdata import ResultsData


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
        pb.title = "Print link attributes to file"
        pb.add_select_file(
            "results_path", "directory", file_filter="", start_path="",
            title="Directory to save file in:")
        if self.tool_run_msg:
            pb.add_html(self.tool_run_msg)
        return pb.render()

    def run(self):
        self()

    def __call__(self):
        """Print link attributes for current scenario.
        """
        scen = _m.Modeller().scenario
        print_links(scen.get_network(), ResultsData(self.results_path))
        msg = "Link attributes for scenario {} printed to links.txt!".format(
            scen.id)
        self.write(msg)
        self.tool_run_msg = _m.PageBuilder.format_info(msg)

    def write(self, message):
        _m.logbook_write(message)

    def flush(self):
        """Flush the logbook (i.e., do nothing)."""
        pass
