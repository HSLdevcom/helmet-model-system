class ExternalModel:
    def __init__(self, base_demand, growth):
        self.base_demand = base_demand
        self.growth = growth

    def calc_external(self, mode):
        self.base_demand.open_file("external", "vrk")
        base_mtx = self.base_demand.get_data(mode)
        self.base_demand.close()
        mtx = self.growth[mode].values * base_mtx
        return mtx.T