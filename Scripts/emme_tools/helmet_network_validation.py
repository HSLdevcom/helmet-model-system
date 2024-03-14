import os
import sys
import logging
from collections import namedtuple

import inro.modeller as _m

# TODO Could this be done more elegantly?
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),"../"))
from utils.validate_network import validate


class Validation(_m.Tool()):
    def __init__(self):
        """Tool with click-button that can be imported in the Modeller GUI.
        """
        self.tool_run_msg = ""
        sh = logging.StreamHandler(stream=self)
        logging.getLogger().addHandler(sh)

    def page(self):
        pb = _m.ToolPageBuilder(self)
        pb.title = "Validate network"
        if self.tool_run_msg:
            pb.add_html(self.tool_run_msg)
        return pb.render()

    def run(self):
        self()

    def __call__(self):
        """Perform a network validation for current scenario.
        """
        modeller = _m.Modeller()
        scen = modeller.scenario
        validate(scen.get_network())
        msg = "Network validation finished for scenario {}!".format(scen.id)
        self.write(msg)
        self.tool_run_msg = _m.PageBuilder.format_info(msg)

    def write(self, message):
        _m.logbook_write(message)

    def flush(self):
        """Flush the logbook (i.e., do nothing)."""
        pass
