#!/usr/bin/env python3
"""Lean parameter/definition glossary + overlap analysis (2026-10-15).
Read-only. Does not change theorems or credit. Leaves AUTORESEARCH-STOP alone.

Sources of truth for status:
  - graph/analysis.json recurring_params (review keyword hits: free/fixed/input)
  - notes/EXCLUSION-LEDGER.md (no-gos that rule out SM lines)
  - Lean docstrings for meaning ([DOC]); curated only when a quantity is named in a
    known module+binder table ([CURATED]); otherwise 'unknown' (never guessed).
'input' in analysis.json is reported as 'cited' (literature/data; not geometry-fixed).
"""
from __future__ import annotations
import json, re, csv, collections, pathlib
import networkx as nx
R = pathlib.Path(__file__).resolve().parents[1]
decls = [json.loads(l) for l in open(R/'graph/raw_decls.jsonl')]
decls = [d for d in decls if d['kind'] in ('thm', 'def')]
T = json.load(open(R/'graph/theorems.json'))
A = json.load(open(R/'graph/analysis.json'))
comp_of = {n['name']: n.get('component') for n in T['nodes']}
credit_of = {n['name']: bool((n.get('overlay') or {}).get('credit')) for n in T['nodes']}
short = lambda m: m.split('.', 1)[1] if '.' in m else m
AUX = re.compile(r'\.(mk|noConfusion|noConfusionType|rec|recOn|casesOn|ctorIdx|injEq|sizeOf_spec|brecOn|below)$|_match_|_proof_|\.inst[A-Z]')
GENERIC_DOC = re.compile(r'^Auxiliary definition `')

# analysis.json: param -> {status_counts, modules}; map input→cited
REC = A.get('recurring_params', {})
REC_ALIAS = {  # normalize analysis keys to glossary quantity ids
    'scale': 'scale (dimensionful unit)',
    'couplings(g,lambda)': 'couplings g / lambda',
    'shift ansatz': 'shift ansatz (NLSM δ / mesh)',
    'LECs(L_i,l_i)': 'LECs L_i / l_i',
    'm_pi': 'm_π', 'm_rho': 'm_ρ', 'm_K': 'm_K', 'Nc': 'N_c',
    'f_pi': 'f_π', 'sigma-term': 'σ-term', 'curvature c': 'dispersion curvature c',
    'alpha_prime': "α' (Regge slope)", 'vev': 'vev v', 'theta_W': 'θ_W',
    'spurion/quark mass': 'spurion / quark mass',
}
# Module → quantity → preferred status (majority in analysis; EXCLUSION overrides for free)
MOD_Q: dict[str, dict[str, str]] = collections.defaultdict(dict)
for k, info in REC.items():
    qid = REC_ALIAS.get(k, k)
    sc = info.get('status_counts', {})
    # majority status; input→cited
    maj = max(sc, key=sc.get) if sc else 'unknown'
    status = {'input': 'cited', 'free': 'free', 'fixed': 'fixed'}.get(maj, 'unknown')
    for M in info.get('modules', []):
        MOD_Q[M][qid] = status
# EXCLUSION overrides: scale and N_c remain free (no-go)
for M in ('BR4', 'ScaleNoGo', 'SG1', 'SG1b', 'PG1', 'OrderParameter'):
    MOD_Q[M]['scale (dimensionful unit)'] = 'free'
for M in ('STRUCT2', 'MassiveLS', 'SC1'):
    MOD_Q[M]['N_c'] = 'free'  # STRUCT-2: only odd N selected
# 2026-10-20 (H4, approved by the author): GB1a removed from the N_c override. `N` in GB1a is the glueball level
# index (notes/LEAN-NAMING-MAP-2026-10-15.md, Deferred table: "Glueball level index ... not N_c"); see BINDER_OVERRIDE.
MOD_Q['GB1a'].pop('N_c', None)
MOD_Q['FL1Z'].pop('LECs L_i / l_i', None)  # FL-1Z 2026-10-22: keyword false positive (planted-test labels L1..L4), no ChPT LECs
MOD_Q['STRUCT1']['hypercharges y_i'] = 'fixed'
MOD_Q['STRUCT1b']['hypercharges y_i'] = 'fixed'  # Majorana restores; Dirac free family
MOD_Q['STRUCT1']['anomaly_canonical_residue'] = 'free'
MOD_Q['STRUCT1']['ew_from_pion_geometry'] = 'free'
MOD_Q['STRUCT1']['geometry_struct_separation'] = 'free'
MOD_Q['STRUCT2']['N_gen'] = 'free'
MOD_Q['STRUCT2']['anomaly_canonical_residue'] = 'free'
MOD_Q['Spinor']['chirality_orientation'] = 'free'
MOD_Q['Separation']['geometry_struct_separation'] = 'fixed'  # R5: Lean bundle, NO-LINK accepted
MOD_Q['Separation']['ew_from_pion_geometry'] = 'free'  # R4: no candidate; pi0 bridge N_c-blind
MOD_Q['Separation']['N_c'] = 'free'
MOD_Q.setdefault('R4Indep', {})['ew_from_pion_geometry'] = 'free'  # R4-indep 2026-10-16: 5 angles killed
MOD_Q['Separation']['hypercharges y_i'] = 'fixed'
MOD_Q['FRMU']['N_c'] = 'fixed'  # FR-MU uses N_c = 3 as a zero-parameter input
MOD_Q['FRMU']['hypercharges y_i'] = 'fixed'  # STRUCT-2 branch charges
MOD_Q.setdefault('FRWZW', {})['N_c'] = 'free'  # FR-WZW: odd 5-pt normalisation free
MOD_Q.setdefault('FDim', {})['spacetime dimension D'] = 'free'  # F-DIM: bounded (D<=4), not forced
MOD_Q.setdefault('FRhoWidth', {})['rho width ratio Gamma/m'] = 'fixed'  # F-RHOWIDTH: LS/KSRF = (2/pi)(1-x^2), FAIL
MOD_Q.setdefault('FDeltaNLSM', {})["stringy NLSM shift alpha'delta"] = 'free'  # F-POSGEOM-DAUGHTER: alpha'delta in (0,1) unfixed -> ILL-DEFINED; tachyon m^2=-delta every member
MOD_Q.setdefault('BridgePLCharge', {})['U(1) charge vector (hypercharge) via column torus'] = 'free'  # BRIDGE-PL-ASSOC: chain charge-blind (M1), M2 unearned -> NO-LINK
MOD_Q.setdefault('STRUCTNGen', {})['N_gen'] = 'free'  # STRUCT-NGEN: SM consistency window {1..5}; exactly 3 only with gauged triality or 3-3-1 rival
MOD_Q.setdefault('IntChamber', {})['kinematic ratio mu = c13p/c14p'] = 'free'  # INT-1 2026-10-22: face-lattice integers chamber-constant; mu free/dense -> P1 closed
MOD_Q.setdefault('GradedPositroid', {})['Cartan-weight grading (H3, H8\', T3, Y) of positroid columns'] = 'free'  # GRADED-POSITROID: graded m1/m3 <=> ACC exactly; NO-LINK
MOD_Q.setdefault('TrialityWhy', {})['N_gen'] = 'free'  # TRIALITY-WHY 2026-10-23: B3 linear anomaly == exactness (tautology); QG dichotomy broken by QQQL -> window {1..5}; NOT-FORCED / NO-GO
MOD_Q.setdefault('FL1Z', {})['neutrino ratio rho = dm2sol/dm2atm'] = 'free'  # FL-1Z 2026-10-22: tau=omega excluded (rank 1); rho varies with free |tau-omega| and b_k -> NOT-WELL-POSED
MOD_Q.setdefault('FScatLen', {})['S-wave pi-pi scattering lengths a0^0, a0^2'] = 'fixed'  # F-SCATLEN: P_b repair excluded (a02 = 0 exactly)
MOD_Q.setdefault('FDimMass', {})['LS intercept alpha0 at physical m_pi'] = 'free'  # F-DIM-MASS: Adler-line baseline fails D=4; P_b repair at cost
MOD_Q.setdefault('FCoulomb', {})['mass ratios'] = 'free'  # F-COULOMB 2026-10-20: deformed positivity leaves ratios continuous
MOD_Q.setdefault('LeanCert', {})['GPOS anomaly-free count N_ACC (yQ = 1)'] = 'fixed'  # LEAN-CERT-1 2026-10-23: N_ACC = 2 PROVED (nacc_eq_two); was SIMULATED
MOD_Q.setdefault('LeanCert2', {})['FR-WZW parity-odd count dim ker M_{k,sigma} (k = 0, 1)'] = 'fixed'  # LEAN-CERT-2 2026-10-28: k = 0,1 counts kernel-checked (1, 0, 2, 0); k = 2, 3 memory LIMIT (stay SIMULATED); rung verdict ILL-DEFINED (null N2 mis-specified)
MOD_Q.setdefault('Jord1', {})['gauge-group type: g_sm = stab(E1) ∩ setstab(h3(C)) as a positivity (pointwise-stabiliser) closure'] = 'free'  # JORD-1 2026-10-28: g_sm is not stab(S) for any S (gsm_not_pointwise_stabiliser); Galois closure = stab(E1) = spin(9); the h3(C) choice is input; locked rung verdict ILL-DEFINED (checker idempotent scaling, FM-SPEC)
MOD_Q.setdefault('Surf1', {})['N_c from one-loop SU(N) colour-sign coherence (d-coupled cubic adjoint, n <= 4)'] = 'free'  # SURF-1′ 2026-10-28: no N >= 3 coherent (no_sign_coherent_N: triangle K(3) = -1, crossed box K < 0 for N >= 4); full-tree window N >= 5; locked verdict EMPTY, NO-GO
MOD_Q.setdefault('Cascade1', {})['external mass ratios m_i/m_j (mass-shifted Tr phi^3, n = 4, 5)'] = 'free'  # CASCADE-1 2026-10-23: hidden zeros impose linear relations; dim Theta_final = 4/5 in EM (RATIOS-FREE)
MOD_Q['STRUCT3']['N_gen'] = 'free'  # STRUCT-3: AF+KM window {3,4,5}, not 3
MOD_Q['STRUCT3']['b₀ (β-function / curve count)'] = 'cited'
MOD_Q['X6']['chirality_orientation'] = 'free'  # X6: positivity is parity/reflection-blind (NO-GO)
MOD_Q['X6']['N_c'] = 'free'  # chirality + Witten => odd N_c >= 3, not 3
MOD_Q['X6']['hypercharges y_i'] = 'fixed'  # STRUCT-2 branch, yQ = 1 normalisation
MOD_Q['BridgePLAssoc']['anomaly_canonical_residue'] = 'free'
MOD_Q['Associahedron']['anomaly_canonical_residue'] = 'free'
MOD_Q['SC1']["α' (Regge slope)"] = 'fixed'
MOD_Q['SC1']['string tension σ'] = 'cited'
MOD_Q['MassiveLS']["α' (Regge slope)"] = 'fixed'
MOD_Q['SC2']['b₀ (β-function / curve count)'] = 'fixed'
MOD_Q['SC2b']['b₀ (β-function / curve count)'] = 'fixed'
MOD_Q['EWZ1b']['couplings g / lambda'] = 'fixed'  # lam4 = g² gauge (not Higgs)
# 2026-10-20 (M12/M1, approved by the author): alpha0 / α₀ is the Regge INTERCEPT, not the slope α'.
# Naming map: `a0` in MassiveLS = α₀ intercept; `alpha0` in FDim / FDimMass / FScatLen = α₀ intercept (F-DIM updates).
INTERCEPT = 'α₀ (Regge intercept)'
for M, st in (('MassiveLS', 'fixed'), ('FDim', 'unknown'), ('FDimMass', 'free'), ('FScatLen', 'unknown')):
    MOD_Q[M][INTERCEPT] = st

