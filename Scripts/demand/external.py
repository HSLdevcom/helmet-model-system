def calc_external(base_demand, mode):
    base_demand.open_file("external", "vrk")
    base_mtx = base_demand.get_data(mode)
    base_demand.close()
    return base_mtx.T