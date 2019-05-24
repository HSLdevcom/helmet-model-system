from parameters import impedance_share

class ImpedanceTransformer:
    """Perform aggregation/transformation for source matrices from this data source
        Returns Dictionary containing transformed matrices
    """
    def transform(self, purpose, impedance):
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
                        imp = impedance[time_period][mtx_type][ass_class]
                        if idx == 0:
                            day_imp[mtx_type][mode] = share[0] * imp
                        else:
                            day_imp[mtx_type][mode] += share[0] * imp
                        day_imp[mtx_type][mode] += share[1] * imp.T
        return day_imp