# binder tokens → quantity, only trusted inside modules that list that quantity (or DEF_Q)
BIND_Q = {
    # Canonical mass binders (2026-10-15 naming pass) + legacy aliases
    'mpi': 'm_π', 'm_pi': 'm_π', 'mpi2': 'm_π', 'm_pi2': 'm_π', 'mP': 'm_π', 'mP2': 'm_π', 'Mpi': 'm_π',
    'mp': 'm_π', 'mp2': 'm_π',  # legacy (pre-naming-pass)
    'mrho': 'm_ρ', 'm_rho': 'm_ρ', 'mrho2': 'm_ρ', 'm_rho2': 'm_ρ', 'Mrho': 'm_ρ', 'mr2': 'm_ρ',
    'mK': 'm_K', 'm_K': 'm_K', 'mK2': 'm_K', 'm_K2': 'm_K', 'MK': 'm_K',
    'm_eta2': 'm_η', 'me2': 'm_η', 'm_Kstar2': 'm_K*', 'mks2': 'm_K*', 'm_phi2': 'm_φ', 'mphi2': 'm_φ',
    'fpi': 'f_π', 'f_pi': 'f_π', 'Fpi': 'f_π',
    'ap': "α' (Regge slope)", "ap'": "α' (Regge slope)",
    'alpha0': 'α₀ (Regge intercept)', 'α₀': 'α₀ (Regge intercept)',  # was "α' (Regge slope)" (wrong; H4/M12 2026-10-20)
    # 'a0' no longer global: it is the intercept only in MassiveLS (MOD_BIND) and a scattering length elsewhere (M1)
    'sigmaNG': 'string tension σ', 'Sigma': 'σ-term',
    'lam3': 'couplings g / lambda', 'lam4': 'couplings g / lambda',
    'yQ': 'hypercharges y_i', 'yu': 'hypercharges y_i', 'yd': 'hypercharges y_i',
    'yL': 'hypercharges y_i', 'ye': 'hypercharges y_i', 'yn': 'hypercharges y_i',
    'Nc': 'N_c', 'N_c': 'N_c', 'b0': 'b₀ (β-function / curve count)', 'beta0': 'b₀ (β-function / curve count)',
    'L1': 'LECs L_i / l_i', 'L2': 'LECs L_i / l_i', 'L3': 'LECs L_i / l_i', 'L4': 'LECs L_i / l_i',
    'L5': 'LECs L_i / l_i', 'L6': 'LECs L_i / l_i', 'L7': 'LECs L_i / l_i', 'L8': 'LECs L_i / l_i',
    'L9': 'LECs L_i / l_i', 'L10': 'LECs L_i / l_i', 'l1': 'LECs L_i / l_i', 'l2': 'LECs L_i / l_i',
}
# module-restricted single-letter / short binders
MOD_BIND = {
    'scale (dimensionful unit)': {'r', 'λ', 'lam', 'mu', 'μ', 'scl'},
    'couplings g / lambda': {'g', 'g2', 'gsq', 'a', 'lambda', 'lam'},
    'vev v': {'v', 'vev'},
    'f_π': {'f', 'F'},
    'N_c': {'N', 'Nc'},
    'shift ansatz (NLSM δ / mesh)': {'delta', 'δ', 'd', 'eps', 'c'},
    'dispersion curvature c': {'c'},
    'm_π': {'m'},  # only in modules already tagged m_π
    'm_ρ': {'m'},
    'string tension σ': {'sigma', 'σ', 'sig'},
    'α₀ (Regge intercept)': {'a0'},  # only where MOD_Q lists the intercept (MassiveLS)
}

MEANING = {
    'm_η': ('η-meson mass', 'mass'),
    'm_K*': ('K* vector-meson mass', 'mass'),
    'm_φ': ('φ-meson mass', 'mass'),
    'm_π': ('pion mass', 'mass'),
    'm_ρ': ('ρ-meson mass (often the hadronic unit m_ρ² = 1)', 'mass'),
    'm_K': ('kaon mass', 'mass'),
    'f_π': ('pion decay constant / NLSM scale', 'mass'),
    'σ-term': ('pion–nucleon σ-term', 'mass'),
    'scale (dimensionful unit)': ('overall mass unit; BR-4/ScaleNoGo: geometry alone cannot fix it', 'mass'),
    'couplings g / lambda': ('gauge/contact couplings; EW-Z1b lam4 = g² is the VVVV contact (NOT Higgs quartic λ_H)', 'dimensionless'),
    'shift ansatz (NLSM δ / mesh)': ('δ-shift of Tr φ³ kinematics that yields NLSM / mesh offset; M2f forces c = M²', 'mass²'),
    'LECs L_i / l_i': ('ChPT / NLSM low-energy constants', 'dimensionless'),
    'N_c': ('number of colours; STRUCT-2: anomaly consistency selects only odd N, not 3', 'integer'),
    'hypercharges y_i': ('U(1)_Y hypercharges of one generation; unique without νᶜ (up to norm); B−L family with νᶜ unless Majorana', 'rational'),
    'chirality_orientation': ('positroid/Gr₊ orientation selecting a chiral spectrum (STRUCT route R2 / XD-6); X6: Gr₊ is invariant under parity (k↔n−k twist) and reflection, so orientation is NOT selected by positivity — chirality stays an input', 'dimensionless (sign)'),
    'anomaly_canonical_residue': ('anomaly polynomial as residue/invariant of a canonical form (STRUCT route R1)', 'rational'),
    'N_gen': ('number of SM fermion generations (STRUCT route R3 / STRUCT-3); STRUCT-3: ACC/Witten blind, AF(SU3) ≤ 8, AF(SU2) ≤ 5, KM ≥ 3 ⇒ window {3,4,5}', 'integer'),
    'ew_from_pion_geometry': ('pion/chiral geometry forcing quarks\' EW quantum numbers (STRUCT route R4); R4 2026-10-15: no candidate — geometry gives flavour-stripped amplitudes; the π⁰→γγ bridge is N_c-blind', 'rational'),
    'geometry_struct_separation': ('fallback: accept geometry↔STRUCT NO-LINK (STRUCT route R5); Lean bundle Separation.geometry_struct_separation; 0 cross edges in the dependency scan', 'method'),
    "α' (Regge slope)": ("Regge slope α' and intercept; MassiveLS gives α₀ = 1/2 in units m_ρ² = 1", 'α\': mass⁻²'),
    'α₀ (Regge intercept)': ('Regge intercept α₀ of the leading trajectory α(s) = α₀ + α′s (not the slope α′). Also known as: '
                             'alpha0, a0 (MassiveLS), alpha_0. MassiveLS / Adler point: α₀ = 1/2 (units α′ = 1 or m_ρ² = 1)',
                             'dimensionless'),
    'string tension σ': ('Nambu–Goto string tension σ = 1/(2π α′) [CITED]', 'mass²'),
    'dispersion curvature c': ('curvature of a discretised dispersion relation (positive weights ⇒ positive)', 'dimensionless'),
    'vev v': ('electroweak vacuum expectation value / leg mass scale', 'mass'),
    'b₀ (β-function / curve count)': ('one-loop UV log / β-function coefficient; SC-2: b₀ = −3/4 as a weighted curve count (PARTIAL)', 'rational'),
    'θ_W': ('weak mixing angle', 'dimensionless'),
    'spurion / quark mass': ('quark-mass spurion in ChPT', 'mass'),
}
EXCLUSION_NOTE = {
    'scale (dimensionful unit)': 'EXCLUSION: BR4.no_scale / ScaleNoGo / PG1.ratio_not_fixed rule out v and any dimensionful parameter from scale-free PG alone',
    'couplings g / lambda': 'EXCLUSION: SC-3 step 0 — Higgs quartic λ_H is absent from EW-Z1b (lam4 there is VVVV)',
    'hypercharges y_i': 'EXCLUSION: STRUCT1.not_unique_with_nu; STRUCT1b.dirac_not_unique (Majorana restores uniqueness)',
    'N_c': 'EXCLUSION: STRUCT2.three_not_selected — only odd N_c follows; X6.chiral_witten_not_selected — chirality adds only N_c ≥ 2',
    'N_gen': 'EXCLUSION: STRUCT3.three_not_selected_ngen — AF+KM window {3,4,5}; STRUCT3.cells_gr1_eq_three_iff / catalan_ne_three — no forced geometric 3',
    'ew_from_pion_geometry': 'EXCLUSION: Separation.pi0Anomaly_nc_blind — the pion↔charge bridge is N_c-blind; no geometry candidate',
    'chirality_orientation': 'EXCLUSION: X6.positivity_orientation_blind — positive-geometry orientation does not force chirality',
}


