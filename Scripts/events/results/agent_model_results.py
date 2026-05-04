from pathlib import Path
import random
from typing import Dict, List, Union, TYPE_CHECKING
import pandas as pd
import numpy as np

from datatypes.person import Person
from datatypes.tour import Tour
from events.model_system_event_listener import ModelSystemEventListener
from datatypes.demand import Demand
from datatypes.purpose import TourPurpose
from utils import log
import parameters.zone as zone_param

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from assignment.abstract_assignment import AssignmentModel


class AgentModelResults(ModelSystemEventListener): 
    """
    A class to analyze demand by tour destination. For hoo subtour the extra (second) destination is shown.
    """
    
    def __init__(self):
        super().__init__()
    
    def on_model_system_initialized(self,
                                    model_system: 'ModelSystem',
                                    zone_data_path: str, 
                                    base_zone_data_path: str, 
                                    base_matrices_path: str,
                                    results_path: str, 
                                    assignment_model: 'AssignmentModel', 
                                    name: str):
        self.ms = model_system
    
    def on_agent_model_results_calculated(self, previous_iter_impedance):
        random.seed(zone_param.population_draw)
        self.ms.dm.predict_income()
        random.seed(None)
        fname0 = "agents"
        fname1 = "tours"
        # print person and tour attr to files
        self.ms.resultdata.print_line("\t".join(Person.attr), fname0)
        self.ms.resultdata.print_line("\t".join(Tour.attr), fname1)
        for person in self.ms.dm.population:
            person.calc_income()
            self.ms.resultdata.print_line(str(person), fname0)
            for tour in person.tours:
                tour.calc_cost(previous_iter_impedance)
                self.ms.resultdata.print_line(str(tour), fname1)
        log.info("Results printed to files {} and {}".format(
            fname0, fname1))