from __future__ import annotations
from typing import Any, Dict, Set, Union
import pandas


class TransitFareZoneSpecification:
    def __init__(self, fare_table: pandas.DataFrame):
        """Transit fare zone specification.

        Parameters
        ----------
        fare_table : pandas.DataFrame
            Table of transit zone combination fares
        """
        self.zone_fares: Dict = fare_table["fare"].to_dict()
        try:
            self.exclusive: Dict = fare_table["exclusive"].dropna().to_dict()
        except KeyError:
            self.exclusive = {}
        self.dist_fare: float = self.zone_fares.pop("dist")
        self.start_fare: float = self.zone_fares.pop("start")

    @property
    def transit_fare_zones(self) -> Set[str]:
        return {char for char in ''.join(self.zone_fares)}
