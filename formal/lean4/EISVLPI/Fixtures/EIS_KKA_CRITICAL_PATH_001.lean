/- EIS-KKA-CRITICAL-PATH-001: synthetic dependency schedule arithmetic.
   These proofs verify declared integer arithmetic only, not task dependencies,
   implementation correspondence, optical timing, energy, or physical conformance. -/
namespace EISVLPI
namespace KkaCriticalPath001

abbrev Picoseconds := Nat

def dac : Picoseconds := 10
def modulator : Picoseconds := 5
def prism : Picoseconds := 40
def thresholder : Picoseconds := 30
def kkaLane : Picoseconds := 60
def joinRouteSync : Picoseconds := 15
def photodetector : Picoseconds := 15
def adc : Picoseconds := 8
def target : Picoseconds := 200

def preKkaFinish : Picoseconds := dac + modulator + prism + thresholder
def parallelKkaFinish : Picoseconds := preKkaFinish + kkaLane
def joinedFinish : Picoseconds := parallelKkaFinish + joinRouteSync
def outputFinish : Picoseconds := joinedFinish + photodetector + adc

theorem pre_kka_finish_is_85 : preKkaFinish = 85 := by decide
theorem both_lanes_start_after_thresholder : preKkaFinish = 85 := by decide
theorem parallel_lanes_finish_at_145 : parallelKkaFinish = 145 := by decide
theorem join_finishes_at_160 : joinedFinish = 160 := by decide
theorem critical_path_is_183 : outputFinish = 183 := by decide
theorem candidate_meets_200ps_target : outputFinish <= target := by decide
theorem candidate_margin_is_17ps : target - outputFinish = 17 := by decide

end KkaCriticalPath001
end EISVLPI
