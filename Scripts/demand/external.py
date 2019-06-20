def calc_external(base_demand):
    base_demand.open_file("external", "vrk")
    base_mtx = base_demand.get_data("car")
    return base_mtx.T