#from models.tour_combinations import TourCombinationModel
from demand.trips import DemandModel
from datatypes.purpose import SecDestPurpose
from datahandling.zonedata import ZoneData, BaseZoneData
from datahandling.resultdata import ResultsData
from transform.impedance_transformer import ImpedanceTransformer
from assignment.emme_assignment import EmmeAssignmentModel
from models.linear import CarDensityModel
import parameters.tour_generation as param
import assignment.departure_time as dt
import os, numpy, pandas
try:
    from assignment.emme_bindings.emme_project import EmmeProject
    import inro.emme.desktop.app as _app
    import inro.emme.database.emmebank as _eb
except ImportError:
    exit(0)

class TourCombinationModel:
    """Nested logit model for tour combination choice.

    Number of tours per day is the upper level of the model and each
    number-of-tour nest can have different combinations of tours
    (e.g., a two-tour combination can be hw-ho, hw-hs or ho-ho, etc.).
    Base for tour generation.

    Parameters
    ----------
    zone_data : ZoneData
        Data used for all demand calculations
    """

    def __init__(self, zone_data):
        self.zone_data = zone_data
        self.param = param.tour_combinations
        self.conditions = param.tour_conditions
        self.increases = param.tour_number_increase
        self.tour_combinations = [combination for nr_tours in self.param
            for combination in self.param[nr_tours]]

    def calc_prob(self, age_group, is_car_user, zones):
        """Calculate choice probabilities for each tour combination.

        Calculation is done for one specific population group
        (age + is car user or not) and probabilities are returned for every
        possible tour combination.

        Parameters
        ----------
        age_group : str
            Age group (age_7-17/age_18-29/...)
        is_car_user : bool
            True if is car user
        zones : int or slice
            Zone number (for agent model) or zone data slice

        Returns
        -------
        dict
            key : tuple of str
                Tour combination (-/hw/hw-ho/...)
            value : pandas.Series
                Choice probabilities per zone
        """
        prob = {}
        nr_tours_exps = {}
        nr_tours_expsum = 0
        for nr_tours in self.param:
            # Upper level of nested logit model
            combination_exps = {}
            combination_expsum = 0
            for tour_combination in self.param[nr_tours]:
                # Lower level of nested logit model
                try:
                    cond = self.conditions[tour_combination]
                except KeyError:
                    is_allowed = True
                else:
                    # If this tour pattern is exclusively for this age group
                    # or if this age group is excluded from this tour pattern
                    is_allowed = (age_group == cond[1] if cond[0]
                        else age_group != cond[1])
                if is_allowed:
                    b = self.param[nr_tours][tour_combination]
                    util = b["constant"]
                    for i in b["zone"]:
                        util += b["zone"][i] * self.zone_data[i][zones]
                        print("---","Zone_data",tour_combination,i,"---")
                        print(self.zone_data[i][zones])
                    dummies = b["individual_dummy"]
                    if age_group in dummies:
                        util += dummies[age_group]
                    if is_car_user and "car_users" in dummies:
                        util += dummies["car_users"]
                    # print("---","Util",tour_combination,"---")
                    # print(util)
                    combination_exps[tour_combination] = numpy.exp(util)
                else:
                    combination_exps[tour_combination] = 0
                combination_expsum += combination_exps[tour_combination]
            for tour_combination in self.param[nr_tours]:
                try:
                    prob[tour_combination] = ( combination_exps[tour_combination]
                                             / combination_expsum)
                except ZeroDivisionError:
                    # Specifically, no 4-tour patterns are allowed for
                    # 7-17-year-olds, so sum will be zero in this case
                    prob[tour_combination] = 0
            util = 0
            nr_tours_exps[nr_tours] = numpy.exp(util)
            scale_param = param.tour_number_scale
            nr_tours_exps[nr_tours] *= numpy.power(combination_expsum, scale_param)
            nr_tours_expsum += nr_tours_exps[nr_tours]
        # Probability of no tours at all (empty tuple) is deduced from
        # other combinations (after calibration)
        prob[()] = 1
        for nr_tours in self.param:
            if nr_tours != 0:
                nr_tours_prob = nr_tours_exps[nr_tours] / nr_tours_expsum
                # Tour number probability is calibrated
                nr_tours_prob *= self.increases[nr_tours]
                prob[()] -= nr_tours_prob
                for tour_combination in self.param[nr_tours]:
                    # Upper and lower level probabilities are combined
                    prob[tour_combination] *= nr_tours_prob
        return prob
    

purpose_areas = {
    "metropolitan": (0, 6000, 16000),
    "peripheral": (16000, 32000),
    "all": (0, 6000, 32000),
    "external": (34031, 34999),
}

emme_dir = "~/Emme_Helmet5/"
project_dir = emme_dir + "Projektit/"
project_name = "Helmet5_nightly"
results_dir = emme_dir+"Tulokset"
db_dir = os.path.join(project_dir, project_name, "Database","emmebank")
# try:
#     from assignment.emme_bindings.emme_project import EmmeProject
#     import inro.emme.desktop.app as _app
#     import inro.emme.database.emmebank as _eb
#     emme_available = True
# except ImportError:
#     emme_available = False

