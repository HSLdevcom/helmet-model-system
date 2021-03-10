from parameters.zone import areas, municipalities


class Zone:
    counter = 0

    def __init__(self, number):
        self.number = number
        self.index = Zone.counter
        Zone.counter += 1
        self.area = None
        for area in areas:
            if areas[area][0] <= number < areas[area][1]:
                self.area = area
                break
        self.municipality = None
        for mp in municipalities:
            if  municipalities[mp][0] <= number < municipalities[mp][1]:
                self.municipality = mp
                break
