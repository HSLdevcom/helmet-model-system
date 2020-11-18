import parameters.zone as param


class ZoneInterval:
    """Get interval slices for given zone division type.

    Parameters
    ----------
    division_type : str
        Type of zone division (municipalities/areas)
    """

    def __init__(self, division_type):
        self._intervals = param.__dict__[division_type]

    def __getitem__(self, name):
        return slice(
            self._intervals[name][0],
            self._intervals[name][1])

    def __iter__(self):
        return self._intervals.iterkeys()

    def keys(self):
        return self._intervals.keys()


def zone_interval(division_type, name):
    """Get interval for given zone division type.

    Parameters
    ----------
    division_type : str
        Type of zone division (municipalities/areas)
    name : str
        Name of the municipality or area

    Returns
    -------
    slice
        (first zone number, last zone number)
    """
    return slice(
        param.__dict__[division_type][name][0],
        param.__dict__[division_type][name][1])
