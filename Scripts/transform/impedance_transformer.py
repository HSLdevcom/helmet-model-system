from parameters import impedance_share, first_peripheral_zone, first_external_zone, tour_purposes

class ImpedanceTransformer:
    def __init__(self, assignment_model):
        self.assignment = assignment_model

    def transform(self, purpose, impedance):
        """Perform transformation for source matrices from this data source
        Return Dictionary containing transformed matrices
        """
        if tour_purposes[purpose]["area"] == "hs15":
            r_0 = 0
            r_n = self.assignment.get_mapping()[first_peripheral_zone]
        if tour_purposes[purpose]["area"] == "peripheral":
            r_0 = self.assignment.get_mapping()[first_peripheral_zone]
            r_n = self.assignment.get_mapping()[first_external_zone]
        if tour_purposes[purpose]["area"] == "all":
            r_0 = 0
            r_n = self.assignment.get_mapping()[first_external_zone]
        c_n = self.assignment.get_mapping()[first_external_zone]
        day_imp = {}
        for mtx_type in impedance["aht"]:
            day_imp[mtx_type] = {}
        for mode in impedance_share[purpose]:
            if mode == "car":
                if purpose == "hw":
                    ass_class = "car_work"
                else:
                    ass_class = "car_leisure"
            else:
                ass_class = mode
            for mtx_type in day_imp:
                for idx, time_period in enumerate(impedance):
                    if ass_class in impedance[time_period][mtx_type]:
                        share = impedance_share[purpose][mode][time_period]
                        imp = impedance[time_period][mtx_type][ass_class][r_0:r_n, 0:c_n]
                        if idx == 0:
                            day_imp[mtx_type][mode] = share[0] * imp
                        else:
                            day_imp[mtx_type][mode] += share[0] * imp
                        imp = impedance[time_period][mtx_type][ass_class][0:c_n, r_0:r_n]
                        day_imp[mtx_type][mode] += share[1] * imp.T
        return day_imp
