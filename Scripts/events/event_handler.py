from sys import gettrace
import importlib.util
from utils import log
from pathlib import Path
from events.model_system_event_listener import ModelSystemEventListener


class EventHandler(ModelSystemEventListener):
    """Event handler that calls all equivalent methods in all other ModelSystemEventListener classes."""
    def __init__(self):
        """Initialize the EventHandler.

        Args:
            model_system (ModelSystem): ModelSystem instance.
        """
        super().__init__()
        self.listeners = []
        self._create_methods()

    def register_listener(self, listener: ModelSystemEventListener):
        self.listeners.append(listener)

    def load_listeners(self, listener_path: Path):
        """Load all listeners from a given path.

        Args:
            listener_path (str): The path to the listeners.
        """
        num_loaded = 0
        for file_path in listener_path.glob("*.py"):
            if file_path.name != "__init__.py":
                try:
                    module_name = file_path.stem
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type) and issubclass(attr, ModelSystemEventListener) and attr is not ModelSystemEventListener:
                            self.register_listener(attr())
                            num_loaded += 1
                            log.debug(f"Loaded listener {attr.__name__} from {file_path}")
                except Exception as e:
                    log.error(f"Error loading listener from {file_path}: {e}")
        log.info(f"Loaded {num_loaded} listeners from {listener_path}. Turn on debug logging for more details.")


    def _create_methods(self):
        """Create methods that call all equivalent methods in all other ModelSystemEventListener classes.
        Methods area automatically created for all methods that start with "on_" in all ModelSystemEventListener classes.
        """
        for method_name in dir(ModelSystemEventListener):
            if method_name.startswith("on_") and callable(getattr(ModelSystemEventListener, method_name)):
                setattr(self, method_name, self._create_method(method_name))
                
    def _create_method(self, method_name):
        """Create a method that calls all equivalent methods in all other ModelSystemEventListener classes.

        Args:
            method_name (str): name of the method to create.
        """
        def method(*args, **kwargs):
            for listener in self.listeners:
                try:
                    getattr(listener, method_name)(*args, **kwargs)
                except Exception as e:
                    if gettrace() is not None:
                        # Re-raise exception if debugger is attached
                        raise e
                    log.error(f"Error in {listener.__class__.__name__}.{method_name}: {e}")
        return method