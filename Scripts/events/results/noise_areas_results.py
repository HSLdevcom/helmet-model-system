from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple, Union, TYPE_CHECKING
import pandas as pd
import numpy as np

from events.model_system_event_listener import ModelSystemEventListener
from utils.zone_interval import ArrayAggregator
import utils.log as log
import parameters.zone as zone_param

if TYPE_CHECKING:
    from modelsystem import ModelSystem
    from datatypes.demand import Demand
    from datatypes.purpose import TourPurpose
    from assignment.abstract_assignment import AssignmentModel


class NoiseAreasResults(ModelSystemEventListener):
    """
    A class to analyze noise impacts.
    """
    
    def __init__(self):
        super().__init__()
    
    def on_model_system_initialized(self,
                                    model_system: 'ModelSystem',
                                    zone_data_path: str, 
                                    base_zone_data_path: str, 
                                    base_matrices_path: str,
                                    results_path: str, 
                                    assignment_model: 'AssignmentModel', 
                                    name: str) -> None:
        self.ms = model_system
    
    def on_iteration_complete(self, iteration: Union[str, int], impedance: Dict[str, Dict[str, np.ndarray]], gap: Dict[str, float]):
        if iteration=="last":
            noise_parameters = None
            if zone_param.noise_calibration_enabled:
                if (
                    len(zone_param.noise_calibration_targets) != 5
                    or any(target < 0.0 for target in zone_param.noise_calibration_targets)
                    or not np.isclose(sum(zone_param.noise_calibration_targets), 1.0)
                ):
                    raise ValueError(
                        "Noise calibration targets must be five non-negative "
                        "shares summing to 100%."
                    )
                if zone_param.noise_calibration_max_relative_weight < 1.0:
                    raise ValueError("Maximum relative noise calibration weight must be at least 1.")
                noise_parameters, shares, score, evaluations = (self._calibrate_noise_parameters())
                log.info(
                    "Noise calibration best parameters: "
                    f"{noise_parameters}; achieved shares: "
                    f"{self._format_shares(shares)}; target shares: "
                    f"{self._format_shares(zone_param.noise_calibration_targets)}; "
                    f"weighted sum squared share error: {score:.8f}; "
                    f"evaluations: {evaluations}"
                )
                parameters_at_bounds = [
                    name
                    for name, value in noise_parameters.items()
                    if value in zone_param.noise_calibration_bounds[name]
                ]
                if parameters_at_bounds:
                    log.warn(
                        "Best noise calibration parameter(s) reached a search "
                        "bound: "
                        f"{', '.join(parameters_at_bounds)}. Consider widening "
                        "the configured bounds if the achieved shares are not "
                        "close enough to the targets."
                    )
            self._calculate_noise_areas(noise_parameters)

    @staticmethod
    def _format_shares(shares: Tuple[float, ...]) -> str:
        bands = ("55-59", "60-64", "65-69", "70-74", "75+")
        return ", ".join(
            f"{band}: {share:.2%}" for band, share in zip(bands, shares)
        )

    @staticmethod
    def _exclusive_noise_areas(cumulative_areas: Tuple[pd.Series, ...]) -> Dict[str, pd.Series]:
        if len(cumulative_areas) != 6:
            raise ValueError(
                "Noise calculation must return cumulative contours at "
                "50, 55, 60, 65, 70, and 75 dB."
            )
        (
            area_50_plus,
            area_55_plus,
            area_60_plus,
            area_65_plus,
            area_70_plus,
            area_75_plus,
        ) = cumulative_areas
        return {
            "50_54": area_50_plus - area_55_plus,
            "55_59": area_55_plus - area_60_plus,
            "60_64": area_60_plus - area_65_plus,
            "65_69": area_65_plus - area_70_plus,
            "70_74": area_70_plus - area_75_plus,
            "75_plus": area_75_plus,
        }

    def _population_shares(self, noise_areas) -> Tuple[float, ...]:
        exclusive_areas = self._exclusive_noise_areas(noise_areas)
        area_aggregator = ArrayAggregator(
            self.ms.zdata_forecast.zone_numbers
        )
        population = area_aggregator.aggregate(
            self.ms.zdata_forecast["population"]
        )
        conversion = pd.Series(zone_param.pop_share_per_noise_area)
        selected_areas = list(zone_param.noise_calibration_areas)
        # Calibration targets cover all five bands at 55 dB and above.
        population_by_band = (
            conversion * exclusive_areas[band] * population
            for band in (
                "55_59",
                "60_64",
                "65_69",
                "70_74",
                "75_plus",
            )
        )
        counts = tuple(
            float((band_population.loc[selected_areas]).sum())
            for band_population in population_by_band
        )
        total = sum(counts)
        if total <= 0.0:
            raise ValueError(
                "Cannot calibrate noise shares: population in the selected "
                "55 dB and above is zero."
            )
        return tuple(count / total for count in counts)

    def _calibrate_noise_parameters(self) -> Tuple[Dict[str, float], Tuple[float, ...], float, int]:
        parameter_names = (
            "near_db_per_doubling",
            "far_db_per_doubling",
            "transition_doublings",
        )
        initial = {
            "near_db_per_doubling": zone_param.noise_near_db_per_doubling,
            "far_db_per_doubling": zone_param.noise_far_db_per_doubling,
            "transition_doublings": zone_param.noise_transition_doublings,
        }

        def evaluate(parameters: Dict[str, float]):
            noise_areas = self.ms.ass_model.calc_noise(**parameters)
            shares = self._population_shares(noise_areas)
            return 0.0, shares

        def score_for_shares(shares: Tuple[float, ...]):
            weights = _adaptive_share_weights(
                shares,
                zone_param.noise_calibration_targets,
                zone_param.noise_calibration_max_relative_weight,
            )
            return _weighted_share_error(
                shares, zone_param.noise_calibration_targets, weights
            )

        parameters, shares, score, evaluations = _coordinate_search(
            evaluate=evaluate,
            initial=initial,
            bounds=zone_param.noise_calibration_bounds,
            parameter_names=parameter_names,
            grid_points=zone_param.noise_calibration_grid_points,
            passes=zone_param.noise_calibration_passes,
            score_for_shares=score_for_shares,
        )
        return parameters, shares, score, evaluations

    def _calculate_noise_areas(self, noise_parameters: Optional[Dict[str, float]] = None) -> None:
        if noise_parameters is None:
            cumulative_areas = self.ms.ass_model.calc_noise()
        else:
            cumulative_areas = self.ms.ass_model.calc_noise(**noise_parameters)
        exclusive_areas = self._exclusive_noise_areas(cumulative_areas)
        for band in ("50_54", "55_59", "60_64", "65_69", "70_74", "75_plus"):
            self.ms.resultdata.print_data(
                exclusive_areas[band], "noise_areas.txt", f"area_{band}_dB"
            )
        ar = ArrayAggregator(self.ms.zdata_forecast.zone_numbers)
        pop = ar.aggregate(self.ms.zdata_forecast["population"])
        conversion = pd.Series(zone_param.pop_share_per_noise_area)
        noise_population = {
            band: conversion * area * pop
            for band, area in exclusive_areas.items()
        }
        noise_pop_total = sum(noise_population.values())
        for band, population_in_band in noise_population.items():
            self.ms.resultdata.print_data(
                population_in_band, "noise_areas.txt", f"population_{band}_dB"
            )
        self.ms.resultdata.print_data(noise_pop_total, "noise_areas.txt", "population_total")


