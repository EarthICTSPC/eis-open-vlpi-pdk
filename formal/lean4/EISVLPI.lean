import EISVLPI.Fixtures.EIS_CRC_BUDGET_001
import EISVLPI.Fixtures.EIS_KKA_CRITICAL_PATH_001

/-!
# EIS VLPI formal foundation

This is the Lean 4 entry point for machine-checkable definitions and proofs
supporting Earth ICT, SPC's open VLPI contracts. Keep formal claims distinct
from simulation or measurement evidence.
-/

namespace EISVLPI

/-- Semantic meaning is distinct from the physical representation domain. -/
inductive Domain where
  | electronicDigital
  | electronicAnalog
  | photonicOpticalField
  | photonicOpticalPower
  deriving DecidableEq, Repr

/-- An in-flight optical field may carry semantically digital information.
This does not imply an electronic representation or an O/E/O crossing. -/
def inFlightRepresentation : Domain := .photonicOpticalField

/-- Latency values in this initial formal foundation are integer picoseconds. -/
abbrev Picoseconds := Nat

theorem in_flight_representation_is_optical_field :
    inFlightRepresentation = .photonicOpticalField := by
  rfl

end EISVLPI
