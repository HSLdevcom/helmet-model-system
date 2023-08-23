from __future__ import annotations
import os
from typing import Any, Optional, cast, TYPE_CHECKING
import utils.log as log
import logging
import inro.emme.desktop.app as _app # type: ignore
import inro.modeller as _m # type: ignore
if TYPE_CHECKING:
    #The following one is likely in different location
    from inro.modeller import ContentManager # type: ignore


class EmmeProject:
    """Initialize EMME-resources.

    Access and wrap INRO's own library,
    from EMME-software's Python site-packages.

    Parameters
    ----------
    project_path : str
        Path to EMME project (.emp) file
    emmebank_path : str (optional)
        Path to emmebank file (if EMME project is not initialized)
    """
    def __init__(self, 
                 project_path: str, 
                 emmebank_path: Optional[str] = None):
        log.info("Starting Emme...")
        if TYPE_CHECKING: self.cm: Optional[ContentManager] = None #type checker hint
        emme_desktop = _app.start_dedicated(
            project=project_path, visible=False, user_initials="HSL")
        if emmebank_path is not None:
            db = emme_desktop.data_explorer().add_database(emmebank_path)
            db.open()
            emme_desktop.project.save()
        # Add logging to EMME
        sh = logging.StreamHandler(stream=self)
        logging.getLogger().addHandler(sh)

        self.modeller = _m.Modeller(emme_desktop)
        log.info("Emme started")
        self.import_scenario = self.modeller.tool(
            "inro.emme.data.scenario.import_scenario")
        self.copy_scenario = self.modeller.tool(
            "inro.emme.data.scenario.copy_scenario")
        self.create_matrix = self.modeller.tool(
            "inro.emme.data.matrix.create_matrix")
        self.copy_matrix = self.modeller.tool(
            "inro.emme.data.matrix.copy_matrix")
        self.network_calc = self.modeller.tool(
            "inro.emme.network_calculation.network_calculator")
        self.car_assignment = self.modeller.tool(
            "inro.emme.traffic_assignment.sola_traffic_assignment")
        self.bike_assignment = self.modeller.tool(
            "inro.emme.traffic_assignment.standard_traffic_assignment")
        self.pedestrian_assignment = self.modeller.tool(
            "inro.emme.transit_assignment.standard_transit_assignment")
        self.transit_assignment = self.modeller.tool(
            "inro.emme.transit_assignment.extended_transit_assignment")
        self.congested_assignment = self.modeller.tool(
            "inro.emme.transit_assignment.congested_transit_assignment")
        self.matrix_results = self.modeller.tool(
            "inro.emme.transit_assignment.extended.matrix_results")
        self.network_results = self.modeller.tool(
            "inro.emme.transit_assignment.extended.network_results")
        self.create_extra_attribute = self.modeller.tool(
            "inro.emme.data.extra_attribute.create_extra_attribute")
    
    def write(self, message: str):
        """Write to logbook."""
        # _m.logbook_write(message)

        try:
            if TYPE_CHECKING: self.cm = cast(ContentManager, self.cm)
            self.cm.__exit__(None, None, None)
        except AttributeError:
            pass
        # Logbook_trace returns a content manager that can be used to create 
        # hierarchies. By entering the cm, everything that Emme itself writes
        # to the logbook will be nested underneath this logbook entry.
        self.cm = _m.logbook_trace(message)
        self.cm.__enter__()
        
    def flush(self):
        """Flush the logbook (i.e., do nothing)."""
        pass