def _weighted_share_error(
    actual: Tuple[float, ...],
    target: Tuple[float, ...],
    weights: Tuple[float, ...],
) -> float:
    if not (len(actual) == len(target) == len(weights)):
        raise ValueError(
            "Noise calibration shares, targets, and weights must have equal lengths."
        )
    if any(weight <= 0.0 for weight in weights):
        raise ValueError("Noise calibration weights must be positive.")
    return sum(
        weight * (observed - desired) ** 2
        for observed, desired, weight in zip(actual, target, weights)
    )


def _adaptive_share_weights(
    actual: Tuple[float, ...],
    target: Tuple[float, ...],
    maximum_weight: float,
) -> Tuple[float, ...]:
    if len(actual) != len(target):
        raise ValueError(
            "Noise calibration shares and targets must have equal lengths."
        )
    if maximum_weight < 1.0:
        raise ValueError("Maximum noise calibration weight must be at least 1.")
    if any(value <= 0.0 for value in target):
        raise ValueError("Noise calibration target shares must be positive.")
    return tuple(
        min(
            maximum_weight,
            max(observed / desired, desired / max(observed, 1e-12)),
        )
        for observed, desired in zip(actual, target)
    )


def _coordinate_search(
    evaluate: Callable[[Dict[str, float]], Tuple[float, Tuple[float, ...]]],
    initial: Dict[str, float],
    bounds: Dict[str, Tuple[float, float]],
    parameter_names: Tuple[str, ...],
    grid_points: int,
    passes: int,
    score_for_shares: Optional[Callable[[Tuple[float, ...]], float]] = None,
) -> Tuple[Dict[str, float], Tuple[float, ...], float, int]:
    if grid_points < 3:
        raise ValueError("Noise calibration grid_points must be at least 3.")
    if passes < 1:
        raise ValueError("Noise calibration passes must be positive.")

    current = dict(initial)
    intervals = {}
    for name in parameter_names:
        lower, upper = bounds[name]
        if lower >= upper:
            raise ValueError(f"Invalid noise calibration bounds for {name}.")
        current[name] = min(max(current[name], lower), upper)
        intervals[name] = (lower, upper)

    cache = {}

    def score(parameters):
        key = tuple((name, parameters[name]) for name in parameter_names)
        if key not in cache:
            cache[key] = evaluate(parameters)
        initial_score, shares = cache[key]
        if score_for_shares is None:
            return initial_score, shares
        return score_for_shares(shares), shares

    current_score, current_shares = score(current)
    for _ in range(passes):
        for name in parameter_names:
            lower, upper = intervals[name]
            points = np.linspace(lower, upper, grid_points).tolist()
            points.append(current[name])
            points = sorted(set(points))
            best_index = min(
                range(len(points)),
                key=lambda index: abs(points[index] - current[name]),
            )
            for index, value in enumerate(points):
                candidate = dict(current)
                candidate[name] = value
                candidate_score, candidate_shares = score(candidate)
                if candidate_score < current_score:
                    current = candidate
                    current_score = candidate_score
                    current_shares = candidate_shares
                    best_index = index

            intervals[name] = (
                points[max(0, best_index - 1)],
                points[min(len(points) - 1, best_index + 1)],
            )

    return current, current_shares, current_score, len(cache)