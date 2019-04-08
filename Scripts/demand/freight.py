class FreightModel:
    def __init__(self, zone_data):
        self.zdata = zone_data

    def calc_freight_traffic(self):
        trucks = ( 0.0044 * self.zdata.population 
                 + 0.0222 * self.zdata.workplaces 
                 + 0.1385 * self.zdata.logistics 
                 + 0.00134 * self.zdata.shops
                 + 0.001)
        trailer_trucks = ( 0.0213 * self.zdata.workplaces
                         + 0.1944 * self.zdata.logistics
                         + 0.00095 * self.zdata.shops
                         + 0.001)

