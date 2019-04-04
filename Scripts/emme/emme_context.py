import os
import logging
import inro.emme.desktop.app as _app
import inro.modeller as _m

# Creates and initializes EMME-resources
class EmmeContext:
    def __init__(self, filepath):
        self.logger = logging.getLogger()
        self.logger.info("Starting Emme...")
        emme_desktop = _app.start_dedicated(
            project=filepath, 
            visible=False, 
            user_initials="HSL"
        )
        sh = logging.StreamHandler(stream=self)
        self.logger.addHandler(sh)
        self.modeller = _m.Modeller(emme_desktop)
        self.logger.info("Emme started.")
        self.path = os.path.dirname(self.modeller.emmebank.path)
        self.create_matrix = self.modeller.tool("inro.emme.data.matrix.create_matrix")

    
    def write(self, message):
        """Write to logbook."""
        # _m.logbook_write(message)
        try:
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
    