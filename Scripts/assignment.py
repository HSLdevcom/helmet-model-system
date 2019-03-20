import os
import logging
import inro.emme.desktop.app as _app
import inro.modeller as _m
import parameters as param

class AssignmentModel:
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
        self.emme_modeller = _m.Modeller(emme_desktop)
        self.logger.info("Emme started.")
        self.process = self.emme_modeller.tool(
            "inro.emme.data.function.function_transaction")
        self.path = os.path.dirname(self.emme_modeller.emmebank.path)
    
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
    
    def assign(self):
        """Assign cars, bikes and transit for all time periods."""
        self.logger.info("Assignment starts...")
        function_file = os.path.join(self.path,"d411_pituusriippuvaiset_HM30.in")
        self.process(function_file)
        self.calc_road_cost(21)
        self.calc_road_cost(22)
        self.calc_road_cost(23)
        self.assign_cars(21, param.stopping_criteria_coarse, param.aht_mtx_id)
        # self.assign_cars(22, param.stopping_criteria_coarse, param.pt_mtx_id)
        # self.assign_cars(23, param.stopping_criteria_coarse, param.iht_mtx_id)

    def set_matrix(self, id, name, mtx):
        emme_mtx = self.emme_modeller.emmebank.matrix(id)
        if emme_mtx:
            emme_mtx.initialize()
        else:
            emme_mtx = self.emme_modeller.emmebank.create_matrix(id)
        emme_mtx.name = name
        # emme_mtx.description = "demand matrix"
        emme_mtx.set_numpy_data(mtx)
    
    def calc_road_cost(self, scen_id):
        """Calculate road charges and driving costs for one scenario."""
        self.logger.info("Calculates road charges for scenario " + str(scen_id) + "...")
        emmebank = self.emme_modeller.emmebank
        scenario = emmebank.scenario(scen_id)
        netw_specs = []
        # Link cost [eur]
        netw_specs.append({
            "type": "NETWORK_CALCULATION",
            "selections": {
                "link": "all",
            },
            "expression": "@hinta*length",
            "result": "@ruma",
            "aggregation": None,
        })
        # Driving cost [eur]
        netw_specs.append({
            "type": "NETWORK_CALCULATION",
            "selections": {
                "link": "all",
            },
            "expression": str(param.dist_cost)+"*length",
            "result": "@rumpi",
            "aggregation": None,
        })
        # Total cost [eur]
        netw_specs.append({
            "type": "NETWORK_CALCULATION",
            "selections": {
                "link": "all",
            },
            "expression": "@ruma+@rumpi",
            "result": "@rumsi",
            "aggregation": None,
        })
        netcalc = self.emme_modeller.tool(
            "inro.emme.network_calculation.network_calculator")
        netcalc(netw_specs, scenario)
        
    def assign_cars(self, scen_id, stopping_criteria, mtx_id):
        """Perform car traffic assignment for one scenario."""
        emmebank = self.emme_modeller.emmebank
        scenario = emmebank.scenario(scen_id)
        self.logger.info("Creates car cost matrices...")
        create_matrix = self.emme_modeller.tool(
            "inro.emme.data.matrix.create_matrix")
        create_matrix(matrix_id=mtx_id["car_time"],
                      matrix_name="hatim",
                      matrix_description="ha-aikamatr s="+str(scen_id),
                      default_value=0,
                      overwrite=True)
        create_matrix(matrix_id=mtx_id["car_dist"],
                      matrix_name="halen",
                      matrix_description="ha-pituusmatr s="+str(scen_id),
                      default_value=0,
                      overwrite=True)
        create_matrix(matrix_id=mtx_id["car_cost"],
                      matrix_name="ruma",
                      matrix_description="ruuhkamaksumatr s="+str(scen_id),
                      default_value=0,
                      overwrite=True)
        spec = {
            "type": "SOLA_TRAFFIC_ASSIGNMENT",
            "classes": [
                {
                    "mode": "c",
                    "demand": mtx_id["car_demand"],
                    "generalized_cost": {
                        "link_costs": "@rumsi",
                        "perception_factor": param.vot_inv,
                    },
                    "results": {
                        "link_volumes": None,
                        "turn_volumes": None,
                        "od_travel_times": {
                            "shortest_paths": mtx_id["car_time"]
                        }
                    },
                    "path_analyses": [
                        {
                            "link_component": "length",
                            "turn_component": None,
                            "operator": "+",
                            "selection_threshold": {
                                "lower": None,
                                "upper": None,
                            },
                            "path_to_od_composition": {
                                "considered_paths": "ALL",
                                "multiply_path_proportions_by": {
                                    "analyzed_demand": False,
                                    "path_value": True,
                                }
                            },
                            "analyzed_demand": None,
                            "results": {
                                "selected_link_volumes": None,
                                "selected_turn_volumes": None,
                                "od_values": mtx_id["car_dist"],
                            },
                        },
                        {
                            "link_component": "@ruma",
                            "turn_component": None,
                            "operator": "+",
                            "selection_threshold": {
                                "lower": None,
                                "upper": None,
                            },
                            "path_to_od_composition": {
                                "considered_paths": "ALL",
                                "multiply_path_proportions_by": {
                                    "analyzed_demand": False,
                                    "path_value": True
                                }
                            },
                            "analyzed_demand": None,
                            "results": {
                                "selected_link_volumes": None,
                                "selected_turn_volumes": None,
                                "od_values": mtx_id["car_cost"],
                            },
                        },
                    ]
                },
                {
                    "mode": "y",
                    "demand": mtx_id["trailer_truck_demand"],
                    "generalized_cost": {
                        "link_costs": "length",
                        "perception_factor": 0.2,
                    },
                    "results": {
                        "link_volumes": "@yhd",
                        "turn_volumes": None,
                        "od_travel_times": {
                            "shortest_paths": None
                        }
                    },
                    "path_analyses": []
                },
                {
                    "mode": "k",
                    "demand": mtx_id["truck_demand"],
                    "generalized_cost": {
                        "link_costs": "length",
                        "perception_factor": 0.2,
                    },
                    "results": {
                        "link_volumes": "@ka",
                        "turn_volumes": None,
                        "od_travel_times": {
                            "shortest_paths": None
                        }
                    },
                    "path_analyses": []
                },
                {
                    "mode": "v",
                    "demand": mtx_id["van_demand"],
                    "generalized_cost": {
                        "link_costs": "length",
                        "perception_factor": 0.2,
                    },
                    "results": {
                        "link_volumes": "@pa",
                        "turn_volumes": None,
                        "od_travel_times": {
                            "shortest_paths": None
                        }
                    },
                    "path_analyses": []
                },
            ],
            "background_traffic": None,
            "performance_settings": {
                "number_of_processors": "max"
            },
            "stopping_criteria": stopping_criteria,
        }
        self.logger.info("Traffic assignment started...")
        car_assignment = self.emme_modeller.tool(
            "inro.emme.traffic_assignment.sola_traffic_assignment")
        car_assignment(spec, scenario)
        self.logger.info("Traffic assignment performed for scenario " + str(scen_id))
        
        # Traffic assignment produces a generalized cost matrix.
        # To get travel time, monetary cost is removed from generalized cost.
        self.logger.info("Extracts time matrix from generalized cost...")
        matrix_spec = {
            "type": "MATRIX_CALCULATION",
            "expression": mtx_id["car_time"]
                          +"-"+str(param.vot_inv)+"*("+mtx_id["car_cost"]
                          +"+"+str(param.dist_cost)+"*"+mtx_id["car_dist"]+")",
            "result": mtx_id["car_time"],
            "constraint": {
                "by_value": None,
                "by_zone": None,
            },
            "aggregation": {
                "origins": None,
                "destinations": None,
            },
        }
        matcalc = self.emme_modeller.tool(
            "inro.emme.matrix_calculation.matrix_calculator")
        matcalc(matrix_spec, scenario)
    
    def assign_bikes(self, scen_id):
        pass
        
    def assign_transit(self, scen_id):
        pass