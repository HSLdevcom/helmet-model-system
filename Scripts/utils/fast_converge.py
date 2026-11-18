"""Temporary car-impedance relaxation for the demand/assignment feedback loop."""


class FastConvergence:
    """Use 50/50 feedback until the normal demand-gap thresholds first pass."""

    def __init__(self, enabled=False):
        self.active = enabled
        self.enabled = enabled

    def update(self, previous, assigned, thresholds_met, is_final=False):
        """Return next feedback and whether convergence may stop the run.

        The first threshold pass releases the raw assignment impedances. A
        subsequent, unrelaxed iteration must pass before the run can stop.
        """
        if not self.active:
            return assigned, thresholds_met
        if thresholds_met:
            self.active = False
            return assigned, False
        if is_final:
            return assigned, False
        for period, matrix_types in assigned.items():
            for matrix_type, classes in matrix_types.items():
                old_classes = previous[period][matrix_type]
                for car_class in ("car_work", "car_leisure"):
                    if car_class in classes:
                        classes[car_class] = (
                            0.5 * old_classes[car_class]
                            + 0.5 * classes[car_class]
                        )
        return assigned, False
