import PositiveGeometryEmergentSpaceTime.Surf1.Enum
open PositiveGeometryEmergentSpaceTime.Surf1
def boxU : G := ⟨[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11], [12, 13, 14], [15, 16, 17]],
  [(2, 5), (7, 11), (10, 14), (13, 17), (16, 8), (0, 6), (3, 9), (1, 12), (4, 15)]⟩
def ttU : G := ⟨[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]], [(2, 5), (8, 11), (0, 6), (3, 9), (1, 7), (4, 10)]⟩
#eval W1 ttU
#eval W1 boxU
#eval (List.range 64).map (fun o => ovec boxU o (hiW boxU) (lenW boxU))
