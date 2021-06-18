class TransitFareZoneSpecification:
    def __init__(self, fare_table):
        """Transit fare zone specification.

        Parameters
        ----------
        fare_table : pandas.DataFrame
            Table of transit zone combination fares
        """
        self.zone_fares = fare_table["fare"].to_dict()
        try:
            self.exclusive = fare_table["exclusive"].dropna().to_dict()
        except KeyError:
            self.exclusive = {}
        self.dist_fare = self.zone_fares.pop("dist")
        self.start_fare = self.zone_fares.pop("start")

    @property
    def transit_fare_zones(self):
        return {char for char in ''.join(self.zone_fares)}
