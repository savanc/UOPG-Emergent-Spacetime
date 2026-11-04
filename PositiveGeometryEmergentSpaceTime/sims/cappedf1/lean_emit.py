"""Emit lean/PositiveGeometryEmergentSpaceTime/CappedFormanCerts.lean: exact lazy-Ollivier certificates (CAPPED-FORMAN-1, 2026-10-31).
Graphs: prism C_7 x K2, prism C_8 x K2, truncated cube (networkx.truncated_cube_graph). For one edge of each class:
upper bound = explicit walk-realised perfect matching between closed neighbourhoods; lower bound = integer 1-Lipschitz
potential from the Kantorovich-Rubinstein LP (HiGHS, rounded, re-verified here and by Lean `decide +kernel`)."""
import networkx as nx, numpy as np, itertools, sys
from scipy.optimize import linear_sum_assignment, linprog
from fractions import Fraction as Fr

def prism(k):
    G = nx.Graph()
    for i in range(k):
        G.add_edge(i, (i+1) % k); G.add_edge(k+i, k+(i+1) % k); G.add_edge(i, k+i)
    return G

def cert(G, a, b):
    nodes = sorted(G); idx = {v: i for i, v in enumerate(nodes)}
    d = dict(nx.all_pairs_shortest_path_length(G))
    NA = [a] + sorted(G[a]); NB = [b] + sorted(G[b])
    C = np.array([[d[x][y] for y in NB] for x in NA])
    r, c = linear_sum_assignment(C); cost = int(C[r, c].sum())
    ws = []
    for i, j in zip(r, c):
        p = nx.shortest_path(G, NA[i], NB[j]); ws.append((p[0], p[1:]))
    n = len(nodes); obj = np.zeros(n)
    for x in NA: obj[idx[x]] -= 1
    for y in NB: obj[idx[y]] += 1
    A = []; rhs = []
    for u, v in G.edges():
        for s, t in ((u, v), (v, u)):
            row = np.zeros(n); row[idx[s]] = 1; row[idx[t]] = -1; A.append(row); rhs.append(1)
    bounds = [(0, 0) if i == 0 else (None, None) for i in range(n)]
    res = linprog(obj, A_ub=np.array(A), b_ub=rhs, bounds=bounds, method='highs')
    phi = [int(round(x)) for x in res.x]
    assert all(abs(phi[i]-res.x[i]) < 1e-9 for i in range(n))
    assert all(abs(phi[idx[u]]-phi[idx[v]]) <= 1 for u, v in G.edges())
    gap = sum(phi[idx[x]] for x in NA) - sum(phi[idx[y]] for y in NB)
    assert gap == cost, (gap, cost)
    return nodes, NA, NB, ws, phi, cost

