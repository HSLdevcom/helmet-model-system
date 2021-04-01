from parameters.zone import areas, municipalities
from utils.zone_interval import is_in


class Zone:
    counter = 0

    def __init__(self, number):
        self.number = number
        self.index = Zone.counter
        Zone.counter += 1
        self.area = None
        for area in areas:
            if is_in(areas[area], number):
                self.area = area
                print(area)
                break
                
        self.municipality = None
        for mp in municipalities:
            if is_in(municipalities[mp], number):
                self.municipality = mp
                break
