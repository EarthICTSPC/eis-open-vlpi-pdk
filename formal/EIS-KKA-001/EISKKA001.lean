/-!
EIS-KKA-001 — Interference Operator and Physical-Response Contract
Version: 0.1.0
Status: specified / software-reference only; not hardware-validated.

For fields a=(ar,ai), b=(br,bi), freeze the signed cross term:
  X(a,b) = 2 * (ar*br + ai*bi) = 2 Re(a * conjugate(b)).
The factor of two is intentional. This is a scalar primitive, not a complete
attention/KKA definition and not a model of a particular photonic PDK.
-/
namespace EISKKA001

structure Field where
  re : Int
  im : Int
  deriving DecidableEq, Repr

def zeroField : Field := ⟨0, 0⟩

def crossTerm (a b : Field) : Int :=
  2 * (a.re * b.re + a.im * b.im)

def intensity (a : Field) : Int :=
  a.re * a.re + a.im * a.im

theorem crossTerm_comm (a b : Field) : crossTerm a b = crossTerm b a := by
  simp [crossTerm, Int.mul_comm, Int.add_comm]

theorem crossTerm_zero_right (a : Field) :
    crossTerm a zeroField = 0 := by
  simp [crossTerm, zeroField]

theorem crossTerm_zero_left (a : Field) :
    crossTerm zeroField a = 0 := by
  simp [crossTerm, zeroField]

/-- Aligned unit fields produce the +2 cross term. -/
def alignedUnit : Field := ⟨1, 0⟩
/-- Quadrature fields have zero cross term. -/
def quadratureUnit : Field := ⟨0, 1⟩
/-- Anti-aligned unit fields produce the -2 cross term. -/
def antiAlignedUnit : Field := ⟨-1, 0⟩

#eval crossTerm alignedUnit alignedUnit
#eval crossTerm alignedUnit quadratureUnit
#eval crossTerm alignedUnit antiAlignedUnit

end EISKKA001