# dim = {
#     "scalar_matrices": 100,
#     "origin_matrices": 100,
#     "destination_matrices": 100,
#     "full_matrices": 400,
#     "scenarios": 5,
#     "centroids": 20,
#     "regular_nodes": 1000,
#     "links": 2000,
#     "turn_entries": 100,
#     "transit_vehicles": 30,
#     "transit_lines": 20,
#     "transit_segments": 2000,
#     "extra_attribute_values": 300000,
#     "functions": 99,
#     "operators": 5000,
#     "sola_analyses": 240,
# }
scenario_num = 1
# try:
#     eb = _eb.create(os.path.join(db_dir, "emmebank"), dim)
#     eb.create_scenario(scenario_num)
#     emmebank_path = eb.path
#     eb.dispose()
# except RuntimeError:
#     emmebank_path = None

emme_project_path = os.path.join(project_dir, project_name, project_name+".emp")
print(emme_project_path)
print(db_dir)
emme_project = EmmeProject(emme_project_path)
emme_available = True

ass_model = EmmeAssignmentModel(
            emme_project,
            first_scenario_id=scenario_num,
            separate_emme_scenarios=False,
            save_matrices=False,
            first_matrix_id=100)

if emme_available:

    mod_scenario = emme_project.modeller.emmebank.scenario(scenario_num)
    #Helmet 4
    # zone_data_path = emme_dir + "Ennusteskenaarioiden_syottotiedot/2023_vain_TCO_uusi"
    # base_zone_data_path = emme_dir + "Lahtodata/2018_zonedata"
    #Helmet 5
    zone_data_path = emme_dir + "Ennusteskenaarioiden_syottotiedot/2023_Santeri"
    base_zone_data_path = emme_dir + "Lahtodata/2023_zonedata"
    zones = ZoneData(zone_data_path, mod_scenario.zone_numbers)
    print(mod_scenario.zone_numbers)
    zdata_base = BaseZoneData(
            base_zone_data_path, ass_model.zone_numbers)
    print("Zone data loaded")
    bounds = purpose_areas["metropolitan"]
    bounds_slice = slice(*zones.all_zone_numbers.searchsorted(
        [bounds[0], bounds[-1]]))
    #bounds_slice = slice(0,16000)
    print(bounds_slice)
    # zone_numbers = zones.all_zone_numbers
    resultdata = ResultsData(os.path.join(results_dir, "H5_test"))
    # imptrans = ImpedanceTransformer()
    dm = DemandModel(zones, resultdata, is_agent_model=False)
    # cdm = CarDensityModel(zdata_base, zones, bounds_slice, resultdata)
    # dtm = dt.DepartureTimeModel(
    #         ass_model.nr_zones, ass_model.time_periods)

    # #need to fake the car predition, because otherwise circular dependency?
    # zones["car_density"] = pandas.Series(
    #         0.0, zones.zone_numbers[bounds_slice])
    # print("Demand model initiated")

    # for purpose in dm.tour_purposes:
    #     if isinstance(purpose, SecDestPurpose):
    #         purpose.gen_model.init_tours()
    #     else:
    #         purpose_impedance = imptrans.transform(
    #             purpose, get_init_impedance(zones,ass_model, dtm, zone_numbers))
    #         purpose.calc_prob(purpose_impedance)
    #         zones = update_ratios(dtm, resultdata, zones, zone_numbers, purpose_impedance, "aht")


    # # Update car density
    # prediction = cdm.predict()
    # zones["car_density"] = prediction
    # zones["cars_per_1000"] = 1000 * prediction



    old_results_path = "~/Emme_Helmet5/Tulokset/H5_test/"
    accessibility_file = old_results_path + "accessibility.txt"
    acc = pandas.read_csv(accessibility_file,sep="\t")

    print(acc["hu_t"][bounds_slice].clip(lower=0))
    zones["hu_t"] = pandas.Series(list(acc["hu_t"][bounds_slice].clip(lower=0)), zones.zone_numbers[bounds_slice])
    zones["ho_w"] = pandas.Series(list(acc["ho_w"][bounds_slice].clip(lower=0)), zones.zone_numbers[bounds_slice])

    car_density_file = old_results_path + "car_density.txt"
    car_density = pandas.read_csv(car_density_file, sep="\t")

    zones["car_density"] = car_density["car_density"]
    zones["cars_per_1000"] = zones["car_density"]*1000

    dm.create_population_segments()
    pop_groups = dm.segments

    tcm = TourCombinationModel(zones)

    age_groups = [(7,17),(18,29),(30,49),(50,64),(65,99)]
    
    sel_zone = 2001

    tours_by_type = {}
    for ag in age_groups:
        ag_str = f"age_{ag[0]}-{ag[1]}"
        for drives_car,dc_str in zip([True,False],["car_users","no_car"]):
            pop_size = pop_groups[ag_str][dc_str]
            #print(ag,drives_car, pop_size)
            res_dict = tcm.calc_prob(ag_str,drives_car,bounds_slice)
            for k in res_dict:
                # for kx in res_dict[k]:
                #     print(kx, res_dict[k])
                # print(ag_str,drives_car,k,len(res_dict[k]))
                # print(res_dict[k])
                # print(ag_str,drives_car,k,res_dict[k].loc[15511])
                #tours_generated = (res_dict[k].loc[sel_zone] * pop_size).sum()
                tours_generated = (res_dict[k] * pop_size).sum()
                if tours_generated > 10: print(k, tours_generated)

                if k not in tours_by_type: tours_by_type[k] = 0
                tours_by_type[k] += tours_generated
    #print(type(tcm.calc_prob("age_18_29",False,bounds_slice)))
    for tc in tours_by_type:
        print(tours_by_type[tc])
    print("Sum: ", sum(tours_by_type.values()))