from math import log10

import parameters.assignment as param

class NoiseModel:
    """Model for calculating noise zone width for road links.

    Parameters
    ----------
    morning_network : inro.emme.network.Network
        Network used for morning peak hour assignment
    light_modes : tuple of str
        Extra attribute names for 24-h traffic per assignment class
    heavy_modes : tuple of str
        Extra attribute names for 24-h traffic per assignment class
    """
    def __init__(self, morning_network, light_modes, heavy_modes):
        self.morning_network = morning_network
        self.light_modes = light_modes
        self.heavy_modes = heavy_modes
        self.car_morning = "@car_time_aht"

    def calc_noise(self, link):
        """Calculate noise zone width.

        Parameters
        ----------
        link : inro.emme.network.link.Link
            Link for which noise will be calculated

        Returns
        -------
        float
            Noise zone width (m)
        """
        traffic = sum([link[mode] for mode in self.light_modes])
        rlink = link.reverse_link
        if rlink is None:
            reverse_traffic = 0
        else:
            reverse_traffic = sum([rlink[mode] for mode in self.light_modes])
        cross_traffic = (param.years_average_day_factor
                            * param.share_7_22_of_day
                            * (traffic+reverse_traffic))
        heavy = sum([link[mode] for mode in self.heavy_modes])
        traffic = max(traffic, 0.01)
        heavy_share = heavy / (traffic+heavy)

        # Calculate speed
        link = self.morning_network.link(link.i_node, link.j_node)
        rlink = link.reverse_link
        if reverse_traffic > 0:
            speed = (60 * 2 * link.length
                        / (link[self.car_morning]+rlink[self.car_morning]))
        else:
            speed = (0.3*(60*link.length/link[self.car_morning])
                        + 0.7*link.data2)
        speed = max(speed, 50.0)

        # Calculate start noise
        if speed <= 90:
            heavy_correction = (10*log10((1-heavy_share)
                                + 500*heavy_share/speed))
        else:
            heavy_correction = (10*log10((1-heavy_share)
                                + 5.6*heavy_share*(90/speed)**3))
        start_noise = ((68 + 30*log10(speed/50)
                        + 10*log10(cross_traffic/15/1000)
                        + heavy_correction)
            if cross_traffic > 0 else 0)

        # Calculate noise zone width
        func = param.noise_zone_width
        for interval in func:
            if interval[0] <= start_noise < interval[1]:
                zone_width = func[interval](start_noise - interval[0])
                break
        else:
            raise ValueError("{}".format(link.id))
        return zone_width
