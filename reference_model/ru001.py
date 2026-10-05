"""RU-001 executable reference field model.

This is a mathematical reference model for agent experimentation.
It is not a calibrated device model and does not claim EM, fabrication,
measurement, or foundry validity.
"""

from cmath import exp, pi
from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class RU001Result:
    residual: complex
    residual_power: float
    phase_rad: float


def residual_field(a: complex, b: complex, phase_rad: float = 0.0) -> RU001Result:
    """Evaluate a balanced two-field residual reference transformation.

    The model represents the conceptual field operation
        r = (a - exp(i*phi)*b) / sqrt(2)
    used only as an executable information/physics reference.
    """
    r = (a - exp(1j * phase_rad) * b) / sqrt(2.0)
    return RU001Result(r, abs(r) ** 2, phase_rad)


def sweep_phase(a: complex, b: complex, phases):
    return [residual_field(a, b, p) for p in phases]


def phase_grid(count: int = 9):
    if count < 2:
        raise ValueError("count must be >= 2")
    return [2.0 * pi * i / (count - 1) for i in range(count)]