def emit_block(tag, G, a, b, D, ks, out):
    nodes, NA, NB, ws, phi, cost = cert(G, a, b)
    assert nodes == list(range(len(nodes)))
    n = len(nodes); Bv = 1 - Fr(sum(min(3, k-3) for k in ks), D+1)
    assert 1 - Fr(cost, D+1) == Bv, (tag, cost, Bv)
    nb = [sorted(G[v]) for v in nodes]
    ns = f"PositiveGeometryEmergentSpaceTime.CappedFormanCerts.{tag}"
    out.append(f"""
/-! ## {tag}: edge ({a}, {b}), 2-faces through it of sizes {ks}, D = {D}; matching cost {cost}, κ = 1 − {cost}/{D+1} = {Bv} = B -/
namespace {tag}
abbrev V := Fin {n}
def nbrT : List (List Nat) := {nb}
def nbrs (i : V) : List V := (nbrT.getD i.val []).map fun j => (Fin.ofNat {n} j)
def adj (i j : V) : Bool := (nbrs i).contains j
/-- Symmetric, loop-free, {D}-regular adjacency. -/
theorem adj_ok : ∀ i j : V, (adj i j = adj j i) ∧ adj i i = false ∧ (nbrs i).length = {D} := by decide +kernel
def NA : List V := {NA}
def NB : List V := {NB}
theorem nbhd : NA = {a} :: nbrs {a} ∧ NB = {b} :: nbrs {b} ∧ adj {a} {b} = true := by decide +kernel
def ws : List (V × List V) := {[(x, p) for x, p in ws]}
def phi (i : V) : Int := ({phi} : List Int).getD i.val 0
theorem phi_lip : ∀ i : V, (nbrs i).all (fun j => decide (phi i - phi j ≤ 1)) = true := by decide +kernel
theorem phi_gap : (NA.map phi).sum - (NB.map phi).sum = {cost} := by decide +kernel
theorem ws_ok : (ws.all fun p => walkOk adj (p.1 :: p.2)) = true ∧ (ws.map Prod.fst).Perm NA ∧
    (ws.map fun p => fin p.1 p.2).Perm NB ∧ (ws.map fun p => (p.2.length : Int)).sum = {cost} := by
  refine ⟨by decide +kernel, ?_, ?_, by decide +kernel⟩ <;> exact List.perm_iff_count.mpr (by decide +kernel)
/-- Minimum walk-realised perfect-matching cost between the closed neighbourhoods is exactly {cost}. -/
theorem cost_exact :
    (∃ ws : List (V × List V), (∀ p ∈ ws, walkOk adj (p.1 :: p.2) = true) ∧ (ws.map Prod.fst).Perm NA ∧
      (ws.map fun p => fin p.1 p.2).Perm NB ∧ (ws.map fun p => (p.2.length : Int)).sum = {cost}) ∧
    (∀ ws : List (V × List V), (∀ p ∈ ws, walkOk adj (p.1 :: p.2) = true) → (ws.map Prod.fst).Perm NA →
      (ws.map fun p => fin p.1 p.2).Perm NB → {cost} ≤ (ws.map fun p => (p.2.length : Int)).sum) := by
  obtain ⟨h1, h2, h3, h4⟩ := ws_ok
  refine ⟨⟨ws, fun p hp => List.all_eq_true.mp h1 p hp, h2, h3, h4⟩, ?_⟩
  intro ws hw hA hB
  have hl : ∀ i j : V, adj i j = true → phi i - phi j ≤ 1 := by
    intro i j hij
    have := List.all_eq_true.mp (phi_lip i) j (by simpa [adj] using hij)
    simpa using this
  have := cost_lower adj phi hl ws hw
  rw [(hA.map phi).sum_eq, (hB.map phi).sum_eq, phi_gap] at this
  exact this
/-- κ = 1 − cost/(D+1) equals the capped-Forman bound B = 1 − Σ min(3, k−3)/(D+1). -/
theorem kappa_eq_B : (1 : ℚ) - {cost} / {D+1} = 1 - (({' + '.join(f'min 3 ({k} - 3)' for k in ks)} : ℕ) : ℚ) / {D+1} := by norm_num
end {tag}""")
    return (tag, a, b, ks, cost, str(Bv))

out = ["""import PositiveGeometryEmergentSpaceTime.CappedForman

/-!
# CappedFormanCerts — exact lazy-Ollivier certificates for the capped-Forman equality (CAPPED-FORMAN-1, 2026-10-31)

For one edge of each edge class of the prisms C_7 × K_2, C_8 × K_2 (2-faces: the two k-gons and k squares) and the
truncated cube (triangles and octagons), `cost_exact` proves that the minimum walk-realised perfect-matching cost between
the closed neighbourhoods (uniform, idleness 1/(D+1)) is exactly the stated integer, and `kappa_eq_B` that
κ = 1 − cost/(D+1) equals B = 1 − Σ min(3, k−3)/(D+1). These are the k ≥ 7 cases where the cap is active.
Edge-transitivity within each class (prism / truncated-cube symmetry) is not formalised: each certificate is for the
named edge. Scope as in `PositiveGeometryEmergentSpaceTime.HgDim2P4`: fractional couplings reduce to matchings (Birkhoff, cited, not formalised).
Generated by sims/cappedf1/lean_emit.py.
-/

namespace PositiveGeometryEmergentSpaceTime.CappedFormanCerts
open PositiveGeometryEmergentSpaceTime.HgDim2
"""]
rows = []
for k in (7, 8):
    G = prism(k)
    rows.append(emit_block(f"Prism{k}H", G, 0, 1, 3, (4, k), out))   # k-gon edge: square + k-gon
    rows.append(emit_block(f"Prism{k}V", G, 0, k, 3, (4, 4), out))   # vertical: two squares
T = nx.convert_node_labels_to_integers(nx.truncated_cube_graph(), ordering='sorted')
tri = set()
for u, v in T.edges():
    if set(T[u]) & set(T[v]): tri.add((u, v))
e38 = min(tri); e88 = min(e for e in T.edges() if e not in tri)
rows.append(emit_block("TCubeTriOct", T, e38[0], e38[1], 3, (3, 8), out))
rows.append(emit_block("TCubeOctOct", T, e88[0], e88[1], 3, (8, 8), out))
out.append("\nend PositiveGeometryEmergentSpaceTime.CappedFormanCerts\n")
open(sys.argv[1], 'w').write("\n".join(out))
for r in rows: print(r)