# Per-definition curated fill for GraphExport placeholders / empty docs.
# Sources: module header + adjacent Lean comments only ([NOTE]/[CURATED]). Never guessed.
# value: (meaning, dimension, status, source_tag)
DEF_META = {
    # 2026-10-16 housekeeping: remaining meaning/dimension unknowns, from module source/docstrings only
    'PositiveGeometryEmergentSpaceTime.BridgePLAssoc.hypersimplex25': ('Hypersimplex Δ(2,5): x ∈ [0,1]⁵ with Σxᵢ = 2 (moment-map image of Gr(2,5); def body)', 'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.BridgePLAssoc.pairNorm5': ('Sum of squares of all ten 2×2 Plücker minors pl5 P i j of a 2×5 matrix (moment-map normaliser; def body)', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.BridgePLAssoc.mu5': ('Moment map μᵢ (n=5): sum of squared Plücker minors containing i, over pairNorm5 (docstring)', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.BridgePLAssoc.channel01_23': ('n=4 planar channel monomial ⟨01⟩⟨23⟩ (module section (b))', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.BridgePLAssoc.channel03_12': ('n=4 planar channel monomial ⟨03⟩⟨12⟩ (module section (b))', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.BridgePLAssoc.channel02_13': ('n=4 crossed channel monomial ⟨02⟩⟨13⟩; Klein relation = planar three-channel identity (module section (b))', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.BridgePLAssoc.X13mono': ('Plücker monomial standing for planar variable X13: ⟨02⟩⟨13⟩ (docstring)', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.BridgePLAssoc.X14mono': ('Plücker monomial standing for planar variable X14: ⟨03⟩⟨14⟩ (docstring)', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.BridgePLAssoc.X24mono': ('Plücker monomial standing for planar variable X24: ⟨13⟩⟨24⟩ (docstring)', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.BridgePLAssoc.c13Mono': ('ABHY chart offset c13 = X24 − X14 + X13 on the Plücker monomials (docstring + def body)', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.HadronKinematics.sigmaPiK': ('Σ_πK = m_π² + m_K², πK dual-zero line value (docstring)', 'mass²', 'cited', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.HadronKinematics.stuSumPiK': ('On-shell elastic πK Mandelstam sum s+t+u = 2Σ_πK (docstring)', 'mass²', 'cited', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.HadronKinematics.q2PiK': ('πK c.m. momentum squared q²(s) = (s−(m_K+m_π)²)(s−(m_K−m_π)²)/(4s) (docstring + def body)', 'mass²', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IsingTiling.ogSignature': ('OG(3,6) signature η = (+,−,+,−,+,−) used in C η Cᵀ = 0 (def body + C_orth)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IsingTiling10.ogSignature': ('OG signature η (+−+−…) for the n=10 Ising tiling certificate (aka OG eta; docstring)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IsingTiling8.ogSignature': ('OG signature η (+−+−…) for the n=8 Ising tiling certificate (aka OG eta; docstring)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.MassiveSpinor.SpinorMat': ('2×2 complex matrix type (little-group / spinor; aka M; docstring)', 'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.SliceBridge.minkowskiDot': ('Minkowski product p·η·q, mostly-minus (1,3) (aka SliceBridge.mdot; docstring)', 'mass²', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.minkowskiQuad': ('Minkowski quadratic form η(v) = t² − x² − y² − z² (aka eta(v), minkQ; docstring)', 'mass²', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.TP1b.charPolyE8': ('E₈ adjacency characteristic polynomial in c (aka TP1b.P; docstring); root 2cos(π/30)', 'dimensionless', 'fixed', 'NOTE'),
    # FRMU (frontier rung 1: mu_n/mu_p)
    'PositiveGeometryEmergentSpaceTime.FRMU.SymIrrepME': ('Symmetric-irrep nucleon matrix elements ⟨Σσ_z⟩, ⟨Σσ_zτ_3⟩ in p↑/n↑ (aka ⟨2S_z⟩, ⟨4G^33⟩); FRONTIER-CONSTRUCTION data', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FRMU.SymIrrepME.Valid': ('Construction hypothesis: ⟨Σσ_z⟩ = 1, ⟨Σσ_zτ_3⟩ = ±(N_c+2)/3 (brute-force checked in sims/frmu; explicit hypothesis, not axiom)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FRMU.muProton': ('Proton magnetic moment μ_p in quark magnetons (aka μ_p)', 'dimensionless (μ_q units)', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FRMU.muNeutron': ('Neutron magnetic moment μ_n in quark magnetons (aka μ_n)', 'dimensionless (μ_q units)', 'fixed', 'NOTE'),
    # FDim (frontier F-DIM, 2026-10-20)
    'PositiveGeometryEmergentSpaceTime.FDim.gegen1': ('Gegenbauer C₁^λ(x) = 2λx, λ = (D−3)/2 (aka G₁(x, D)); SO(D−1) partial wave', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FDim.gegen2': ('Gegenbauer C₂^λ(x) = 2λ(λ+1)x² − λ (aka G₂(x, D))', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FDim.lsLevel1': ('Level-1 Lovelace–Shapiro residue in x = cos θ (aka R₁(x)); amplitude CITED', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FDim.lsCritDim': ('Critical dimension D_c(α₀) = 2(1+4α₀)/(2−α₀) of the LS family (aka D_c); = 4 at Adler α₀ = ½', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FDim.lsLevel2Half': ('Level-2 LS residue at α₀ = ½, σ-normalised ×128: (5x−3)(5x+1)(5x+5) (aka R₂(x))', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FDim.lsSpin0': ('Level-1 spin-0 coefficient 9α₀/(D−1) − (2−α₀) (aka B_{1,0})', 'dimensionless', 'variable', 'NOTE'),
    # FDimMass (frontier F-DIM-MASS, 2026-10-20)
    'PositiveGeometryEmergentSpaceTime.FDimMass.level1K': ('Level-1 kinematic shift k = (2 − α₀ − 4α′m_π²)/2 of the massive-pion LS residue (aka K/2)', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FDimMass.level1Spin0': ('Level-1 spin-0 coefficient k²/(D−1) + (α₀−k)(α₀+1−k) with external pion mass (aka B_{1,0}(α₀, m², D))', 'dimensionless', 'variable', 'NOTE'),
    # FScatLen (frontier F-SCATLEN, 2026-10-20)
    'PositiveGeometryEmergentSpaceTime.FScatLen.isoT0': ('Isospin-0 combination T⁰ = 3A(s,t,u)+A(t,s,u)+A(u,t,s); a₀⁰ = T⁰(4m²,0,0)/(32π)', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FScatLen.isoT2': ('Isospin-2 combination T² = A(t,s,u)+A(u,t,s); a₀² = T²(4m²,0,0)/(32π)', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FScatLen.linAmp': ('Linear Adler-zero pion amplitude (s − s_A)/F² (aka current-algebra amplitude; Weinberg at s_A = m²)', 'MeV^-2·MeV^2', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FScatLen.dualAmp': ('Dual crossing combination λ[V(s,t)+V(s,u)−V(t,u)] (aka Lovelace ππ amplitude)', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FScatLen.lsV': ('LS building block Γ(1−α_s)Γ(1−α_t)/Γ(1−α_s−α_t) (aka V(s,t))', 'dimensionless', 'variable', 'NOTE'),
    # FRhoWidth (frontier F-RHOWIDTH, 2026-10-20)
    'PositiveGeometryEmergentSpaceTime.FRhoWidth.isoT1': ('Isospin-1 combination T¹ = A(t,s,u) − A(u,t,s) (ρ channel)', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FRhoWidth.gLS2': ('LS ρππ coupling² with N1 normalisation, 1/(2πα′F²) (aka g²_ρππ, LS)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FRhoWidth.gKSRF2': ('KSRF ρππ coupling² m_ρ²/(2F²) (aka g²_KSRF)', 'dimensionless', 'fixed', 'NOTE'),
    # FDeltaNLSM (frontier F-POSGEOM-DAUGHTER, 2026-10-20; arXiv:2312.16282 eq. 7.10 CITED)
    'PositiveGeometryEmergentSpaceTime.FDeltaNLSM.deltaAmp4': ('δ-shifted stringy Tr(Φ³) 4-pt amplitude Γ(α′(X₁₃−δ))Γ(α′(X₂₄+δ))/Γ(α′(X₁₃+X₂₄)) (aka I₄^δ, stringy NLSM)', 'dimensionless', 'free', 'NOTE'),
    # BridgePLCharge (BRIDGE-PL-ASSOC mission rung, 2026-10-20)
    'PositiveGeometryEmergentSpaceTime.BridgePLCharge.torusAct': ('Column-torus action P ↦ P·diag(t) on 2×5 Plücker data (aka charge cocharacter; the torus element itself is the binder t)', 'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.BridgePLCharge.uCR': ('Plücker cross-ratio ⟨ab⟩⟨cd⟩/(⟨ac⟩⟨bd⟩) (aka u-variable of M₀,ₙ⁺)', 'dimensionless', 'variable', 'NOTE'),
    # IntChamber (frontier INT-1, 2026-10-22; ABHY 1711.09102 CITED)
    'PositiveGeometryEmergentSpaceTime.IntChamber.forms': ('Six wall forms c13, c14, c24, c13+c14, c14+c24, c13+c14+c24 of the n=5 kinematic associahedron (aka wall arrangement, chamber walls)', 'mass²', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IntChamber.chamberSign': ('Sign vector of the six wall forms at c′ (aka chamber label, sign vector σ)', 'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IntChamber.vertexType': ('Labelled vertex set of the associahedron at c′ (aka face type, I_comb)', 'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IntChamber.f0': ('Vertex count f₀ (aka f₀, number of vertices)', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IntChamber.f1': ('Edge count f₁ (aka f₁, number of edges)', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IntChamber.pt': ('Candidate vertex = intersection point of a facet pair (aka pair point)', 'mass²', 'variable', 'NOTE'),
    # LeanCert (method rung LEAN-CERT-1, 2026-10-23; ABHY 1711.09102 CITED)
    'PositiveGeometryEmergentSpaceTime.LeanCert.checkZero': ('Bool check that the integer product M·K is the zero matrix (aka certificate check MK = 0)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.LeanCert.checkSplit': ('Bool check of the split identity P·M + K·Q = d·1 (aka splitting certificate)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.LeanCert.checkInj': ('Bool check of the left inverse Q·K = d·1, so K is injective (aka injectivity certificate)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.LeanCert.checkEq': ('Bool check of entrywise equality of two integer matrices (aka matrix equality check)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.LeanCert.abhy6_M': ('n = 6 ABHY constraint matrix c_ij = X_ij + X_{i+1,j+1} − X_{i,j+1} − X_{i+1,j} on the 9 planar variables (aka ABHY conservation matrix, n = 6)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.LeanCert.abhy6_K': ('Integer basis of ker M for n = 6, 9 columns (aka kinematic-space basis K_6)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.LeanCert.gpos_M': ('Integer matrix of the GRADED-POSITROID linear ACC rows in (u, d, l, e) at yQ = 1 (aka GPOS linear system)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.LeanCert.gpos_x0': ('Particular solution of the GPOS linear system (aka base point x0)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.LeanCert.accSet': ('Set of rational hypercharge tuples with yQ = 1 satisfying all four ACC (aka anomaly-free set, N_ACC set)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.LeanCert.gpos_Kflip': ('Planted wrong kernel vector (one sign flipped) (aka planted flip)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.LeanCert.gpos_Pbad': ('Planted wrong split matrix P (aka planted split)', 'dimensionless', 'fixed', 'NOTE'),
    # Cascade1 (rung CASCADE-1, 2026-10-23; Arkani-Hamed et al. 2312.16282 CITED)
    'PositiveGeometryEmergentSpaceTime.Cascade1.A5': ('n = 5 Tr φ³ triangulation sum Σ Π 1/y in shifted variables y = X − μ (aka cascade S2 amplitude)', 'mass⁻⁴', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Cascade1.Zeros5': ('A5(X − μ) vanishes on all five physical hidden-zero loci Z_i (aka n5 hidden-zero condition)', 'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Cascade1.Rel5': ('The five linear S3 relations μ_ab = c_ab(m) between chord offsets and external masses (aka EM n5 zero relations)', 'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Cascade1.em5_M': ('Integer matrix of the five EM n = 5 relations on (μ13, μ14, μ24, μ25, μ35, m1…m5) (aka Rel5 matrix)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Cascade1.em5_K': ('Integer kernel basis of em5_M, 5 columns (aka n5 Θ_3 basis)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Cascade1.em5_P': ('Split matrix P with P·M + K·Q = 1 for n = 5 (aka n5 splitting certificate)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Cascade1.em5_Q': ('Left inverse Q with Q·K = 1 for n = 5 (aka n5 injectivity certificate)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Cascade1.em5_d': ('Certificate denominator d = 1 for n = 5 (aka n5 certificate scale)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Cascade1.em4_M': ('Integer matrix of the two EM n = 4 relations on (μ13, μ24, m1…m4) (aka n4 relation matrix)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Cascade1.em4_K': ('Integer kernel basis of em4_M, 4 columns (aka n4 Θ_3 basis)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Cascade1.em4_P': ('Split matrix P for n = 4 (aka n4 splitting certificate)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Cascade1.em4_Q': ('Left inverse Q for n = 4 (aka n4 injectivity certificate)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Cascade1.em4_d': ('Certificate denominator d = 1 for n = 4 (aka n4 certificate scale)', 'dimensionless', 'fixed', 'NOTE'),
    # FL1Z (frontier FL-1Z, 2026-10-22; Kobayashi–Okada–Orikasa 2502.12662 CITED)
    'PositiveGeometryEmergentSpaceTime.FL1Z.D3': ('Fixed-point Zee–Babu neutrino matrix of 2502.12662 eq. (D.3) at τ = ω (aka m_ν(ω), D.3 matrix)', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FL1Z.w': ('Rank-1 generator w = (2, −ω², 2ω) with D3 = w wᵀ (aka fixed-point vector)', 'dimensionless', 'variable', 'NOTE'),
    # STRUCTNGen (STRUCT-NGEN sharpen, 2026-10-20)
    'PositiveGeometryEmergentSpaceTime.STRUCTNGen.b1QCD': ('Two-loop QCD coefficient 102 − 38/3·n_f, n_f = 2N_gen (aka β₁)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.STRUCTNGen.anomaly331': ('3-3-1 SU(3)_L anomaly #3 = #3̄ with N lepton triplets (aka 331 anomaly)', 'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.STRUCTNGen.b0QCD331': ('One-loop QCD coefficient in the 3-3-1 rival, n_f = 3N_gen', 'dimensionless', 'fixed', 'NOTE'),
    # GradedPositroid (GRADED-POSITROID mission rung, 2026-10-22)
    'PositiveGeometryEmergentSpaceTime.GradedPositroid.genW': ('Cartan weights (H3, H8′, T3, Y) of the 15 SM Weyl states for hypercharges (yQ, yu, yd, yL, ye) (aka graded column weights)', 'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.GradedPositroid.smW': ('SM Cartan weights (Y = 1/6, −2/3, 1/3, −1/2, 1)', 'type', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.GradedPositroid.m1': ('Graded first moment Σᵢ wᵢᵃ (up to the factor k/n)', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.GradedPositroid.cub': ('Graded cubic tensor Σᵢ wᵢᵃwᵢᵇwᵢᶜ (aka Cartan-restricted anomaly polynomial)', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.GradedPositroid.ACC': ('Four perturbative ACC (grav, SU(3)²Y, SU(2)²Y, Y³) with SM multiplicities', 'type', 'variable', 'NOTE'),
    # TrialityWhy (TRIALITY-WHY, 2026-10-23)
    'PositiveGeometryEmergentSpaceTime.TrialityWhy.doubletCharge': ('Z_k doublet charge per generation 3·qQ + qL (aka c, B3 doublet charge)', 'integer (mod k)', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.TrialityWhy.sphaleronCharge': ('Z_k charge of the SU(2) instanton (\'t Hooft) vertex N·(3qQ + qL) (aka sphaleron charge)', 'integer (mod k)', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.TrialityWhy.wwxSum': ('Ibáñez–Ross SU(2)²–Z_k linear anomaly sum over doublets, N generations (aka WWX, A_2)', 'integer (mod k)', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.TrialityWhy.ccxSum': ('SU(3)²–Z_k linear anomaly sum per generation with Yukawa-fixed charges (aka CCX, A_3)', 'integer (mod k)', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.TrialityWhy.gravSum': ('Gravity²–Z_k linear sum per generation without νᶜ (aka GGX, A_grav)', 'integer (mod k)', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.TrialityWhy.qgOK': ('No-global-symmetries dichotomy: exact → gauged ∨ broken (aka QG dichotomy) [CITED: 1011.5120, 1810.05337]', 'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.TrialityWhy.nullFamily': ('Declared null family of (k, c), 2 ≤ k ≤ 18, 0 ≤ c < k (170 pairs; aka Z_k null)', 'type', 'fixed', 'NOTE'),
    # LeanCert2 (method rung LEAN-CERT-2, 2026-10-28; list-based certificates, run LEANCERT2-2026-10-28-r1)
    'PositiveGeometryEmergentSpaceTime.LeanCert2.dotL': ('Dot product of two integer lists by structural recursion, stopping at the shorter list (aka list dot product)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.LeanCert2.rowsM': ('Fin-indexed integer matrix whose row i is the i-th list (missing entries 0) (aka rows-to-matrix)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.LeanCert2.colsM': ('Fin-indexed integer matrix whose column j is the j-th list (missing entries 0) (aka columns-to-matrix)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.LeanCert2.lenL': ('Bool: every list in L has length at most n (aka row-length bound)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.LeanCert2.mulL': ('(i, j) entry of a product given as row lists times column lists (aka list matrix product entry)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.LeanCert2.tposL': ('Bool: the row-list and column-list encodings give the same matrix (aka transpose consistency check)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.LeanCert2.zeroL': ('Bool: M·K = 0 from row lists of M and column lists of K (aka list certificate check MK = 0)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.LeanCert2.splitL': ('Bool: P·M + K·Q = d·1 from list encodings (aka list splitting certificate)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.LeanCert2.injL': ('Bool: Q·K = d·1 from list encodings, so K is injective (aka list injectivity certificate)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.LeanCert2.certL': ('Full list certificate that dim ker M = k over ℚ: d ≠ 0, length bounds, transposes, MK = 0, PM + KQ = d·1, QK = d·1 (aka certL, kernel-dimension certificate)', 'dimensionless', 'fixed', 'NOTE'),
    # Surf1 (rung SURF-1′, 2026-10-28; run SURF1-2026-10-28-r1)
    'PositiveGeometryEmergentSpaceTime.Surf1.G': ('Closed cubic graph: vertices as cyclically ordered half-edge lists plus edges as half-edge pairs (aka ribbon graph)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.inS': ('Incoming index slot 2h of half-edge h (aka in-slot)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.outS': ('Outgoing index slot 2h+1 of half-edge h (aka out-slot)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.oriented': ('Vertex half-edges in cyclic order, reversed when bit j of o is set (aka vertex orientation)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.nextIn': ('Cyclic successor of a half-edge at its vertex (aka next half-edge)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.prevIn': ('Cyclic predecessor of a half-edge at its vertex (aka previous half-edge)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.findSome': ('First vertex index giving Some under f (aka search helper)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.vlink': ('Vertex link: out(h) joins in(next h) under orientation o (aka double-line vertex)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.findEdge': ('Edge index and endpoints containing a half-edge (aka edge lookup)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.elink': ('Edge link: exchange propagator, or self-contraction (U(1) ghost term) when the edge bit of m is set (aka double-line propagator)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.nSlots': ('Number of index slots, 2·Σ|v| (aka slot count)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.vtab': ('Vertex-link table over all slots (aka vertex permutation)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.etab': ('Edge-link table over all slots (aka edge permutation)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.markLoop': ('Marks one alternating vertex/edge cycle in a bitmask (aka loop walker)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.loopsT': ('Number of closed index loops from link tables (aka loop count)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.loops': ('Closed index loops of configuration (o, m) (aka face count)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.popc': ('Popcount of the low bits of m (aka ghost-edge count k)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.nCubic': ('Number of cubic vertices (unused helper)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.oValid': ('Bool: orientation o flips only cubic vertices (aka valid orientation)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.coefO': ('Coefficient of N^e from orientation o, summed over ghost subsets with sign (−1)^k at c = 1 (aka per-orientation weight)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.ovec': ('Per-orientation coefficient vector over exponents hi down to hi−len+1 (aka orientation vector)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.vsum': ('Sum of orientation vectors over o < n (aka orientation sum)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.hiW': ('Top exponent of the coefficient window, nSlots (aka window top)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.lenW': ('Coefficient window length nSlots + |E| + 1 (aka window length)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.coefs': ('Full SU(N) colour-weight coefficient vector of a graph (aka colour weight)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.coefU': ('U(N) (no ghost) loop-count coefficient (aka U(N) weight)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.nz': ('Nonzero (exponent, coefficient) pairs of a coefficient vector (aka sparse polynomial)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.W1': ('SU(N) colour weight as a Laurent polynomial in N, c = 1 (aka W(G))', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.single': ('One-edge one-vertex test graph (aka planted loop)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.theta': ('Theta graph: tree∘tree at n = 3, the n = 3 denominator (aka theta graph)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.tetra': ('Tetrahedron: tree∘triangle at n = 3 (aka W(tree∘G), triangle)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.boxU': ('Crossed box glued to the u-channel tree, box1234|u (aka crossed box channel)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.ttU': ('u-channel tree glued to itself, the n = 4 u-channel denominator (aka u-tree self-gluing)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.ev': ('Evaluates a sparse Laurent polynomial at rational N (aka evaluation)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.K': ('Interference ratio K = W(tree∘G)/W(tree∘tree) at N (aka colour-sign ratio)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.thetaL': ('Theta weight 2N³ − 10N + 8/N (aka theta polynomial)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.tetraL': ('Tetrahedron weight (aka triangle polynomial)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.ttUL': ('u-tree self-gluing weight (aka n = 4 denominator)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Surf1.boxUL': ('Crossed-box weight −32(N²−1)(N²−4)(N²−10)/N³ (aka box polynomial)', 'dimensionless', 'fixed', 'NOTE'),
    # Jord1 (exploration rung JORD-1, 2026-10-28; run JORD1-2026-10-28-r1)
    'PositiveGeometryEmergentSpaceTime.Jord1.fano': ('Oriented Fano lines (1,2,4),(2,3,5),(3,4,6),(4,5,7),(5,6,1),(6,7,2),(7,1,3): e_x e_y = e_z cyclically (aka octonion multiplication lines)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.lineHit': ('Product of two imaginary octonion units along one Fano line, if both lie on it (aka line lookup)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.ou': ('Octonion unit product e_a e_b = s e_c returned as (s, c), e_0 = 1 (aka octonion structure constants)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.Ent': ('Sparse octonion-matrix entry (row, col, unit, coefficient) (aka sparse entry)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.blk': ('Off-diagonal blocks (base, row, col) of h3(O): a = coords 3..10 at (2,3), b = 11..18 at (3,1), c = 19..26 at (1,2) (aka block layout)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.basisE': ('Basis element b_i (i < 27) of h3(O) as a sparse hermitian octonion 3×3 matrix (aka Jordan basis)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.mprod': ('Sparse octonion-matrix product using ou (aka matrix product)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.coefS': ('Coefficient of index l in a sparse vector (aka sparse coefficient)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.sumAt': ('Sum of the coefficients of a sparse matrix at (row, col, unit) (aka entry sum)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.coordE': ('Coordinate l of a sparse hermitian matrix in the basis b_0..b_26 (aka coordinate map)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.jprod': ('Coordinates of 2 b_i∘b_j = b_i b_j + b_j b_i (aka Jordan product, 2× scale)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.T1s': ('Sparse structure constants T1[i][j] = list of (l, c) with 2 b_i∘b_j = Σ c b_l (aka Jordan table)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.T2s': ('Transposed sparse table T2s[j][k] = list of (l, c), c = T1[l][j][k] (aka Jordan table by output index)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.T1s_ok': ('Bool: T1s agrees with jprod on all 27×27 pairs (aka table check)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.T2s_ok': ('Bool: T2s is the transpose-indexed form of T1s (aka table consistency check)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.comm_ok': ('Bool: the Jordan table is commutative (aka commutativity check)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.idx_ok': ('Bool: every sparse index in the tables is below 27 (aka index bound check)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.idxOK': ('Bool: all indices of a sparse vector are below 27 (aka index bound)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.bc': ('Structure constants as a function: 2 b_i∘b_j = Σ_l bc i j l • b_l (aka bc)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.IsDer': ('D (27×27 over ℚ, acting on column vectors) is a derivation of (h3(O), ∘) (aka derivation, f4 element)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.dotS': ('Sparse-dense dot product (aka sparse dot)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.derS': ('Bool: sparse derivation test of a row list Dr and its column list Dc against T1s/T2s (aka sparse derivation check)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.E1v': ('The rank-1 idempotent E1 = diag(1,0,0) as a coordinate vector (aka E1)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.inB': ('Coordinates [0,1,2,3,4,11,12,19,20] spanning h3(C) ⊂ h3(O), C = span{1, e1} (aka h3(C) index set)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.PresB': ('D maps h3(C) into itself (aka preserves h3(C), set-stabiliser condition)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.presBL': ('Bool form of PresB on a list encoding (aka presB check)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.col0L': ('Bool: column 0 of D is zero, i.e. D E1 = 0 (aka kills E1 check)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.gsm': ('g_sm = stab(E1) ∩ setstab(h3(C)) inside the derivations of h3(O) over ℚ (aka Standard Model subalgebra, Todorov/Dubois-Violette; dims (12,4,1,11) SIMULATED) [CITED: 1911.13124, 2606.15235]', 'dimensionless', 'free', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.stab': ('Pointwise stabiliser of S ⊆ h3(O) in the derivations (aka stab(S), positivity/Galois closure candidate)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.Gs': ('Rows of 12 integer elements of g_sm from the live run (aka g_sm generators)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.GsC': ('Columns (transposes) of Gs (aka generator columns)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.gR': ('Row list of one g_sm generator (aka generator rows)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.gC': ('Column list of one g_sm generator (aka generator columns)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.genOK': ('Bool: all kernel checks for generator k (derivation, kills E1, preserves h3(C)) (aka generator certificate)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.Wr': ('Row lists of W, a derivation in stab(Fix(g_sm)) that does not preserve h3(C) (aka witness W)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.Wc': ('Column lists of W (aka witness columns)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.ww': ('W as a 27×27 rational matrix (aka witness matrix)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.wk': ('Witness entry W[5][1] = −1 ≠ 0 with 5 ∉ h3(C), 1 ∈ h3(C) (aka escape entry)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.selIdx': ('Selected rows (k, ρ): row r of Rsel is row ρ of generator k (aka row selection)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.nSel': ('Number of selected rows (aka selection size)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.Rsel': ('25 selected rows of the g_sm generators: Rsel x = 0 for every x fixed by g_sm (Rsel_kills) (aka selected rows)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.RselC': ('Columns of Rsel (aka selected rows, column form)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.selOK': ('Bool: each row of Rsel is the declared row of the declared generator (aka selection check)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.Cm': ('Integer coefficient matrix with dW • W = Cm * Rsel (aka row-span certificate)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.dW': ('Nonzero integer denominator in the row-span certificate (aka certificate scale)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Jord1.certW': ('Bool certificate: Cm * Rsel = dW • W from list encodings (aka row-span check)', 'dimensionless', 'fixed', 'NOTE'),
    # FCoulomb (frontier F-COULOMB, 2026-10-20: deformed amplituhedron, arXiv:2311.10814 CITED)
    'PositiveGeometryEmergentSpaceTime.FCoulomb.crossRatioU': ('Dual-conformal cross-ratio u = (1+r)²/(4r), r = ρρ̃ (eq. (21); aka u, v with r = ηη̃)', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FCoulomb.crossRatioMass': ('Eq. (22) RHS (−s+m₁²+m₃²)²/(4m₁²m₃²) (aka u(s, m₁, m₃)); masses are inputs (BR-4)', 'dimensionless', 'free', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FCoulomb.Wedge': ('Deformed one-loop region half, eq. (7): y > ρz > 0, z > ρ̃y > 0 (aka deformed amplituhedron wedge; ρ = rho, ρ̃ = rhot)', 'dimensionless', 'variable', 'NOTE'),
    # FRWZW (frontier: parity-odd 5-point form)
    'PositiveGeometryEmergentSpaceTime.FRWZW.Vec4': ('4-vector over ℚ (aka p, momentum)', 'mass', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FRWZW.levi4': ('Levi-Civita contraction ε(a,b,c,d) = det[a;b;c;d] (aka ε, eps4)', 'mass⁴', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FRWZW.p5': ('Fifth momentum −(p₁+p₂+p₃+p₄) by conservation (aka p5)', 'mass', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FRWZW.oddNumerator5': ('Leading parity-odd 5-pt numerator c·ε(p₁..p₄) (aka WZW-5 numerator, oddCanonicalForm numerator); c free', 'mass⁴', 'free', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.FRWZW.wzwContactVertex': ('Ordered WZW contact vertex, sum of 5 cyclic placements = 5ε (planted answer)', 'mass⁴', 'fixed', 'NOTE'),
    # Separation (R4/R5)
    'PositiveGeometryEmergentSpaceTime.Separation.chargeUp': ('Up-quark electric charge Q_u = yQ + 1/2 (T₃ + Y; aka Q_u, e_u)', 'rational (e)', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Separation.chargeDown': ('Down-quark electric charge Q_d = yQ − 1/2 (aka Q_d, e_d)', 'rational (e)', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Separation.pi0Anomaly': ('π⁰→γγ triangle coefficient N_c(Q_u² − Q_d²) (aka A_π⁰γγ) [CITED structure: ABJ/Bär–Wiese]', 'dimensionless', 'fixed', 'NOTE'),
    # R4 independent attempt (2026-10-16)
    'PositiveGeometryEmergentSpaceTime.R4Indep.mesonCharge': ('Charge of flavour-ordered meson q_i q̄_j: Q_i − Q_j (adjoint action; aka Q_ij)', 'rational (e)', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.R4Indep.dgmlyCharge': ('DGMLY π⁺−π⁰ EM-splitting charge factor (Q_u − Q_d)² [CITED structure: Das et al. 1967]', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.R4Indep.etaPiPiGamma': ('η⁸→π⁺π⁻γ WZW box coefficient N_c(Q_u − Q_d) [CITED: Bär–Wiese eq. 5.9]', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.R4Indep.pi0KKGamma': ('π⁰K⁺K⁻γ WZW box coefficient N_c·Q_u [CITED: Bär–Wiese eq. 5.12]', 'dimensionless', 'fixed', 'NOTE'),
    # STRUCT3 (N_gen)
    'PositiveGeometryEmergentSpaceTime.STRUCT3.b0SU3': ('One-loop SU(3) β coefficient b₀ = 11 − (4/3) N_gen (aka β₀ QCD) [CITED]', 'rational', 'cited', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.STRUCT3.b0SU2': ('One-loop SU(2)_L β coefficient b₀ = 22/3 − (4/3) N_gen − 1/6, one Higgs doublet (aka β₀ weak) [CITED]', 'rational', 'cited', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.STRUCT3.kmPhases': ('Number of physical CKM CP phases (N_gen−1)(N_gen−2)/2 (aka KM phase count) [CITED]', 'integer', 'cited', 'NOTE'),
    # X6 (chirality_orientation)
    'PositiveGeometryEmergentSpaceTime.X6.Plucker24': ('Plücker coordinates p_ij (i<j) of a point of Gr(2,4). Also known as Δ_ij, ⟨ij⟩', 'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.X6.Plucker24.rel': ('Three-term Plücker relation p13 p24 = p12 p34 + p14 p23 (aka Schouten)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.X6.Plucker24.pos': ('Total positivity of all six Plücker coordinates (Gr₊(2,4) top cell)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.X6.parityDual': ('Parity map p_I ↦ p_{Iᶜ} (twisted complement; aka twist map, λ↔λ̃, k↔n−k) [CITED Galashin–Lam 1805.00600]', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.X6.reflect': ('Cyclic reflection i ↦ 5−i on Gr(2,4) Plücker data (orientation reversal)', 'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.X6.branchCharges': ('One-generation charge multiset on the STRUCT-2 branch, yQ = 1: Q(2N_c)×1, uᶜ(N_c)×(N_c−1), dᶜ(N_c)×(−N_c−1), L(2)×(−N_c), eᶜ×2N_c', 'rational (U(1)_Y)', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.X6.VectorLike': ('Charge multiset closed under negation (vector-like / real representation)', 'dimensionless', 'fixed', 'NOTE'),
    # Associahedron
    'PositiveGeometryEmergentSpaceTime.Assoc.crosses': (
        'True iff diagonals p,q of a convex n-gon properly cross (used to filter triangulations / Catalan vertices of A_n)',
        'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Assoc.noncrossing': (
        'True iff a list of diagonals is pairwise non-crossing (= admissible triangulation / A_n vertex)',
        'dimensionless', 'variable', 'NOTE'),
    # CoulombZero (module header: planar shift / c_ij)
    'PositiveGeometryEmergentSpaceTime.CoulombZero.cvar': (
        'Planar 2×2 combination c_ij = X_ij + X_{i+1,j+1} − X_{i,j+1} − X_{i+1,j} (CGW Coulomb-branch kinematics)',
        'mass²', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.CoulombZero.Xt': (
        'Planar shift X̃_ij = X_ij − g²(v_i − v_j)² (CGW eq. 56; vev eigenvalues v_i)',
        'mass²', 'variable', 'NOTE'),
    # Hankel spectral toys
    'PositiveGeometryEmergentSpaceTime.Hankel.xT': (
        'Support points of the toy positive spectral measure δ_{1/2}+2δ_{1/3}+3δ_1 (Hankel moment checks)',
        'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Hankel.xC': (
        'Support points of the signed C1 counterexample measure δ_{1/2}−½δ_1 (violates H2)',
        'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Hankel.xC3': (
        'Support points of the signed C3 counterexample at 0,1,2 (moments (1,2,1) violate H2)',
        'dimensionless', 'fixed', 'NOTE'),
    # MarkovTrace
    'PositiveGeometryEmergentSpaceTime.MarkovTrace.pi3': (
        'Stationary distribution π=(1/4,1/4,1/2) of the 3-state counterexample chain P3 (entropy-rate / trace)',
        'dimensionless', 'fixed', 'NOTE'),
    # IsingLoop (shares docstring with m12)
    'PositiveGeometryEmergentSpaceTime.IsingLoop.m13': (
        'Triangle-network boundary correlation m₁₃; u=(u₁₂,u₁₃,u₂₃)=tanh K (high-T expansion)',
        'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IsingLoop.m23': (
        'Triangle-network boundary correlation m₂₃; u=(u₁₂,u₁₃,u₂₃)=tanh K (high-T expansion)',
        'dimensionless', 'variable', 'NOTE'),
    # IsingTiling / 8 / 10 (module headers: GP matrices in OG(k,n))
    'PositiveGeometryEmergentSpaceTime.IsingTiling.C': (
        'Certified GP / orthogonal-Grassmannian matrix C ∈ Mat_{3×6}(ℚ) for the n=6 Ising tiling (Y=CΛ, CηCᵀ=0)',
        'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IsingTiling.Λ': (
        'Vandermonde-like rows (1,x,…,x⁴) for x=1..6 used in the Ising tiling certificate Y=CΛ',
        'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IsingTiling.Y': (
        'Certified 3×5 moment / embedding matrix Y=CΛ for the n=6 Ising tiling point in OG(3,6)',
        'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IsingTiling.eta': (
        'Signature vector η=(+−+−+−) for the OG(3,6) orthogonality CηCᵀ=0',
        'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IsingTiling10.eta': (
        'Signature vector η=(+−)⁵ for OG(5,10) orthogonality Cx η Cxᵀ=0',
        'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IsingTiling10.C1': (
        'GP matrix C1 for Ising network T₁ (tanh J=1/2); lies in OG(5,10) with prescribed vanishing minors',
        'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IsingTiling10.C2': (
        'GP matrix C2 for Ising network T₂ (tanh J=1/2); OG(5,10) certificate',
        'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IsingTiling10.C3': (
        'GP matrix C3 for Ising network T₃ (tanh J=1/2); OG(5,10) certificate',
        'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IsingTiling10.C4': (
        'GP matrix C4 for Ising network T₄ (tanh J=1/2); OG(5,10) certificate',
        'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IsingTiling10.C5': (
        'GP matrix C5 for Ising network T₅ (tanh J=1/2); OG(5,10) certificate',
        'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IsingTiling8.eta': (
        'Signature vector η=(+−)⁴ for OG(4,8) orthogonality',
        'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IsingTiling8.C0': (
        'GP matrix C0 in positroid cell (4,6,7,1,8,2,3,5) for the n=8 Ising tiling (HW σ2)',
        'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.IsingTiling8.C2': (
        'GP matrix C2 in positroid cell (5,7,6,8,1,3,2,4) for the n=8 Ising tiling (HW σ1)',
        'dimensionless', 'fixed', 'NOTE'),
    # Kerr
    'PositiveGeometryEmergentSpaceTime.KerrMinimal.currS': (
        'Kerr current multipoles S_ℓ = m Im(i a)^ℓ (spin S₁=ma; even ℓ vanish)',
        'mass × length^ℓ', 'variable', 'NOTE'),
    # LatticeGate
    'PositiveGeometryEmergentSpaceTime.LatticeGate.q2': (
        'Equal-mass-style c.m. momentum squared q²(s) for πK; on s=Σ=m_π²+m_K² equals −m_π² m_K²/Σ',
        'mass²', 'variable', 'NOTE'),
    # MassiveLS Legendre
    'PositiveGeometryEmergentSpaceTime.MassiveLS.P1': (
        'Legendre polynomial P₁(x)=x used in LS residue partial-wave decompositions',
        'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.MassiveLS.P2': (
        'Legendre polynomial P₂(x)=(3x²−1)/2 used in LS residue partial-wave decompositions',
        'dimensionless', 'fixed', 'NOTE'),
    # MassiveSpinor
    'PositiveGeometryEmergentSpaceTime.MassiveSpinor.M': (
        '2×2 complex matrix type for massive spinor-helicity momenta (det p = m²)',
        'type', 'variable', 'NOTE'),
    # MassiveZero*
    'PositiveGeometryEmergentSpaceTime.MassiveZeroOneLoop.bsum': (
        'One-loop polynomial combination b₁+b₂+b₃+b₄(t−u)² of SU(2) ππ amplitude at P (BCEGS / GL85 matching)',
        'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.MassiveZeroSU3.SA': (
        'Single-trace O(p⁴) kinematic structure SA=((s−2)²+(t−2)²)/4 (units M=1)',
        'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.MassiveZeroSU3.SB': (
        'Single-trace O(p⁴) kinematic structure SB=(u−2)²/4 with u=4−s−t (units M=1)',
        'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.MassiveZeroSU3Phys.AF4': (
        'SU(3) ππ tree O(p⁴) amplitude×F⁴ polynomial at massive hidden-zero kinematics (MR-2d form)',
        'dimensionless', 'variable', 'NOTE'),
    # Network
    'PositiveGeometryEmergentSpaceTime.Network.pipath': (
        'Stationary distribution of the path random walk 0—2—1 with conductances a,c (electrical network / Lam point)',
        'dimensionless', 'variable', 'NOTE'),
    # OrderParameter
    'PositiveGeometryEmergentSpaceTime.OrderParam.SU2': (
        'SU(2) as Matrix.specialUnitaryGroup (Fin 2) ℂ — gauge factor of the OP-1 gauge instance',
        'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.OrderParam.Gauge': (
        'Gauge group SU(2)×U(1)≃SU2×Circle acting on the Higgs doublet ℂ² (OP-1)',
        'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.OrderParam.GL4': (
        'GL(4,ℝ) as units of 4×4 real matrices — spacetime congruence group in OP-1',
        'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.OrderParam.gaugeAction': (
        'MulAction of Gauge on ℂ²: ψ ↦ z·(Uψ) (U(1) charge-1 parametrisation; Y=½ is a double cover)',
        'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.OrderParam.congrAction': (
        'MulAction of GL4 on Form4 by congruence B ↦ g B gᵀ (preserves symmetric forms)',
        'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.OrderParam.gaugeOP': (
        'OrderParameter instance: Gauge on ℂ² with Higgs vev (0,1) (broken phase)',
        'type', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.OrderParam.spacetimeOP': (
        'OrderParameter instance: GL4 on Form4 with Minkowski η=diag(1,−1,−1,−1) (broken phase)',
        'type', 'fixed', 'NOTE'),
    # PiKZero
    'PositiveGeometryEmergentSpaceTime.PiKZero.Fp': (
        'Even πK subthreshold polynomial F⁺(τ,x) in BDM variables (τ=t/m_π², x related to ν)',
        'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.PiKZero.Fm': (
        'Odd πK subthreshold polynomial F⁻(τ,x); F^{3/2}=F⁺−F⁻ on the line x=κτ',
        'dimensionless', 'variable', 'NOTE'),
    # PionBound
    'PositiveGeometryEmergentSpaceTime.PionBound.b4': (
        '16π² b₄ at LO: b₄(l₂)=l₂/6 − 5/36 (ChPT ππ amplitude coefficient)',
        'dimensionless', 'variable', 'NOTE'),
    # PositroidCells
    'PositiveGeometryEmergentSpaceTime.PositroidCells.mem': (
        'Membership test: whether index x lies in the necklace pair p (Grassmann necklace / bounded affine perm)',
        'dimensionless', 'variable', 'NOTE'),
    # SliceBridge
    'PositiveGeometryEmergentSpaceTime.SliceBridge.mdot': (
        'Minkowski product p·q = t_p t_q − x·y on ℝ^{1,3} (mostly-minus)',
        'mass²', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.SliceBridge.mdotQ': (
        'Rational Minkowski product on ℚ^{1,3} (exact kinematics certificates)',
        'mass²', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.SliceBridge.Null': (
        'Null vector predicate: p·p = 0 in ℝ^{1,3}',
        'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.SliceBridge.splitPosT': (
        'Right spinor factors of an explicit (2,2) n=5 configuration with all planar invariants positive',
        'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.SliceBridge.splitNegT': (
        'Right spinor factors of an explicit (2,2) n=5 configuration with all planar invariants negative',
        'dimensionless', 'fixed', 'NOTE'),
    # Spinor (M1)
    'PositiveGeometryEmergentSpaceTime.M2': (
        '2×2 complex matrices; target of the Pauli / σ map from Minkowski ℝ^{1,3}',
        'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.Herm': (
        'ℝ-submodule of Hermitian 2×2 matrices inside M2 (spinor form of real Minkowski space)',
        'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.sigma': (
        'σ(t,x,y,z)=[[t+z, x−iy],[x+iy, t−z]]; linear map ℝ^{1,3}→M2 with det σ(v)=η(v)',
        'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.sigmaL': (
        'Linear map version of σ: (Fin 4 → ℝ) →ₗ[ℝ] M2',
        'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.eta': (
        'Minkowski quadratic form η(v)=t²−x²−y²−z² on ℝ^{1,3}',
        'mass²', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.hermEquiv': (
        'Linear equivalence ℝ^{1,3} ≃ₗ Herm via σ (M1 spinor form)',
        'type', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.minkQ': (
        'Mathlib QuadraticForm for weightedSumSquares(1,−1,−1,−1); equals η',
        'mass²', 'variable', 'NOTE'),
    # Subthreshold / TP / UnitarisedLS
    'PositiveGeometryEmergentSpaceTime.SubthresholdGate.Asub': (
        'ππ subthreshold amplitude A(s,t,u) in Knecht–Moussallam–Stern–Fuchs / CGL form (units M_π²=1)',
        'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.TP1a.x': (
        'A_n Perron–Frobenius eigenvector component x_k = sin(kπ/(n+1)) (Coxeter h=n+1)',
        'dimensionless', 'variable', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.TP1b.P': (
        'E8 characteristic polynomial P(c)=c⁸−7c⁶+14c⁴−8c²+1; vanishes at c=2cos(π/30)',
        'dimensionless', 'fixed', 'NOTE'),
    'PositiveGeometryEmergentSpaceTime.UnitarisedLS.reK': (
        'Real part of K-matrix unitarised partial wave: Re t = K/(1+σ²K²) (elastic model)',
        'dimensionless', 'variable', 'NOTE'),
}
# LeanCert2 certificate data (LEAN-CERT-2, 2026-10-28): one entry per generated symbol
_LC2_CERTS = {'abhyL5': 'ABHY eq. (5) n = 5 (planted PL1)', 'abhyL6': 'ABHY eq. (5) n = 6 (planted PL1)', 'abhyL7': 'ABHY eq. (5) n = 7 (planted PL1)',
              'brokenB1': 'forged dim-10 certificate for ABHY n = 6 (broken case B1, rejected)',
              'frwzw_k0p': 'FR-WZW k = 0, sigma = +1', 'frwzw_k0m': 'FR-WZW k = 0, sigma = -1', 'frwzw_k1p': 'FR-WZW k = 1, sigma = +1', 'frwzw_k1m': 'FR-WZW k = 1, sigma = -1'}
_LC2_PARTS = {'Mr': 'rows of the integer constraint matrix M', 'Mc': 'columns of M', 'Kr': 'rows of the kernel basis K', 'Kc': 'columns of K',
              'Pr': 'rows of the split matrix P', 'Qr': 'rows of the left inverse Q', 'Qc': 'columns of Q', 'd': 'certificate scale d'}
for _c, _cd in _LC2_CERTS.items():
    for _p, _pd in _LC2_PARTS.items():
        DEF_META['PositiveGeometryEmergentSpaceTime.LeanCert2.%s_%s' % (_c, _p)] = ('%s: %s, certificate data (aka %s_%s)' % (_cd, _pd, _c, _p), 'dimensionless', 'fixed', 'NOTE')

def dim_from_sig_doc(sig: str, doc: str, lean_name: str = '') -> str | None:
    """Safe dimension from type signature / docstring keywords / lean_name. None = leave unknown."""
    s, d = sig or '', (doc or '').lower()
    # dim-only curated overrides (DOC meaning kept; dimension from notes/headers)
    if lean_name in DEF_DIM:
        return DEF_DIM[lean_name]
    if '→ Prop' in s or s.strip() == 'Prop' or s.endswith(' Prop'):
        return 'dimensionless'
    if 'Bool' in s:
        return 'dimensionless'
    if s.strip() == 'Type' or '≃' in s or 'Submodule' in s or 'Submonoid' in s             or 'MulAction' in s or 'OrderParameter' in s or 'QuadraticForm' in s             or 'Set ' in s:
        return 'type'
    if 'Matrix' in s and ('ℚ' in s or 'ℤ' in s):
        return 'dimensionless'
    if s.startswith('List ') or s.startswith('Finset ') or 'ℕ × ℕ' in s:
        return 'dimensionless'
    # docstring keyword cues (conservative; natural-unit amplitudes → dimensionless)
    if 'masses²' in d or 'mass²' in d or 'mass^2' in d or 'mandelstam' in d             or 'planar variable' in d or 'planar invariant' in d             or 's-channel invariant' in d or 't-channel invariant' in d             or 'internal mass' in d or 'mass² of' in d:
        return 'mass²'
    if 'higgs vev' in d or 'decay constant' in d or ('meson mass' in d)             or d.startswith('pion mass') or ('string tension' in d):
        return 'mass'
    if any(k in d for k in (
            'low-energy constant', 'coupling', 'hypercharge', 'probability',
            'weight', 'legendre', 'eigenvector', 'correlation', 'entropy',
            'stochastic', 'hankel', 'moment of', 'signed measure', 'spectral measure',
            'canonical form', 'plücker', 'plucker', 'minor on', 'bracket',
            'adjacency', 'cartan', 'conductance', "lam's point", "lam point",
            'relative entropy', 'gibbs', 'symmetry factor', 'jacobian',
            'affine length', 'fusions', 'trace on', 'entropy rate',
            'partial wave', 'amplitude', 'wavefunction', 'residue polynomial',
            'contact amplitude', 'ordered amplitude', 'dressing', 'casimir',
            'random walk', 'stationary', 'multipole coefficient')):
        return 'dimensionless'
    if 'vvs coupling' in d or 'vvss coupling' in d or 'vvvv' in d:
        return 'dimensionless'
    if 'ε' in (doc or '') and ('·ε' in (doc or '').replace(' ', '') or 'ε·' in (doc or '').replace(' ', '')):
        return 'dimensionless'
    # ε·p style (polarisation · momentum)
    if 'ε' in (doc or '') and '·p' in (doc or '').replace(' ', '').lower():
        return 'mass'
    if 'vev' in d and 'difference' in d:
        return 'mass'
    if 'gram matrix' in d or ('dot product' in d and '4d' in d):
        return 'mass²'
    if '5th' in d and 'component' in d:
        return 'mass'
    if 'minkowski form' in d or 'minkowski product' in d:
        return 'mass²'
    if 'null momentum' in d or 'null momenta' in d:
        return 'mass'  # momentum components / spinor factors live in kinematic charts
    if 'spinor' in d and ('factor' in d or 'λ' in doc or 'configuration' in d):
        return 'dimensionless'
    if 'field `x' in d or 'field `m' in d:  # Gram4 fields: xij = dots, mi = masses
        if "field `m" in d:
            return 'mass'
        return 'mass²'
    if 'm² ∝' in d or 'm^2 ∝' in d or 'model a' in d and 'nambu' in d or 'model b' in d and 'ls' in d:
        return 'mass²'
    if 'polarisation' in d or 'polarization' in d:
        return 'dimensionless'
    if 'off-shell current' in d:
        return 'mass'  # current ~ mass×polarisation in these notes
    if 'numerator' in d and ('s-channel' in d or 't-channel' in d):
        return 'mass⁴'
    if 'contact term' in d and 'four-vector' in d:
        return 'mass⁴'
    if 'hidden-zero residual' in d or 'coefficient of the' in d and 'defect' in d:
        return 'dimensionless'  # EWZ1b Q-polys / N in script units
    if 'congruence action' in d or 'raw action map' in d or 'lorentz group' in d             or 'induced real-linear' in d or 'chart' in d and 'i | x' in d             or 'antilinear involution' in d or 'complexification' in d             or 'coordinates back' in d or 'sl(2) invariant' in d             or 'angle bracket' in d or 'undotted spinor' in d             or 'rank-one hermitian' in d:
        return 'type'
    return None

# Dimension-only fills when DOC meaning exists but keywords are thin (from module headers / adjacent comments).
DEF_DIM = {
    'PositiveGeometryEmergentSpaceTime.BR5p.Vec.add': 'type', 'PositiveGeometryEmergentSpaceTime.BR5p.Vec.neg': 'type', 'PositiveGeometryEmergentSpaceTime.BR5p.Vec.smul': 'type',
    'PositiveGeometryEmergentSpaceTime.BR5p.Vec.d4': 'type', 'PositiveGeometryEmergentSpaceTime.BR5p.Vec.d5': 'type', 'PositiveGeometryEmergentSpaceTime.BR5p.Vec.c': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.BR5p.s': 'mass²', 'PositiveGeometryEmergentSpaceTime.BR5p.tz': 'mass²',
    'PositiveGeometryEmergentSpaceTime.BR5p.Nbuilt': 'dimensionless',  # amplitude×props in script ℚ units
    'PositiveGeometryEmergentSpaceTime.BR5p.E': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.Assoc.br': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.Assoc.m5': 'dimensionless', 'PositiveGeometryEmergentSpaceTime.Assoc.omegaFan': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.Assoc.tri': 'dimensionless', 'PositiveGeometryEmergentSpaceTime.Assoc.vertex': 'mass²',  # planar X coords
    'PositiveGeometryEmergentSpaceTime.FT5aL.m0': 'mass', 'PositiveGeometryEmergentSpaceTime.FT5aL.m1': 'mass', 'PositiveGeometryEmergentSpaceTime.FT5aL.m2': 'mass',
    'PositiveGeometryEmergentSpaceTime.FT5aL.m3': 'mass',
    'PositiveGeometryEmergentSpaceTime.FT5aL.x01': 'mass²', 'PositiveGeometryEmergentSpaceTime.FT5aL.x02': 'mass²', 'PositiveGeometryEmergentSpaceTime.FT5aL.x03': 'mass²',
    'PositiveGeometryEmergentSpaceTime.FT5aL.x12': 'mass²', 'PositiveGeometryEmergentSpaceTime.FT5aL.x13': 'mass²', 'PositiveGeometryEmergentSpaceTime.FT5aL.x23': 'mass²',
    'PositiveGeometryEmergentSpaceTime.OrderParam.higgsVev': 'mass', 'PositiveGeometryEmergentSpaceTime.OrderParam.eta': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.OrderParam.m': 'dimensionless', 'PositiveGeometryEmergentSpaceTime.OrderParam.cact': 'type',
    'PositiveGeometryEmergentSpaceTime.OrderParam.gact': 'type', 'PositiveGeometryEmergentSpaceTime.OrderParam.diagMat': 'type',
    'PositiveGeometryEmergentSpaceTime.OrderParam.lorentzSet': 'type',
    'PositiveGeometryEmergentSpaceTime.Hankel.wC': 'dimensionless', 'PositiveGeometryEmergentSpaceTime.Hankel.wT': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.Hankel.hankel': 'dimensionless', 'PositiveGeometryEmergentSpaceTime.Hankel.hankel2': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.Hankel.moment': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.IsingLoop.det3': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.IsingTiling.br': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.KerrMinimal.massM': 'mass × length^ℓ', 'PositiveGeometryEmergentSpaceTime.KerrMinimal.coef': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.KerrMinimal.nullMom': 'mass',
    'PositiveGeometryEmergentSpaceTime.TP1b.v': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.TP1bMatrix.adjE8': 'dimensionless', 'PositiveGeometryEmergentSpaceTime.TP1bMatrix.cartanE8': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.SC2.bubble': 'type', 'PositiveGeometryEmergentSpaceTime.SC2.triangle': 'type', 'PositiveGeometryEmergentSpaceTime.SC2.sym': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.SC2b.bubbleCone': 'dimensionless', 'PositiveGeometryEmergentSpaceTime.SC2b.triCone': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.SC2b.slice3': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.Spinor.coords': 'mass',  # Minkowski coordinates recovered from Herm
    'PositiveGeometryEmergentSpaceTime.Null.outerH': 'type',
    'PositiveGeometryEmergentSpaceTime.MassiveSpinor.eps': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.MassiveSpinor.ang': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.MassiveSpinor.br': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.MassiveSpinor.u': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.SliceBridge.br2': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.SliceBridge.cfg4': 'mass', 'PositiveGeometryEmergentSpaceTime.SliceBridge.cfg6': 'mass',
    'PositiveGeometryEmergentSpaceTime.SliceBridge.splitPosL': 'dimensionless', 'PositiveGeometryEmergentSpaceTime.SliceBridge.splitNegL': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.SliceBridge.Xw': 'type', 'PositiveGeometryEmergentSpaceTime.SliceBridge.tau': 'type',
    'PositiveGeometryEmergentSpaceTime.PionBound.b3': 'dimensionless', 'PositiveGeometryEmergentSpaceTime.PionBound.J2': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.PionBound.A': 'dimensionless', 'PositiveGeometryEmergentSpaceTime.PionBound.Tpm': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.PionBound.T00': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.GB1a.mA2': 'mass²', 'PositiveGeometryEmergentSpaceTime.GB1a.mB2': 'mass²',
    'PositiveGeometryEmergentSpaceTime.MassShift.a00': 'dimensionless', 'PositiveGeometryEmergentSpaceTime.MassShift.a20': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.PG1.Lam': 'dimensionless', 'PositiveGeometryEmergentSpaceTime.PG1.MP2': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.SG1b.f': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.ScaleNoGo.LS': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.LSResidue.Ff2': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.LECRatio.P4': 'dimensionless', 'PositiveGeometryEmergentSpaceTime.LECRatio.g20': 'mass⁻⁴',
    'PositiveGeometryEmergentSpaceTime.LECRatio.g21': 'mass⁻⁴',
    # remaining thin-DOC fills (2026-10-15 unknowns pass)
    'PositiveGeometryEmergentSpaceTime.IsingOG.gp2': 'dimensionless', 'PositiveGeometryEmergentSpaceTime.IsingOG.gpY': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.conjAct': 'type',
    'PositiveGeometryEmergentSpaceTime.MassiveZero.fpoly': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.OrderParam.emEmbed': 'type',
    'PositiveGeometryEmergentSpaceTime.PositroidCells.dy': 'dimensionless',
    'PositiveGeometryEmergentSpaceTime.ShiftForced.Llin': 'dimensionless',
}
# fix Assoc.br key (ternary above is ugly) — already set via ternary to PositiveGeometryEmergentSpaceTime.Assoc.br


srcs = {}
def src(d):
    p = R/'lean'/(d['module'].replace('.', '/') + '.lean')
    if p not in srcs:
        srcs[p] = p.read_text().splitlines() if p.exists() else []
    return '\n'.join(srcs[p][d['line']-1:d['end_line']])
BIND_RE = re.compile(r'[({\[]\s*([^(){}\[\]:]+?)\s*:\s*([^(){}\[\]]+?)\s*[)}\]]')
def binders(d):
    s = src(d); head = s.split(':=', 1)[0]
    out = []
    for names, ty in BIND_RE.findall(head):
        for n in names.split():
            if re.match(r"^[A-Za-zα-ωΑ-Ωμσδλ_][\w'₀-₉]*$", n):
                out.append((n, ty.strip()[:60]))
    for names, ty in re.findall(r'∀\s*\(([^():]+):\s*([^()]+)\)', d.get('statement', '')):
        for n in names.split():
            if re.match(r"^[A-Za-zα-ωΑ-Ωμσδλ_][\w'₀-₉]*$", n):
                out.append((n, ty.strip()[:60]))
    return out

users = collections.defaultdict(set)
for d in decls:
    for u in d['type_uses'] + d['value_uses']:
        users[u['n']].add(d['name'])

def resolve_qty(module: str, tok: str):
    """Return (quantity_id, status) or (None, None)."""
    if tok in BIND_Q:
        q = BIND_Q[tok]
        st = MOD_Q.get(module, {}).get(q) or MEANING.get(q) and 'unknown'
        # if module lists it, use that status; else allow if binder is unambiguous
        if q in MOD_Q.get(module, {}):
            return q, MOD_Q[module][q]
        if tok in BIND_Q and len(tok) > 2:  # unambiguous long binder
            # use global majority from analysis if available
            for ak, info in REC.items():
                if REC_ALIAS.get(ak, ak) == q:
                    sc = info.get('status_counts', {})
                    maj = max(sc, key=sc.get) if sc else 'unknown'
                    return q, {'input': 'cited', 'free': 'free', 'fixed': 'fixed'}.get(maj, 'unknown')
            return q, 'unknown'
    # module-restricted short binders
    for q, toks in MOD_BIND.items():
        if tok in toks and q in MOD_Q.get(module, {}):
            return q, MOD_Q[module][q]
    return None, None

# kinematic variables (always 'variable', never free/fixed)
KIN = re.compile(r'^(s|t|u|s\d+|t\d+|u\d+|s12|s13|s23|X\d+|x\d+|y\d+|c\d\d|X|pl|p\d\d|mn|e\dp\d|ee\d\d|lam|lamt|eta|etat)$')

# 2026-10-20 (M12, approved by the author): "Also known as" aliases are kept in their own column, including those
# on generic "Auxiliary definition" docstrings (whose text is otherwise replaced by DEF_META) and "(aka …)" in DEF_META.
AKA_RE = re.compile(r'Also known as:\s*(.+?)(?:\.\s*$|\.\s+[A-Z]|\n\n|$)', re.S)
AKA_META = re.compile(r'\(aka ([^()]*(?:\([^()]*\)[^()]*)*)\)')
def split_aliases(txt):
    out, depth, cur = [], 0, ''
    for ch in txt:
        if ch in '([{':
            depth += 1
        elif ch in ')]}':
            depth -= 1
        if ch in ',;' and depth == 0:
            out.append(cur); cur = ''
        else:
            cur += ch
    out.append(cur)
    out = [a.replace('`', '').strip() for a in out]
    return [a for a in out if a and not re.match(r'^(docstring|def body|module section|module header)', a)]
def aliases_of(doc, meta_text=''):
    al = []
    for m in AKA_RE.finditer(doc or ''):
        al += split_aliases(re.sub(r'\s+', ' ', m.group(1)))
    for m in AKA_META.finditer(meta_text or ''):
        al += split_aliases(m.group(1))
    seen = []
    for a in al:
        if a not in seen:
            seen.append(a)
    return seen

rows = []
# ---- definitions ----
for d in decls:
    if d['kind'] != 'def' or AUX.search(d['name']):
        continue
    nm = d['name'].split('.')[-1]
    M = short(d['module'])
    doc = (d.get('doc') or '').strip()
    q, st = resolve_qty(M, nm)
    meta = DEF_META.get(d['name'])
    generic = bool(doc and GENERIC_DOC.match(doc))
    real_doc = bool(doc and not generic)
    src_tag = ''
    if real_doc:
        meaning = '[DOC] ' + doc
        if not st:
            st = 'unknown'
        src_tag = 'docstring'
    elif meta:
        meaning = f'[{meta[3]}] ' + meta[0]
        if not st or st == 'unknown':
            st = meta[2]
        src_tag = meta[3]
    elif q and q in MEANING:
        meaning = '[CURATED] ' + MEANING[q][0]
        if EXCLUSION_NOTE.get(q):
            meaning += ' | ' + EXCLUSION_NOTE[q]
        src_tag = 'CURATED+' + ('EXCLUSION' if EXCLUSION_NOTE.get(q) else 'analysis')
    else:
        meaning = 'unknown'
        st = st or 'unknown'
        src_tag = ''
    # dimension: quantity dict → DEF_META → signature/doc heuristics → unknown
    if q and q in MEANING:
        dim = MEANING[q][1]
    elif meta:
        dim = meta[1]
    else:
        dim = dim_from_sig_doc(d.get('statement', '').replace('\n', ' '), doc if real_doc else '', d['name']) or 'unknown'
    # If we have a real DOC but still unknown status, promote safe structural statuses
    if st == 'unknown' and dim in ('type',) and real_doc:
        st = 'variable'
    if st == 'unknown' and dim == 'dimensionless' and real_doc and (
            'Bool' in d.get('statement', '') or '→ Prop' in d.get('statement', '') or
            'List ' in d.get('statement', '') or 'Finset ' in d.get('statement', '')):
        st = 'variable'
    ths = sorted(u for u in users[d['name']] if u != d['name'])
    # constant defs with numeric RHS → fixed if no free binders of interest
    if st == 'unknown' and re.search(r':=\s*[-\d]', src(d)) and not binders(d):
        st = 'fixed'
    rows.append(dict(
        aliases='; '.join(aliases_of(doc, meta[0] if meta else '')),
        kind='definition', symbol=nm, lean_name=d['name'], module=M, quantity=q or '',
        meaning=meaning[:400], dimension=dim, status=st or 'unknown',
        sm_input=EXCLUSION_NOTE.get(q, '')[:120] if q else '',
        source=src_tag,
        signature=d['statement'].replace('\n', ' ')[:220],
        binders=' '.join(b for b, _ in binders(d)),
        n_users=len(ths), used_by=';'.join(x.split('.')[-1] for x in ths[:30]),
        component=str(comp_of.get(d['name'], '')),
        credited_users=sum(credit_of.get(x, False) for x in ths),
        line=d.get('line', '')))

# ---- parameters: aggregate binder (module, name), only if tagged or kinematic ----
agg = collections.defaultdict(lambda: dict(types=collections.Counter(), decls=set(), comps=set()))
for d in decls:
    M = short(d['module'])
    for b, ty in binders(d):
        a = agg[(M, b)]
        a['types'][ty] += 1
        a['decls'].add(d['name'])
        a['comps'].add(comp_of.get(d['name']))

# also emit one row per (module, known quantity) from MOD_Q even if binder names differ
seen_mq = set()
# Binder overrides (PositiveGeometryEmergentSpaceTime review 2026-10-20): binders the KIN pattern mislabels as kinematics. Source: module headers and
# notes/REVIEW-HANDOFF-MAP-DELTAS-2026-10-20.md (lam = λ charge vector, τ / t = torus parameter).
BINDER_OVERRIDE = {
    ('FL1Z', 'r'): ('positive dimensionless ratio r = D2²/D3² (hierarchy_ratio_surj)', 'variable',
        '[CURATED] arbitrary positive ratio r realised as D2²/D3² (the role of ρ = Δm²sol/Δm²atm); not a mass scale. Also known as: hierarchy ratio, ρ target', 'dimensionless'),
    ('GB1a', 'N'): ('glueball level index N (Nambu–Goto spectrum)', 'variable',
        '[CURATED] glueball level index N of the Nambu–Goto closed-string spectrum, NOT N_c '
        '(notes/LEAN-NAMING-MAP-2026-10-15.md, Deferred table)', 'integer'),
    ('BridgePLCharge', 'lam'): ('U(1) charge vector λ (column-torus cocharacter)', 'variable',
        '[CURATED] U(1) charge vector λ. Also known as: hypercharge assignment, cocharacter of the column torus (t = exp(τλ))', 'dimensionless'),
    ('BridgePLCharge', 't'): ('column-torus parameter t', 'variable',
        '[CURATED] column-torus element acting as P ↦ P·diag(t). Also known as: t = exp(τλ), torus parameter', 'dimensionless'),
}
# 2026-10-20 (M12, approved by the author): physical binders with no row get one. Physical = scalar type and a
# physics symbol (masses, F/f decay constants, couplings, Regge α′/α₀, D, N, charges, Adler zero, shift, LECs, β coeffs,
# scales). Meaning is taken from a module docstring/comment that names the binder (backticked, or `b =` / `b ∈` / `b :`),
# quoted with its line; if none names it, the row says "unverified" and nothing is guessed.
PHYS_BINDER = re.compile(r"^(m|M|m\d+|M\d+|m[A-Za-z_]\w*|M[A-Za-z_]\w*|F\d*|Fpi\w*|f|fpi\w*|g|g[A-Za-z0-9_]\w*|lam\d\w*|ap'?|"
                         r"alpha\w*|α\w*|a0|D|N|N\w+|nf|n_f|y[A-Za-z]\w*|Q[a-z]?|sA|σ|sigma\w*|delta|δ|d|b\d|L\d+|l\d+|"
                         r"v|vev|mu|μ|Lam|Λ\w*|r)$")
SCALAR_T = re.compile(r'^(ℝ|ℚ|ℕ|ℤ|ℂ)$')
PHYS_FILL_Q = ('physical binder (docstring)', 'physical binder (unverified)')
PHYS_FILLED = []
# hypercharge binders that only appear as arguments of the anomaly conditions (definition, not docstring)
PHYS_CURATED = {(M, y): (f'U(1)_Y hypercharge `{y}`: argument of `STRUCT2.ACCN (N_c yQ yu yd yL ye)` (STRUCT2.lean:15), '
                         'the N_c-colour anomaly conditions; normalisation Q = T₃ + Y (naming map: hypercharges yQ … ye)')
                for M in ('STRUCT2', 'STRUCT3', 'R4Indep') for y in ('yQ', 'yu', 'yd', 'yL', 'ye')}
_modsrc = {}
def binder_doc(M, b):
    """First docstring/comment line in module M that names binder b; (text, line) or None."""
    if M not in _modsrc:
        fs = sorted({d['module'] for d in decls if short(d['module']) == M})
        txt = []
        for mod in fs:
            pth = R/'lean'/(mod.replace('.', '/') + '.lean')
            if pth.exists():
                txt.append((pth.name, pth.read_text().splitlines()))
        _modsrc[M] = txt
    eb = re.escape(b)
    pats = [re.compile(r'`' + eb + r'`'), re.compile(r'(?<![\w\'])' + eb + r'\s*(=|∈|:|≔|is |denotes|means)(?!=)')]
    for pat in pats:
        for fname, lines in _modsrc[M]:
            inside = False
            for i, ln in enumerate(lines, 1):
                st = ln.strip()
                opens = st.startswith('/-')
                if opens:
                    inside = True
                is_doc = inside or st.startswith('--')
                if is_doc and pat.search(ln) and 'Auxiliary definition' not in ln:
                    return re.sub(r'\s+', ' ', st.lstrip('/-!').rstrip('-/').strip())[:260], f'{fname}:{i}'
                if inside and '-/' in ln:
                    inside = False
    return None

SUP = str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹')
def display_forms(b):
    """Printed forms of a binder used in docstrings: trailing digit → superscript (F2 → F², M2 → M²),
    ap → α′, alpha0 / a0 → α₀, sA → s_A, d → δ."""
    f = []
    m = re.match(r'^([A-Za-z]+?)(\d)$', b)
    if m:
        f.append(m.group(1) + m.group(2).translate(SUP))
    f += {'ap': ['α′', "α'"], 'alpha0': ['α₀'], 'a0': ['α₀', 'a₀'], 'sA': ['s_A'], 'd': ['δ']}.get(b, [])
    m = re.match(r'^y([A-Za-z])$', b)
    if m:
        f.append('y_' + m.group(1))
    return f
decl_doc_by_binder = collections.defaultdict(list)
for d in decls:
    if d.get('doc') and not GENERIC_DOC.match(d['doc']):
        for bb, _ in binders(d):
            decl_doc_by_binder[(short(d['module']), bb)].append(d)
def binder_display_doc(M, b):
    """Docstring of a declaration that has binder b and prints it in a display form; (text, where, form) or None."""
    for form in display_forms(b):
        pat = re.compile(r'(?<![\w])' + re.escape(form) + r'(?![\w₀-₉⁰-⁹])')
        for d in sorted(decl_doc_by_binder[(M, b)], key=lambda x: x['name']):
            if pat.search(d['doc']):
                return re.sub(r'\s+', ' ', d['doc'])[:240], f"docstring of {d['name'].split('.')[-1]}", form
    return None

for (M, b), a in agg.items():
    q, st = resolve_qty(M, b)
    if (M, b) in BINDER_OVERRIDE:  # 2026-10-22 (FL-1Z): curated binder meaning wins over the keyword resolver
        q = None
    ty = a['types'].most_common(1)[0][0]
    if q is None and b in MOD_Q.get(M, {}):  # binder literally named after a module quantity (STRUCT3 `N_gen`)
        q, st = b, MOD_Q[M][b]
    if q is None and (M, b) not in BINDER_OVERRIDE and PHYS_BINDER.match(b) and SCALAR_T.match(ty) \
            and not KIN.match(b):
        hit = binder_doc(M, b)
        hit2 = None if hit else binder_display_doc(M, b)
        if (M, b) in PHYS_CURATED:
            q, st, meaning, dim = PHYS_FILL_Q[0], 'unknown', '[CURATED] ' + PHYS_CURATED[(M, b)], 'rational (U(1)_Y)'
        elif hit:
            q, st, meaning, dim = PHYS_FILL_Q[0], 'unknown', f'[DOC-BINDER auto] {hit[0]} ({hit[1]})', 'unknown'
        elif hit2:
            q, st, meaning, dim = PHYS_FILL_Q[0], 'unknown', \
                f'[DOC-BINDER auto] `{b}` printed as {hit2[2]} in {hit2[1]}: {hit2[0]}', 'unknown'
        else:
            q, st, meaning, dim = PHYS_FILL_Q[1], 'unknown', \
                f'unverified: no docstring or comment in {M} names `{b}`; meaning not guessed', 'unknown'
    if q is None and (M, b) in BINDER_OVERRIDE:
        q, st, meaning, dim = BINDER_OVERRIDE[(M, b)]
    elif q is None:
        if KIN.match(b):
            q, st, meaning, dim = 'kinematics (Mandelstam / planar / spinor)', 'variable', \
                '[CURATED] kinematic invariant or spinor/Plücker placeholder', 'mass² or mass^(1/2)'
        elif ty.startswith(('Prop', 'Type', 'Sort')) or re.match(r'^(h|hh|hx|hy|hz|hm|hg|hi|hj|hk|hn|hab)', b):
            continue  # proofs / hypotheses
        elif re.match(r'^(i|j|k|n|l)$', b) and ('ℕ' in ty or 'Fin' in ty or 'Nat' in ty):
            q, st, meaning, dim = 'index', 'variable', '[CURATED] discrete index', 'dimensionless'
        else:
            continue  # do not invent unknowns for every binder
    elif q not in PHYS_FILL_Q:
        meaning = '[CURATED] ' + MEANING.get(q, (q,))[0]
        if EXCLUSION_NOTE.get(q):
            meaning += ' | ' + EXCLUSION_NOTE[q]
        dim = MEANING.get(q, ('', 'unknown'))[1]
    dl = sorted(a['decls'])
    key = (M, q or b)
    if q in PHYS_FILL_Q:
        PHYS_FILLED.append((M, b, meaning))
    seen_mq.add(key)
    pf = q in PHYS_FILL_Q
    rows.append(dict(
        aliases='; '.join(aliases_of(meaning)) if (M, b) in BINDER_OVERRIDE else '',
        kind='parameter', symbol=b, lean_name=f'{M}::{b}', module=M, quantity='' if pf else (q or ''),
        meaning=meaning[:400], dimension=dim, status=st or 'unknown',
        sm_input=EXCLUSION_NOTE.get(q, '')[:120] if q and not pf else '',
        source=('binder docstring (M12 2026-10-20)' if q == PHYS_FILL_Q[0] else 'binder, unverified (M12 2026-10-20)') if pf else
               'binder + analysis.json/EXCLUSION' if q and q != 'kinematics (Mandelstam / planar / spinor)' and q != 'index' else 'binder',
        signature=ty, binders='', n_users=len(dl),
        used_by=';'.join(x.split('.')[-1] for x in dl[:30]),
        component=';'.join(str(c) for c in sorted(c for c in a['comps'] if c is not None)),
        credited_users=sum(credit_of.get(x, False) for x in dl), line=''))

# module-level quantity rows for MOD_Q entries with no binder hit
for M, qs in MOD_Q.items():
    for q, st in qs.items():
        if (M, q) in seen_mq:
            continue
        meaning = '[CURATED] ' + MEANING.get(q, (q,))[0]
        if EXCLUSION_NOTE.get(q):
            meaning += ' | ' + EXCLUSION_NOTE[q]
        # find components of this module
        comps = sorted({comp_of[n['name']] for n in T['nodes'] if short(n['module']) == M})
        rows.append(dict(
            aliases='; '.join(aliases_of(MEANING.get(q, ('',))[0])),
            kind='parameter', symbol=q, lean_name=f'{M}::{q}', module=M, quantity=q,
            meaning=meaning[:400], dimension=MEANING.get(q, ('', 'unknown'))[1],
            status=st, sm_input=EXCLUSION_NOTE.get(q, '')[:120],
            source='analysis.json recurring_params / EXCLUSION (module-level; binder name may differ)',
            signature='', binders='', n_users=0, used_by='',
            component=';'.join(map(str, comps)), credited_users=0, line=''))

rows.sort(key=lambda r: (r['kind'], r['module'], r['symbol']))
F = ['kind', 'symbol', 'lean_name', 'module', 'quantity', 'meaning', 'dimension', 'status',
     'sm_input', 'source', 'signature', 'binders', 'n_users', 'used_by', 'component',
     'credited_users', 'line', 'aliases']
with open(R/'graph/lean-glossary.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, F); w.writeheader(); w.writerows(rows)

# ---- alias report (kept, not dropped): an alias naming two or more different glossary entries is reported as broken ----
alias_map = collections.defaultdict(list)
for r in rows:
    for a in filter(None, (x.strip() for x in r['aliases'].split(';'))):
        alias_map[a].append(r)
# broken = the alias names entries with different symbols that are not the same glossary quantity
BROKEN_ALIASES = {}
for a, rs in sorted(alias_map.items()):
    ids = {(r['quantity'] or r['symbol']) for r in rs}
    if len(ids) > 1:
        BROKEN_ALIASES[a] = sorted({r['lean_name'] for r in rs})
json.dump({'note': 'Aliases parsed from "Also known as:" docstrings and "(aka …)" notes; kept in the CSV column `aliases`. '
                   'An alias listed under two or more different entries is ambiguous ("broken") and is reported here, not '
                   'dropped. Generated by scripts/lean_glossary.py (M12, 2026-10-20).',
           'n_entries_with_aliases': sum(1 for r in rows if r['aliases']),
           'n_distinct_aliases': len(alias_map),
           'broken_aliases': BROKEN_ALIASES},
          open(R/'graph/lean-glossary-aliases.json', 'w'), indent=1, ensure_ascii=False)

# ---- overlaps: same quantity across components / modules ----
qinfo = collections.defaultdict(lambda: dict(mods=set(), comps=set(), names=set(), status=collections.Counter(), defs=set()))
for r in rows:
    q = r['quantity']
    if not q or q in ('kinematics (Mandelstam / planar / spinor)', 'index'):
        continue
    o = qinfo[q]
    o['mods'].add(r['module']); o['names'].add(r['symbol']); o['status'][r['status']] += 1
    if r['kind'] == 'definition':
        o['defs'].add(r['lean_name'])
    for c in str(r['component']).split(';'):
        if c != '':
            o['comps'].add(int(c))
over = sorted(
    [{'quantity': k, 'n_components': len(v['comps']), 'n_modules': len(v['mods']),
      'modules': sorted(v['mods']), 'components': sorted(v['comps']),
      'symbols': sorted(v['names']), 'status_counts': dict(v['status']),
      'defs': sorted(v['defs'])[:20],
      'bridge_note': EXCLUSION_NOTE.get(k, MEANING.get(k, ('',))[0] if k in MEANING else '')}
     for k, v in qinfo.items()],
    key=lambda x: (-x['n_components'], -x['n_modules']))

# same short def name, different modules (potential same-quantity collision)
dn = collections.defaultdict(set)
for r in rows:
    if r['kind'] == 'definition':
        dn[r['symbol']].add(r['module'])
# filter to interesting collisions (exclude trivial aux already filtered)
PHYS_COLL = {k: sorted(v) for k, v in dn.items() if len(v) > 1 and k not in
             {'ctorIdx', 'recOn', 'noConfusionType', 'eta'}}

counts = collections.Counter(r['status'] for r in rows)
kinds = collections.Counter(r['kind'] for r in rows)
json.dump({'counts': dict(counts), 'kind_counts': dict(kinds),
           'quantity_overlaps': over, 'def_name_collisions': PHYS_COLL,
           'n_entries': len(rows), 'n_quantities': len(qinfo)},
          open(R/'graph/lean-glossary-overlaps.json', 'w'), indent=1)

# ---- figure ----
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
csize = collections.Counter(comp_of.values())
ccred = collections.Counter(c for n, c in comp_of.items() if credit_of.get(n))
cmods = collections.defaultdict(set)
for n in T['nodes']:
    cmods[n.get('component')].add(short(n['module']))
G = nx.Graph()
for o in over:
    qs = o['quantity']
    comps = o['components']
    for i in range(len(comps)):
        for j in range(i + 1, len(comps)):
            a, b = comps[i], comps[j]
            if G.has_edge(a, b):
                G[a][b]['q'].append(qs)
            else:
                G.add_edge(a, b, q=[qs])
# keep large or well-connected components
keep = [c for c in G.nodes if csize[c] >= 5 or G.degree(c) >= 2]
H = G.subgraph(keep).copy()
# drop edges that only share one weak quantity if too dense: keep top quantities
top_q = {o['quantity'] for o in over[:12]}
for a, b, e in list(H.edges(data=True)):
    e['q'] = [q for q in e['q'] if q in top_q]
    if not e['q']:
        H.remove_edge(a, b)
H.remove_nodes_from([n for n in list(H.nodes) if H.degree(n) == 0 and csize[n] < 15])

plt.figure(figsize=(15, 11))
pos = nx.spring_layout(H, k=1.4, seed=11, weight=None)
qs = sorted({q for _, _, e in H.edges(data=True) for q in e['q']})
cmap = plt.get_cmap('tab20')
qcol = {q: cmap(i % 20) for i, q in enumerate(qs)}
for a, b, e in H.edges(data=True):
    for i, q in enumerate(e['q'][:3]):
        x0, y0 = pos[a]; x1, y1 = pos[b]
        off = (i - 1) * 0.008
        plt.plot([x0 + off, x1 + off], [y0 + off, y1 + off], color=qcol[q], lw=1.6, alpha=.7)
sizes = [50 + 8 * csize[c] for c in H.nodes]
cols = ['#c0392b' if ccred[c] else '#2980b9' for c in H.nodes]
nx.draw_networkx_nodes(H, pos, node_size=sizes, node_color=cols, alpha=.9, edgecolors='white', linewidths=.5)
labels = {}
for c in H.nodes:
    ms = ','.join(sorted(cmods[c]))
    if len(ms) > 32:
        ms = ms[:30] + '…'
    labels[c] = f'C{c} ({csize[c]})\n{ms}'
nx.draw_networkx_labels(H, pos, labels, font_size=6.5)
for q in qs:
    plt.plot([], [], color=qcol[q], lw=3, label=q)
plt.legend(loc='lower left', fontsize=7.5, ncol=2, title='shared quantity (candidate bridge)')
plt.title('Theorem-graph components linked by shared physical quantities — 2026-10-15\n'
          'Node size ∝ #decls; red = contains a credited theorem. Edges = shared glossary quantity '
          '(not Lean import edges).')
plt.axis('off'); plt.tight_layout()
plt.savefig(R/'figures/glossary-overlaps-2026-10-15.png', dpi=150)
plt.close()

# ---- HTML ----
# slim rows for HTML (drop long used_by if huge)
data = json.dumps([{k: r[k] for k in F} for r in rows], ensure_ascii=False)
html_out = f"""<!doctype html><html><meta charset=utf-8><title>PositiveGeometryEmergentSpaceTime Lean glossary 2026-10-15</title>
<style>
body{{font:13px/1.35 system-ui,sans-serif;margin:16px;color:#222}}
input,select{{margin:4px 8px 4px 0;padding:4px}}
table{{border-collapse:collapse;width:100%;margin-top:8px}}
td,th{{border:1px solid #ccc;padding:3px 5px;vertical-align:top;max-width:320px;overflow-wrap:anywhere}}
th{{background:#f0f0f0;cursor:pointer;position:sticky;top:0}}
tr.fixed td:nth-child(8){{background:#d5f5e3}} tr.cited td:nth-child(8){{background:#fdebd0}}
tr.free td:nth-child(8){{background:#fadbd8}} tr.variable td:nth-child(8){{background:#d6eaf8}}
tr.unknown td:nth-child(8){{background:#eee;color:#666}}
.meta{{color:#555;max-width:900px}}
</style>
<h1>PositiveGeometryEmergentSpaceTime Lean glossary — {len(rows)} entries</h1>
<p class=meta>Generated 2026-10-15; regenerated 2026-10-20 with the H4/M12 fixes (GB1a N = glueball level index; α₀ = intercept;
physical binders filled from docstrings or marked unverified; aliases column, broken aliases in
<code>graph/lean-glossary-aliases.json</code>). Built from <code>graph/raw_decls.jsonl</code> (686 thm + 295 def) and
<code>lean/PositiveGeometryEmergentSpaceTime/*.lean</code>. Meaning: <b>[DOC]</b> = Lean docstring (verbatim);
<b>[NOTE]</b>/<b>[CURATED]</b> = hand dictionary from module headers / analysis.json / EXCLUSION —
never a guess. Unknowns pass 2026-10-15 filled DEF_META for GraphExport placeholders. Status: <b>fixed</b> (forced by geometry/proof), <b>cited</b> (literature/data input),
<b>free</b> (undetermined / ruled out as geometry-fixed by EXCLUSION), <b>variable</b> (kinematic/index),
<b>unknown</b>. Credit and Lean theorems unchanged; AUTORESEARCH-STOP left in place.</p>
<p>Counts — {dict(kinds)}; status {dict(counts)}. Quantities with multi-component reach: {len(over)}.</p>
<input id=q size=55 placeholder="search symbol / module / meaning / quantity…">
<select id=s><option value="">all statuses</option>
<option>fixed</option><option>cited</option><option>free</option><option>variable</option><option>unknown</option></select>
<select id=k><option value="">all kinds</option><option>definition</option><option>parameter</option></select>
<span id=n></span>
<table><thead><tr>{''.join(f'<th data-c="{c}">{c}</th>' for c in F)}</tr></thead>
<tbody id=b></tbody></table>
<script>
const D={data}; const F={json.dumps(F)}; let SK=null, SD=1;
document.querySelectorAll('th').forEach(th=>th.onclick=()=>{{const c=th.dataset.c; if(SK===c)SD=-SD; else{{SK=c;SD=1}}
D.sort((a,b)=>SD*String(a[c]).localeCompare(String(b[c]),undefined,{{numeric:true}})); rend()}});
function esc(s){{return String(s).replace(/[&<>]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;'}})[c])}}
function rend(){{const q=document.getElementById('q').value.toLowerCase();
const s=document.getElementById('s').value,k=document.getElementById('k').value; let h='',n=0;
for(const x of D){{if(s&&x.status!==s)continue;if(k&&x.kind!==k)continue;
if(q&&!F.some(f=>String(x[f]).toLowerCase().includes(q)))continue; n++;
h+='<tr class="'+x.status+'">'+F.map(f=>'<td>'+esc(x[f])+'</td>').join('')+'</tr>'}}
document.getElementById('b').innerHTML=h; document.getElementById('n').textContent=n+' shown'}}
document.getElementById('q').oninput=rend; document.getElementById('s').onchange=rend;
document.getElementById('k').onchange=rend; rend();
</script></html>"""
(R/'graph/lean-glossary.html').write_text(html_out)

print('ENTRIES', len(rows))
print('KINDS', dict(kinds))
print('STATUS', dict(counts))
print('N_QUANTITIES', len(qinfo))
print('TOP_OVERLAPS')
for o in over[:12]:
    print(f"  {o['quantity']}: {o['n_components']} comps / {o['n_modules']} mods | {o['status_counts']} | mods={o['modules'][:8]}")
print('COLLISIONS', PHYS_COLL)
print('ALIASES', sum(1 for r in rows if r['aliases']), 'entries;', len(alias_map), 'distinct;', len(BROKEN_ALIASES), 'broken:',
      {a: [x.split('.')[-1] for x in v] for a, v in BROKEN_ALIASES.items()})
print('PHYS_BINDER_ROWS', sum(1 for r in rows if 'M12' in r['source']),
      'unverified', sum(1 for r in rows if 'unverified (M12' in r['source']))
print('FIG', H.number_of_nodes(), 'nodes', H.number_of_edges(), 'edges')
