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
            if "sec_dest" in purpose_spec:
                purpose = SecDestPurpose(
                    purpose_spec, zone_data, resultdata, is_agent_model)
            else:
                purpose = TourPurpose(
                    purpose_spec, zone_data, resultdata, is_agent_model)
            self.tour_purposes.append(purpose)
            self.purpose_dict[purpose_spec["name"]] = purpose
        for purpose_spec in param.tour_purposes:
            if "source" in purpose_spec:
                purpose = self.purpose_dict[purpose_spec["name"]]
                for source in purpose_spec["source"]:
                    purpose.sources.append(self.purpose_dict[source])
                    if "sec_dest" in purpose_spec:
                        self.purpose_dict[source].sec_dest_purpose = purpose
        bounds = slice(0, zone_data.first_peripheral_zone)
        self.age_groups = (
            (7, 17),
            (18, 29),
            (30, 49),
            (50, 64),
            (65, 99),
        )
        self.car_use_model = car_use.CarUseModel(
            zone_data, bounds, self.age_groups, self.resultdata)
        self.tour_generation_model = tour_combinations.TourCombinationModel(
            self.zone_data)
        # Income models used only in agent modelling
        self._incmod1 = linear.IncomeModel(
            self.zone_data, slice(0, self.zone_data.first_not_helsinki_zone),
            self.age_groups, self.resultdata, is_helsinki=True)
        self._incmod2 = linear.IncomeModel(
            self.zone_data, slice(
                self.zone_data.first_not_helsinki_zone,
                self.zone_data.first_peripheral_zone),
            self.age_groups, self.resultdata, is_helsinki=False)
        if is_agent_model:
            self.create_population()

    def create_population_segments(self):
        """Create population segments.
        
        Returns
        -------
        dict
            Age (age_7-17/...) : dict
                Car user (car_user/no_car) : pandas Series
                    Zone array with number of people belonging to segment
        """
        cm = self.car_use_model
        self.zone_data["car_users"] = cm.calc_prob()
        self.segments = {}
        ubound = self.zone_data.first_peripheral_zone
        pop = self.zone_data["population"][:ubound]
        for age_group in self.age_groups:
            age = "age_" + str(age_group[0]) + "-" + str(age_group[1])
            self.segments[age] = {}
            age_share = self.zone_data["share_" + age][:ubound]
            car_share = 0
            for gender in cm.genders:
                car_share += (self.zone_data["share_" + gender][:ubound]
                              * cm.calc_individual_prob(age, gender))
            self.segments[age]["car_users"] = car_share * age_share * pop
            self.segments[age]["no_car"] = (1-car_share) * age_share * pop

    def create_population(self):
        """Create population for agent-based simulation.
        
        Returns
        -------
        list
            Person
        """
        numpy.random.seed(param.population_draw)
        bounds = slice(0, self.zone_data.first_peripheral_zone)
        self.population = []
        zones = self.zone_data.zone_numbers[bounds]
        self.zone_population = pandas.Series(0, zones)
        for zone_number in zones:
            weights = [1]
            for age_group in self.age_groups:
                key = "share_age_" + str(age_group[0]) + "-" + str(age_group[1])
                share = self.zone_data[key][zone_number]
                weights.append(share)
                weights[0] -= share
            weights[0] = max(weights[0], 0)
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
            incmod = (self._incmod1 if self.zone_data["helsinki"][zone_number]
                else self._incmod2)
            for _ in range(zone_pop):
                a = numpy.arange(-1, len(self.age_groups))
                group = numpy.random.choice(a=a, p=weights)
                if group != -1:
                    # Group -1 is under-7-year-olds and they have weights[0]
                    person = Person(
                        self.zone_data.zones[zone_number],
                        self.age_groups[group], self.tour_generation_model,
                        self.car_use_model, incmod)
                    self.population.append(person)
                    self.zone_population[zone_number] += 1
        numpy.random.seed(None)

    def predict_income(self):
        self._incmod1.predict()
        self._incmod2.predict()

    def generate_tours(self):
        """Generate vector of tours for each tour purpose.

        Not used in agent-based simulation.
        Result is stored in `purpose.gen_model.tours`.
        """
        for purpose in self.tour_purposes:
            purpose.gen_model.init_tours()
            if purpose.area == "peripheral" or purpose.dest == "source":
                purpose.gen_model.add_tours()
        bounds = slice(0, self.zone_data.first_peripheral_zone)
        result_data = pandas.DataFrame()  # For printing of results
        gm = self.tour_generation_model
        for age_group in self.age_groups:
            age = "age_" + str(age_group[0]) + "-" + str(age_group[1])
            segment = self.segments[age]
            prob_c = gm.calc_prob(age, is_car_user=True, zones=bounds)
            prob_n = gm.calc_prob(age, is_car_user=False, zones=bounds)
            nr_tours_sums = pandas.Series()
            for combination in prob_c:
                # Each combination is a tuple of tours performed during a day
                nr_tours = ( prob_c[combination] * segment["car_users"]
                           + prob_n[combination] * segment["no_car"])
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
        for age_group in self.age_groups:
            age = "age_" + str(age_group[0]) + "-" + str(age_group[1])
            probs[age] = (
                self._get_probs(age, is_car_user=False),
                self._get_probs(age, is_car_user=True),
            )
        return probs

    def _get_probs(self, age, is_car_user):
        bounds = slice(0, self.zone_data.first_peripheral_zone)
        gm = self.tour_generation_model
        prob_dict = gm.calc_prob(age, is_car_user, bounds)
        probs = numpy.empty(
            [bounds.stop - bounds.start, len(gm.tour_combinations)])
        for i, tour_combination in enumerate(gm.tour_combinations):
            probs[:, i] = prob_dict[tour_combination]
        return probs.cumsum(axis=1)
