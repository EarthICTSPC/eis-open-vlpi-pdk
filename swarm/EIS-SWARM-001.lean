import Std

namespace EIS.SWARM001

inductive EvidenceClass
  | mathematical
  | executable
  | physical
deriving DecidableEq, Repr

inductive Domain
  | vlsi
  | vlpi
  | hybrid
  | fabrication
  | system
deriving DecidableEq, Repr

structure Agent where
  id : String
  domain : Domain
  capability : String
  inputs : List String
  outputs : List String
  evidence : EvidenceClass
deriving Repr

def admissible (a : Agent) : Prop :=
  a.evidence = EvidenceClass.mathematical ∨
  a.evidence = EvidenceClass.executable

def independentVerification (generator verifier : Agent) : Prop :=
  generator.id ≠ verifier.id

def selected : List Agent :=
  [ { id := "A_FIELD", domain := .vlpi, capability := "COMPLEX_FIELD",
      inputs := ["E_in1", "E_in2", "phase_rad"],
      outputs := ["E_out1", "E_out2"], evidence := .mathematical }
  , { id := "A_RESIDUAL", domain := .vlpi, capability := "RESIDUAL_INTENSITY",
      inputs := ["E_out2"], outputs := ["r"], evidence := .mathematical }
  , { id := "A_ENERGY", domain := .vlpi, capability := "ENERGY_CONSERVATION",
      inputs := ["E_out1", "E_out2"], outputs := ["energy_ok"], evidence := .mathematical }
  , { id := "A_SWEEP", domain := .vlpi, capability := "PHASE_SWEEP",
      inputs := ["phase_list", "field_results", "residual_results"],
      outputs := ["sweep_results"], evidence := .executable }
  , { id := "A_INVARIANT", domain := .vlpi, capability := "INVARIANT_CHECK",
      inputs := ["sweep_results", "energy_results"], outputs := ["ok"],
      evidence := .mathematical }
  ]

def selectedAllAdmissible : Prop :=
  ∀ a, a ∈ selected → admissible a

theorem selected_all_admissible : selectedAllAdmissible := by
  intro a ha
  simp [selected] at ha
  rcases ha with rfl | rfl | rfl | rfl | rfl <;> simp [admissible]

end EIS.SWARM001
