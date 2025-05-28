from pathlib import Path
from events.event_handler import EventHandler
from utils.validation import Validation
import webbrowser

if __name__ == '__main__':
    event_handler = EventHandler()
    event_handler.load_listeners(Path(__file__).parent)

    validation = Validation()

    event_handler.on_simulation_started(Path('.'), Path(__file__).parent / 'results', {})
    event_handler.on_validation_initialized(validation, Path(__file__).parent)
    event_handler.on_simulation_complete()

    output_path = Path(__file__).parent / 'test_validation.html'
    validation.to_html(output_path)
    webbrowser.open(output_path.as_uri())
