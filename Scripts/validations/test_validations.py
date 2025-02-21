from pathlib import Path
from events.model_system_event_listener import EventHandler
from utils.validation import Validation

if __name__ == '__main__':
    event_handler = EventHandler()
    event_handler.load_listeners(Path(__file__).parent)

    validation = Validation()

    event_handler.on_simulation_started(Path('.'), Path(__file__).parent / 'results', {})
    event_handler.on_validation_initialized(validation, Path(__file__).parent)
    event_handler.on_simulation_complete()

    validation.to_html(Path(__file__).parent / 'test_validation.html')