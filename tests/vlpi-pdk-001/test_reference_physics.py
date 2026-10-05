from math import isclose
from reference_model.ru001 import residual_field, phase_grid


def test_reference_model_zero_residual_for_equal_in_phase_inputs():
    r = residual_field(1 + 0j, 1 + 0j, 0.0)
    assert isclose(r.residual, 0.0, abs_tol=1e-12)
    assert isclose(r.residual_power, 0.0, abs_tol=1e-12)


def test_reference_model_changes_with_relative_phase():
    r0 = residual_field(1 + 0j, 1 + 0j, 0.0)
    rpi = residual_field(1 + 0j, 1 + 0j, 3.141592653589793)
    assert r0.residual_power < 1e-12
    assert rpi.residual_power > 1.9


def test_reference_phase_grid_is_deterministic():
    phases = phase_grid(9)
    assert len(phases) == 9
    assert isclose(phases[0], 0.0)
    assert isclose(phases[-1], 2.0 * 3.141592653589793)
