/-!
EIS-KKA-EW4All-001 — Lean 4 research contract
Version: 0.1.0
Status: proposed formal contract; compilation pending CI/reviewer execution.

Formalizes exact integer cross-term semantics, forecast horizons, input
availability and future-target temporal boundaries, and separate evidence
claim classes. It does NOT prove meteorological validity, dataset quality,
model performance, operational readiness, photonic feasibility, or energy
savings.
-/
namespace EISKKA_EW4All001

structure Field where
  re : Int
  im : Int
  deriving DecidableEq, Repr

def crossTerm (a b : Field) : Int :=
  2 * (a.re * b.re + a.im * b.im)

theorem crossTerm_comm (a b : Field) :
    crossTerm a b = crossTerm b a := by
  simp [crossTerm, Int.mul_comm, Int.add_comm]

def zeroField : Field := ⟨0, 0⟩

theorem crossTerm_zero_right (a : Field) :
    crossTerm a zeroField = 0 := by
  simp [crossTerm, zeroField]

theorem crossTerm_zero_left (a : Field) :
    crossTerm zeroField a = 0 := by
  simp [crossTerm, zeroField]

def alignedUnit : Field := ⟨1, 0⟩
def quadratureUnit : Field := ⟨0, 1⟩
def antiAlignedUnit : Field := ⟨-1, 0⟩

theorem aligned_fixture :
    crossTerm alignedUnit alignedUnit = 2 := by
  rfl

theorem quadrature_fixture :
    crossTerm alignedUnit quadratureUnit = 0 := by
  rfl

theorem anti_aligned_fixture :
    crossTerm alignedUnit antiAlignedUnit = -2 := by
  rfl

inductive ForecastHorizon where
  | min30
  | min60
  | min120
  deriving DecidableEq, Repr

def horizonMinutes : ForecastHorizon → Nat
  | .min30 => 30
  | .min60 => 60
  | .min120 => 120

theorem horizons_are_positive (h : ForecastHorizon) :
    0 < horizonMinutes h := by
  cases h <;> decide

/-- Times are integer minutes on a single documented timeline. -/
structure TimedInput where
  availableAt : Int
  validAt : Int
  deriving Repr

/-- An input may be used only if it was actually available by issue time.
    validAt alone does not establish availability. -/
def inputAvailable (issueTime : Int) (x : TimedInput) : Prop :=
  x.availableAt ≤ issueTime

/-- Forecast target windows begin strictly after issue time. -/
def targetIsFuture (issueTime targetStart : Int) : Prop :=
  issueTime < targetStart

theorem admissible_input_not_late
    (issueTime : Int) (x : TimedInput)
    (h : inputAvailable issueTime x) :
    x.availableAt ≤ issueTime := by
  exact h

theorem target_strictly_future
    (issueTime targetStart : Int)
    (h : targetIsFuture issueTime targetStart) :
    issueTime < targetStart := by
  exact h

/-- Forecast, operational readiness and photonic energy evidence are distinct. -/
inductive ClaimClass where
  | forecastQuality
  | operationalReadiness
  | photonicEnergy
  deriving DecidableEq, Repr

structure EvidenceRecord where
  forecastEvidence : Bool
  operationalEvidence : Bool
  photonicEnergyEvidence : Bool
  deriving DecidableEq, Repr

def supportsClaim (e : EvidenceRecord) : ClaimClass → Bool
  | .forecastQuality => e.forecastEvidence
  | .operationalReadiness => e.operationalEvidence
  | .photonicEnergy => e.photonicEnergyEvidence

theorem no_implicit_claim_promotion
    (e : EvidenceRecord)
    (hForecastOnly : e.forecastEvidence = true)
    (hNoOperational : e.operationalEvidence = false)
    (hNoEnergy : e.photonicEnergyEvidence = false) :
    supportsClaim e .forecastQuality = true ∧
    supportsClaim e .operationalReadiness = false ∧
    supportsClaim e .photonicEnergy = false := by
  simp [supportsClaim, hForecastOnly, hNoOperational, hNoEnergy]

end EISKKA_EW4All001
