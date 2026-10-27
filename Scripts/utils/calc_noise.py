import math

import parameters.assignment as assignment_param
import parameters.zone as zone_param


class NoiseModel:
    """Model for calculating the 55 dB noise-zone width of road links."""

    def __init__(self, morning_network, light_modes, heavy_modes):
        self.morning_network = morning_network
        self.light_modes = light_modes
        self.heavy_modes = heavy_modes
        self.car_morning = "@car_time_aht"

    def calc_noise(self, link):
        """Calculate the width (m) of the link's 55 dB noise zone."""
        traffic = sum(link[mode] for mode in self.light_modes)
        heavy_traffic = sum(link[mode] for mode in self.heavy_modes)
        reverse_link = link.reverse_link
        if reverse_link is None:
            reverse_traffic = 0.0
            reverse_heavy_traffic = 0.0
        else:
            reverse_traffic = sum(
                reverse_link[mode] for mode in self.light_modes
            )
            reverse_heavy_traffic = sum(
                reverse_link[mode] for mode in self.heavy_modes
            )

        total_light_traffic = traffic + reverse_traffic
        total_heavy_traffic = heavy_traffic + reverse_heavy_traffic
        total_traffic = total_light_traffic + total_heavy_traffic
        if total_traffic <= 0.0:
            return 0.0
        if total_light_traffic < 0.0 or total_heavy_traffic < 0.0:
            raise ValueError("Noise traffic volumes must be non-negative")

        daytime_factor = (
            assignment_param.years_average_day_factor
            * assignment_param.share_7_22_of_day
        )
        cross_light_traffic = daytime_factor * total_light_traffic
        cross_heavy_traffic = daytime_factor * total_heavy_traffic
        heavy_share = total_heavy_traffic / total_traffic

        morning_link = self.morning_network.link(
            link.i_node, link.j_node
        )
        morning_reverse_link = morning_link.reverse_link
        forward_has_traffic = traffic + heavy_traffic > 0.0
        reverse_has_traffic = (
            reverse_traffic + reverse_heavy_traffic > 0.0
        )
        if reverse_has_traffic and morning_reverse_link is None:
            raise ValueError(
                "Reverse link with traffic is missing from the morning "
                "network for link {}".format(link.id)
            )

        direction_speeds = []
        if forward_has_traffic:
            direction_speeds.append(self._speed(morning_link))
        if reverse_has_traffic:
            direction_speeds.append(self._speed(morning_reverse_link))
        speed = sum(direction_speeds) / len(direction_speeds)

        if speed >= 50.0:
            light_event_level = 73.5 + 25.0 * math.log10(speed / 50.0)
            heavy_event_level = (
                80.5 + 30.0 * math.log10(min(speed, 90.0) / 50.0)
            )
        elif speed >= 40.0:
            light_event_level = 73.5 + 25.0 * math.log10(speed / 50.0)
            heavy_event_level = 80.5
        else:
            light_event_level = 71.1
            heavy_event_level = 80.5

        start_noise = self._noise_level_from_traffic(
            light_event_level,
            heavy_event_level,
            cross_light_traffic,
            cross_heavy_traffic,
            averaging_seconds=15.0 * 3600.0,
        )

        gradient_permille = min(
            abs(morning_link["@kaltevuus"]) * 10.0, 30.0
        )
        gradient_delta = (
            (2.0 * gradient_permille) / 100.0
            + (
                3.0
                * gradient_permille
                * math.log10(1.0 + heavy_share * 100.0)
            ) / 100.0
        )
        start_noise += gradient_delta

        return self._noise_zone_distance(
            start_noise,
            threshold=55.0,
            reference_distance=zone_param.noise_reference_distance,
            near_db_per_doubling=zone_param.noise_near_db_per_doubling,
            far_db_per_doubling=zone_param.noise_far_db_per_doubling,
            transition_doublings=zone_param.noise_transition_doublings,
        )

    def _speed(self, link):
        travel_time = link[self.car_morning]
        if travel_time <= 0.0:
            return 50.0
        speed = (
            0.5 * (60.0 * link.length / travel_time)
            + 0.5 * link.data2
        )
        return speed

    @staticmethod
    def _noise_level_from_traffic(
        light_event_level,
        heavy_event_level,
        light_traffic,
        heavy_traffic,
        averaging_seconds,
    ):
        if averaging_seconds <= 0.0:
            raise ValueError("averaging_seconds must be positive")
        if light_traffic < 0.0 or heavy_traffic < 0.0:
            raise ValueError("Noise traffic volumes must be non-negative")

        acoustic_energy = 0.0
        if light_traffic > 0.0:
            acoustic_energy += (
                10.0 ** (light_event_level / 10.0)
                * light_traffic
                / averaging_seconds
            )
        if heavy_traffic > 0.0:
            acoustic_energy += (
                10.0 ** (heavy_event_level / 10.0)
                * heavy_traffic
                / averaging_seconds
            )
        if acoustic_energy == 0.0:
            return 0.0
        return 10.0 * math.log10(acoustic_energy)

    @staticmethod
    def _noise_zone_distance(
        start_noise,
        threshold,
        reference_distance,
        near_db_per_doubling,
        far_db_per_doubling,
        transition_doublings,
        max_distance=10_000.0,
    ):
        if reference_distance <= 0.0:
            raise ValueError("reference_distance must be positive")
        if near_db_per_doubling <= 0.0:
            raise ValueError("near_db_per_doubling must be positive")
        if far_db_per_doubling <= 0.0:
            raise ValueError("far_db_per_doubling must be positive")
        if transition_doublings <= 0.0:
            raise ValueError("transition_doublings must be positive")
        if max_distance < reference_distance:
            raise ValueError(
                "max_distance must be at least reference_distance"
            )

        required_attenuation = start_noise - threshold
        if required_attenuation < 0.0:
            return 0.0
        if required_attenuation == 0.0:
            return reference_distance

        def attenuation(distance):
            doublings = math.log2(distance / reference_distance)
            transition_component = (
                doublings
                - transition_doublings
                * (
                    1.0
                    - math.exp(-doublings / transition_doublings)
                )
            )
            return (
                near_db_per_doubling * doublings
                + (far_db_per_doubling - near_db_per_doubling)
                * transition_component
            )

        if attenuation(max_distance) < required_attenuation:
            return max_distance

        lower = reference_distance
        upper = max_distance
        for _ in range(60):
            midpoint = (lower + upper) / 2.0
            if attenuation(midpoint) < required_attenuation:
                lower = midpoint
            else:
                upper = midpoint
        return (lower + upper) / 2.0
