import numpy
import pandas

import utils.log as log
import parameters.zone as param
from datatypes.purpose import TourPurpose, SecDestPurpose
from models import car_use, linear, tour_combinations
from datatypes.person import Person


class DemandModel:
    """Container for private tour purposes and models.

    Parameters
    ----------
    zone_data : ZoneData
        Data used for all demand calculations
    resultdata : ResultData
        Writer object to result directory
    is_agent_model : bool (optional)
        Whether the model is used for agent-based simulation
    """
    
    def __init__(self, zone_data, resultdata, is_agent_model=False):
        self.resultdata = resultdata
        self.zone_data = zone_data
        self.tour_purposes = []
        self.purpose_dict = {}
        for purpose_spec in param.tour_purposes:
            args = (purpose_spec, zone_data, resultdata, is_agent_model)
            purpose = (SecDestPurpose(*args) if "sec_dest" in purpose_spec
                else TourPurpose(*args))
            self.tour_purposes.append(purpose)
            self.purpose_dict[purpose_spec["name"]] = purpose
        for purpose_spec in param.tour_purposes:
            if "source" in purpose_spec:
                purpose = self.purpose_dict[purpose_spec["name"]]
                for source in purpose_spec["source"]:
                    purpose.sources.append(self.purpose_dict[source])
                    if "sec_dest" in purpose_spec:
                        self.purpose_dict[source].sec_dest_purpose = purpose
        bounds = param.purpose_areas["metropolitan"]
        self.bounds = slice(*zone_data.all_zone_numbers.searchsorted(
            [bounds[0], bounds[-1]]))
        self.car_use_model = car_use.CarUseModel(
            zone_data, self.bounds, param.age_groups, self.resultdata)
        self.tour_generation_model = tour_combinations.TourCombinationModel(
            self.zone_data)
        # Income models used only in agent modelling
        first_not_helsinki = zone_data.zone_numbers.searchsorted(
            param.municipalities["Espoo"][0])
        bounds = (self.bounds.start, first_not_helsinki, self.bounds.stop)
        self._income_models = [
            linear.IncomeModel(
                self.zone_data, slice(*bounds[-2:]),
                self.resultdata, param.age_groups, is_helsinki=False),
            linear.IncomeModel(
                self.zone_data, slice(*bounds[:2]),
                self.resultdata, param.age_groups, is_helsinki=True),
        ]
        if is_agent_model:
            self.create_population()

    def _age_strings(self):
        for age_group in param.age_groups:
            yield "age_{}-{}".format(*age_group)

    def create_population_segments(self):
        """Create population segments.

        Store dict of dicts of `pandas.Series`, where each series is a
        zone array with number of people belonging to segment.
        Upper-level dict keys are age group strings (age_7-17/...).
        Lower-level dict keys are strings car_user and no_car.
        """
        cm = self.car_use_model
        self.zone_data["car_users"] = cm.calc_prob()
        self.segments = {}
        pop = self.zone_data["population"][self.bounds]
        for age in self._age_strings():
            age_pop = self.zone_data["share_" + age][self.bounds] * pop
            car_share = sum(self.zone_data["share_" + gender][self.bounds]
                            * cm.calc_individual_prob(age, gender)
                for gender in cm.genders)
            self.segments[age] = {
                "car_users": car_share * age_pop,
                "no_car": (1-car_share) * age_pop,
            }

    def create_population(self):
        """Create population for agent-based simulation.

        Store list of `Person` instances in `self.population`.
        """
        numpy.random.seed(param.population_draw)
        self.population = []
        zone_numbers = self.zone_data.zone_numbers[self.bounds]
        self.zone_population = pandas.Series(0, zone_numbers)
        # Group -1 is under-7-year-olds
        age_range = numpy.arange(-1, len(param.age_groups))
        for zone_number in zone_numbers:
            weights = [self.zone_data[f"share_{age}"][zone_number]
                for age in self._age_strings()]
            # Append under-7 weight
            weights = [max(1 - sum(weights), 0)] + weights
            if sum(weights) > 1:
                if sum(weights) > 1.005:
                    msg = "Sum of age group shares for zone {} is {}".format(
                        zone_number, sum(weights))
                    log.error(msg)
                    raise ValueError(msg)
                else:
                    weights = numpy.array(weights)
                    rebalance = 1 / sum(weights)
                    weights = rebalance * weights
            zone_pop = int(round(self.zone_data["population"][zone_number]
                                 * param.agent_demand_fraction))
            zone = self.zone_data.zones[zone_number]
            incmod = self._income_models[zone.municipality == "Helsinki"]
            for _ in range(zone_pop):
                i = numpy.random.choice(a=age_range, p=weights)
                if i != -1:
                    self.population.append(Person(
                        zone, param.age_groups[i], self.tour_generation_model,
                        self.car_use_model, incmod))
                    self.zone_population[zone_number] += 1
        numpy.random.seed(None)

    def predict_income(self):
        for model in self._income_models:
            model.predict()

    def generate_tours(self):
        """Generate vector of tours for each tour purpose.

        Not used in agent-based simulation.
        Result is stored in `purpose.gen_model.tours`.
        """
        for purpose in self.tour_purposes:
            purpose.gen_model.init_tours()
            if purpose.area == "peripheral" or purpose.dest == "source":
                purpose.gen_model.add_tours()
        result_data = pandas.DataFrame()  # For printing of results
        gm = self.tour_generation_model
        for age in self._age_strings():
            segments = self.segments[age]
            prob_c = gm.calc_prob(age, is_car_user=True, zones=self.bounds)
            prob_n = gm.calc_prob(age, is_car_user=False, zones=self.bounds)
            nr_tours_sums = pandas.Series()
            for combination in prob_c:
                # Each combination is a tuple of tours performed during a day
                nr_tours = ( prob_c[combination] * segments["car_users"]
                           + prob_n[combination] * segments["no_car"])
                for purpose in combination:
                    self.purpose_dict[purpose].gen_model.tours += nr_tours
                nr_tours_sums["-".join(combination)] = nr_tours.sum()
            result_data[age] = nr_tours_sums.sort_index()
        self.resultdata.print_matrix(
            result_data, "tour_combinations", "tour_combinations")

    def generate_tour_probs(self):
        """Generate matrices of cumulative tour combination probabilities.

        Used in agent-based simulation.

        Returns
        -------
        dict
            Age (age_7-17/...) : tuple
                Is car user (False/True) : numpy.array
                    Matrix with cumulative tour combination probabilities
                    for all zones
        """
        probs = {}
        for age in self._age_strings():
            probs[age] = [self._get_probs(age, is_car_user)
                for is_car_user in (False, True)]
        return probs

    def _get_probs(self, age, is_car_user):
        probs = self.tour_generation_model.calc_prob(
            age, is_car_user, self.bounds)
        return pandas.DataFrame(probs).to_numpy().cumsum(axis=1)
