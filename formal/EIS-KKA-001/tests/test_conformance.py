"""EIS-KKA-001 scalar reference tests; run with unittest discovery."""
from __future__ import annotations
import cmath
import unittest

def cross_term(a: complex, b: complex) -> float:
    """Signed balanced-interference cross term: 2 Re(a * conjugate(b))."""
    return 2.0 * (a * b.conjugate()).real

class KKA001ConformanceTests(unittest.TestCase):
    def test_aligned_unit_fields(self):
        self.assertEqual(cross_term(1 + 0j, 1 + 0j), 2.0)

    def test_quadrature_is_zero(self):
        self.assertEqual(cross_term(1 + 0j, 0 + 1j), 0.0)

    def test_anti_aligned_is_negative(self):
        self.assertEqual(cross_term(1 + 0j, -1 + 0j), -2.0)

    def test_symmetric_in_arguments(self):
        a, b = 0.7 + 0.2j, -0.3 + 0.9j
        self.assertAlmostEqual(cross_term(a, b), cross_term(b, a), places=14)

    def test_zero_field(self):
        self.assertEqual(cross_term(0j, 0.4 - 0.8j), 0.0)
        self.assertEqual(cross_term(0.4 - 0.8j, 0j), 0.0)

    def test_phase_response(self):
        for theta in (0.0, cmath.pi / 3, cmath.pi / 2, cmath.pi):
            self.assertAlmostEqual(
                cross_term(1 + 0j, cmath.exp(1j * theta)),
                2.0 * cmath.cos(theta), places=14)

    def test_bound(self):
        a, b = 0.6 + 0.8j, 0.8 - 0.6j
        self.assertLessEqual(abs(cross_term(a, b)),
                             2.0 * abs(a) * abs(b) + 1e-14)

if __name__ == "__main__":
    unittest.main()
