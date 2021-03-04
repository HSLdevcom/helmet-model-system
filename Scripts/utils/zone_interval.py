import parameters.zone as param
import utils.log as log


class ZoneIntervals:
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

    def __contains__(self, item):
        return self._intervals.has_key(item)

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

def belongs_to_area(node):
    """Get name of area to which node belongs to.

    Parameters
    ----------
    node : inro.emme.network.node.Node
        Node in Emme network with municipality KELA code in `ui3`

    Returns
    -------
    str
        Name of area (helsinki_cbd/helsinki_other/espoo_vant_kau/...)
    """
    try:
        municipality = param.kela_codes[int(node.data3)]
        if municipality == "Helsinki" and node.label != 'A':
            first_zone_id = 1000
        else:
            first_zone_id = param.municipalities[municipality][0]
    except KeyError:
        log.warn("Municipality KELA code not found for node {}".format(node.id))
        first_zone_id = -1
    areas = param.areas
    for area in areas:
        if areas[area][0] <= first_zone_id <= areas[area][1]:
            return area
