"""Hand verdicts for the blueprint pass of 2026-11-03 (judged in batches from out/claims.json).

Key = claim id in out/claims.json. Fields: t = row type (CLAIM | LISTING | SCOPE | META | PAPER),
v = verdict (MATCH | OVERSTATES | UNDERSTATES | MISSING-LEAN | NAME-ONLY; none for META/PAPER),
rung = reassigned rung (GENERAL rows only), d = Lean declarations (short names under PositiveGeometryEmergentSpaceTime., or
"mod:<Module>" = all theorems of that module), hid = hidden hypotheses, n = note, rw = proposed rewording.
SCOPE = a sentence saying what Lean does NOT cover; MATCH means the disclaimer is accurate.
META = preamble, tag definitions, method text or figure code with no checkable Lean claim.
PAPER = tagged proved on paper only (\\proved / \\PAPERPROVED); not a Lean claim, not judged.
"""
M, O, NO = "MATCH", "OVERSTATES", "NAME-ONLY"
MR1B_RW = ("The Legendre decompositions of the $\\rho_3$ and $f_4$ residues (\\leanname{rho3\\_residue}, "
           "\\leanname{f4\\_residue}) and the arithmetic giving $5/16$ and $49/240$ from their coefficients "
           "(\\leanname{rho3\\_ratio}, \\leanname{f4\\_ratio}) are \\PROVED; the step from Legendre coefficient "
           "to coupling ($c_J=-g^2m^2$, the normalisation of AHRV eq.~2.12, transcribed by hand) is a stated convention, "
           "not in Lean.")
V = {
 # ---- MR-1b
 18: dict(t="LISTING", v=M, d=["LSResidue.rho3_ratio"], n="Listing shows the ratio arithmetic; matches what it is printed as."),
 19: dict(t="CLAIM", v=O, d=["LSResidue.rho3_residue", "LSResidue.f4_residue", "LSResidue.rho3_ratio", "LSResidue.f4_ratio"],
          hid="J-coefficient = -g^2 m^2 (AHRV eq. 2.12 normalisation; convention, docstring only)",
          n="Lean proves the residue decompositions and the ratio arithmetic; the coefficient->coupling map is not mechanised (module docstring says so). 'The ratios ... are PROVED' reads as the physical coupling ratios.",
          rw=MR1B_RW),
 7: dict(t="CLAIM", rung="MR-1b", v=O, d=["LSResidue.rho3_ratio", "LSResidue.f4_ratio"],
         hid="same as II:302", n="Abstract: 'blind LS coupling ratios 5/16 and 49/240 PROVED' has the same gap as the MR-1b card.",
         rw="... blind Lovelace--Shapiro coupling ratios $5/16$ and $49/240$ (Legendre arithmetic \\PROVED; coefficient-to-coupling map a stated convention) agree with both width sources ..."),
 # ---- H-T5
 20: dict(t="CLAIM", v=M, d=["IsingTiling.sign_flip_certificate"], hid="one exact point; 40/40 is SIM", n="'exact point PROVED' = sign_flip_certificate at one rational point."),
 21: dict(t="CLAIM", v=M, d=["IsingTiling.sign_flip_certificate", "IsingTiling.C_orth"],
          hid="'star network' is carried by the definition of C/Λ (docstring), not a theorem; unique positive preimage is SIM",
          n="Lean: positivity of the cyclic isingBracket entries and three sign flips at one exact point."),
 # ---- INT-1
 22: dict(t="LISTING", v=M, d=["IntChamber.invariant_chamber_constant"]),
 23: dict(t="CLAIM", v=M, d=["IntChamber.invariant_chamber_constant", "IntChamber.jump_only_on_wall", "IntChamber.mass_shift"],
          hid="n=5 only; invariant = any F of the labelled vertex set vertexType (enough for face-lattice integers of a polygon); offsets c13,c14,c24 with mass offsets as a translation (mass_shift)",
          n="Prose scope (n=5) matches."),
 # ---- LEAN-CERT-1
 24: dict(t="LISTING", v=M, d=["LeanCert.nacc_eq_two"]),
 25: dict(t="CLAIM", v=M, d=["LeanCert.checkZero_spec", "LeanCert.checkSplit_spec", "LeanCert.checkInj_spec", "LeanCert.finrank_ker",
                             "LeanCert.abhy5_finrank", "LeanCert.abhy6_finrank", "LeanCert.abhy7_finrank", "LeanCert.nacc_eq_two", "LeanCert.acc_iff"],
          hid="the ABHY constraint matrices and the ACC set are literal data (DEF rows)", n="finranks 5/9/14 = n(n-3)/2; acc_iff gives the full rational solution set."),
 26: dict(t="META"),
 # ---- BR-4
 27: dict(t="CLAIM", v=M, d=["BR4.no_scale", "BR4.stabilizer_blind", "BR4.eigen_blind", "BR4.LS_blind", "BR4.no_scale_witness"],
          hid="needs a scalar c with c^k ≠ 1 and σ x ≠ 0", n="Earlier BR-4 alignment note: ALIGNED."),
 28: dict(t="CLAIM", v=M, d=["BR4.no_scale"], hid="c^k ≠ 1, σ x ≠ 0"),
 9: dict(t="LISTING", rung="BR-4", v=M, d=["BR4.no_scale"]),
 # ---- MR-3
 29: dict(t="LISTING", v=M, d=["MassiveLS.positivity_forces_chiral"]),
 30: dict(t="CLAIM", v=M, d=["MassiveLS.positivity_forces_chiral", "MassiveLS.level2_decomp"], hid="0 ≤ r < 1/2, f2 level only; hpos is the literal c0 expression"),
 31: dict(t="CLAIM", v=M, d=["MassiveLS.positivity_forces_chiral", "MassiveLS.level2_decomp"],
          hid="'only the J=0 coefficient can fail' is read off level2_decomp; nonnegativity of the J=1,2 coefficients is not a separate theorem",
          n="Mild: the 'only' clause is by inspection of the decomposition, not a stated lemma."),
 # ---- SURF-1'
 32: dict(t="CLAIM", v=M, d=["Surf1.no_sign_coherent_N"], hid="d-type Tr φ³ colour model; N ≥ 3; boxU ≅ K3,3 by docstring (pilot cross-check)", n="Pilot row reused."),
 33: dict(t="CLAIM", v=M, d=["Alignment.Surf1Sanity.Ktri_eq", "Alignment.Surf1Sanity.blind_theta", "Alignment.Surf1Sanity.blind_K4", "Alignment.Surf1Sanity.blind_dsq"], n="Pilot row reused."),
 34: dict(t="SCOPE", v=M, n="K3,3 vector is SIMULATED in the pilot (kernel OOM); disclaimer accurate."),
 35: dict(t="CLAIM", v=M, d=["Alignment.Surf1Sanity.claimEnumerated_of_K33"], hid="conditional on the one evaluated K3,3 vector", n="Pilot row reused."),
 36: dict(t="CLAIM", v=M, d=["Surf1.no_sign_coherent_N"]),
 10: dict(t="LISTING", rung="SURF-1′", v=M, d=["Surf1.no_sign_coherent_N"]),
 8: dict(t="CLAIM", rung="SURF-1′", v=O, d=["Surf1.no_sign_coherent_N"], hid="d-type Tr φ³ colour model; triangle-type vs crossed-box (K3,3) graphs; kinematic sign assumption",
         n="Abstract drops the model scope the pilot said abstract-level wording must carry.",
         rw="SURF-1$'$: in the d-type $\\mathrm{Tr}\\,\\phi^3$ colour model, no $N\\ge3$ makes the one-loop colour factors of the triangle-type and crossed-box ($K_{3,3}$) graphs sign-coherent \\PROVED; robust under the convention re-check \\SIM."),
 # ---- JORD-1
 37: dict(t="CLAIM", v=O, d=["Jord1.gsm_not_pointwise_stabiliser"],
          hid="gsm := {D | IsDer D ∧ D·E1 = 0 ∧ D preserves h3(ℂ)}, a set of derivation matrices on ℚ^27 (Lie algebra stab(E1) ∩ setstab(h3(C))); stab S is the pointwise stabiliser inside Der",
          n="Group vs algebra: Lean is about derivations (the Lie algebra), the prose and heading say 'gauge group'.",
          rw="We proved that the SM gauge algebra $\\mathfrak g_{\\rm SM}=\\mathrm{stab}(E_1)\\cap\\mathrm{setstab}(h_3(\\mathbb C))\\subset\\mathrm{Der}\\,J_3(\\mathbb{O})$ (over $\\mathbb{Q}^{27}$) is not the pointwise stabiliser, within $\\mathrm{Der}\\,J_3(\\mathbb{O})$, of any subset of $J_3(\\mathbb{O})$ \\PROVED. (Heading II:430: ``the SM algebra is not a pointwise stabiliser''.)"),
 11: dict(t="LISTING", rung="JORD-1", v=M, d=["Jord1.gsm_not_pointwise_stabiliser"], n="Listing literal; the overstatement is in the prose around it (II:438, heading II:430)."),
 # ---- TRIALITY-WHY
 38: dict(t="LISTING", v=M, d=["TrialityWhy.window_iff"]),
 39: dict(t="CLAIM", v=M, d=["TrialityWhy.b3_exact_iff", "TrialityWhy.z9_exact_iff"], n="Cited result; Lean also proves 3∣N for B3 and Z9."),
 40: dict(t="CLAIM", v=M, d=["TrialityWhy.window_iff", "TrialityWhy.null_count_d3", "TrialityWhy.null_card"], hid="0 < k", n="exactness = anomaly window is SIM; '12 of 170' = null_count_d3, null_card."),
 92: dict(t="CLAIM", v=M, d=["TrialityWhy.window_iff"]),
 # ---- GRADED-POSITROID
 41: dict(t="LISTING", v=M, d=["GradedPositroid.graded_cubic_iff_acc"]),
 42: dict(t="CLAIM", v=M, d=["GradedPositroid.graded_cubic_iff_acc"], hid="weights genW are the hand-entered Cartan grading of the 15 Weyl states (DEF row)"),
 # ---- FL-1Z
 43: dict(t="CLAIM", v=M, d=["FL1Z.D3_rank_one", "FL1Z.D3_det_zero"], hid="ω³ = 1; D3 is a literal matrix whose identification with the Zee--Babu mass matrix at τ=ω is docstring only",
          n="Theorem MATCH; definition risk recorded as DEF row FL1Z.D3 (NAME-ONLY)."),
 # ---- EW-Z1b
 44: dict(t="LISTING", v=M, d=["EWZ1b.forced"]),
 45: dict(t="CLAIM", v=M, d=["EWZ1b.forced", "EWZ1b.zero_of_gauge", "EWZ1b.N_decomp"],
          hid="N is the script-generated residual (sims/ewz1b/mklean.py) already restricted to the hidden-zero locus; forced uses two numeric points on it",
          n="Theorem MATCH; faithfulness of N to the Feynman rules is a script, not Lean (DEF row EWZ1b.N, NAME-ONLY)."),
 # ---- CASCADE
 46: dict(t="LISTING", v=M, d=["Cascade1.em_n5_zero_iff"]),
 47: dict(t="CLAIM", v=M, d=["Cascade1.split5_of_rel_33_1", "Cascade1.split5_of_rel_35_1", "Cascade1.em_n5_zero_iff"],
          hid="stage-3 relation hypotheses hR; 10 splits = split5_of_rel_33_i, split5_of_rel_35_i, i=1..5", n="'for all masses on the stage-3 relations' literal."),
 48: dict(t="CLAIM", v=M, d=["Cascade1bR2.c_transport", "Cascade1bR2.zeros6_of_rel_skinny", "Cascade1bR2.zeros6_of_rel_square"], hid="c_transport is a linear translation identity"),
 # ---- LEAN-CERT-2
 49: dict(t="META"), 50: dict(t="META", n="SIM null result, no Lean claim."),
 51: dict(t="CLAIM", v=M, d=["LeanCert2.frwzw_counts_k01"], hid="the frwzw_* matrices are script data; no theorem ties them to the FR-WZW constraints (DEF row, NAME-ONLY)", n="finranks k0p 1, k0m 0, k1p 2, k1m 0."),
 52: dict(t="CLAIM", v=M, d=["mod:LeanCertConv", "mod:JordConv", "mod:SurfConv"], n="8 equivalence theorems = LeanCertConv 2 + JordConv 3 + SurfConv 3."),
 53: dict(t="SCOPE", v=M, n="No k=2,3 declarations exist; accurate."),
 54: dict(t="META", n="Cited KITP statement."),
 93: dict(t="META"), 94: dict(t="META"),
 # ---- RG-IR-1
 55: dict(t="CLAIM", v=M, d=["mod:RgIr1"], n="7 theorems; pilot correction applied."),
 56: dict(t="CLAIM", v=M, d=["Alignment.RgIr1Sanity.claim_linearises", "Alignment.RgIr1Sanity.affine_time_map"], hid="k ≠ 0, y ≠ 0", n="Generic linear flow proved in the Alignment modules (pilot)."),
 57: dict(t="SCOPE", v=M), 95: dict(t="CLAIM", v=M, d=["Alignment.RgIr1Sanity.affine_time_map"]),
 # ---- CHIRAL-LATTICE-1
 58: dict(t="CLAIM", v=M, d=["mod:ChiralLat1"], n="4 theorems, as stated."),
 # ---- RP-TN-1
 59: dict(t="CLAIM", v=M, d=["RpTn1.hankel2_minor_nonneg", "RpTn1.toeplitz2_minor_neg"],
          hid="toeplitz2_minor_neg: w>0, x1≠x2, a,b≠0 (nonnegativity of nodes not needed); hankel2_minor_nonneg: w,x≥0", n="Lean is slightly more general than the prose on nodes; extra non-degeneracy hypotheses unstated."),
 96: dict(t="CLAIM", v=M, d=["mod:RpTn1"], n="8 theorems."),
 # ---- M3
 91: dict(t="CLAIM", v=M, d=["LECRatio.be14_central", "LECRatio.be14_fail", "LECRatio.be14_gap"], n="Lean proves > 3.8σ ((19/5)²σ² < gap²); prose 3.84σ is the SIM figure."),
 # ---- HG-DIM-1
 60: dict(t="CLAIM", v=M, d=["Alignment.HgDim1Sanity.claim_mean_conditional", "Alignment.HgDim1Sanity.mean_of_formula"], hid="given the per-edge formula (stated)"),
 61: dict(t="CLAIM", v=M, d=["HgDim1Mean.sumP_closed", "HgDim1Mean.mean_kappa_closed", "HgDim1Mean.enum_eq_sumP", "mod:HgDim1Mean9"]),
 62: dict(t="SCOPE", v=M, n="Accurate description of the earlier Lean (mean_kappa_instance numerals)."),
 63: dict(t="CLAIM", v=M, d=["Alignment.HgDim1Sanity.claim_mean_conditional", "Alignment.HgDim1Sanity.sign_change"]),
 97: dict(t="CLAIM", v=M, d=["Alignment.HgDim1Sanity.claim_mean_conditional"], n="Paper I card: same wording as II card (given the per-edge formula)."),
 98: dict(t="CLAIM", v=M, d=["HgDim1Mean.sumP_closed", "HgDim1Mean.enum_eq_sumP", "mod:HgDim1Mean9"]),
 99: dict(t="CLAIM", v=M, d=["Alignment.HgDim1Sanity.claim_mean_conditional"]),
 100: dict(t="SCOPE", v=M), 101: dict(t="SCOPE", v=M), 102: dict(t="SCOPE", v=M),
 124: dict(t="CLAIM", v=O, d=["HgDim1.edge_neg", "HgDim1.kappa_neg", "HgDim1.edge_pos", "HgDim1.kappa_pos"],
           hid="NA_neg/NB_neg/NA_pos/NB_pos are hand-listed and not proved to be the closed neighbourhoods under adj; kappa_* are arithmetic; Birkhoff/Kantorovich reduction on paper (C:572)",
           n="\\lean tag on the theorem reads as 'Ollivier curvature of two K7 edges checked'; Lean checks optimal-matching cost and a 1-Lipschitz potential gap between listed sets.",
           rw="\\lean{}\\,(two edges of $\\K_7$: optimal matching cost and matching potential gap between the listed closed neighbourhoods; the reduction to Ollivier curvature is on paper, \\cref{sec:lean})"),
 117: dict(t="CLAIM", rung="HG-DIM-1", v=O, d=["HgDim1.edge_neg", "HgDim1.edge_pos"], hid="as C:194",
           n="Contribution (I) carries the same \\lean tag.",
           rw="\\lean{}\\,(two $\\K_7$ edges: matching cost and potential gap; reduction on paper)"),
 125: dict(t="PAPER"), 126: dict(t="PAPER"), 128: dict(t="PAPER", n="classical"),
 127: dict(t="CLAIM", v=M, d=["HgDim1Mean.sumP_closed", "HgDim1Mean.enum_eq_sumP", "mod:HgDim1Mean9"]),
 129: dict(t="CLAIM", v=M, d=["HgDim1Mean.mean_kappa_closed", "HgDim1Mean.enum_eq_sumP"]),
 130: dict(t="CLAIM", v=M, d=["HgDim1Mean.enum_eq_sumP", "mod:HgDim1Mean9"]),
 131: dict(t="SCOPE", v=M),
 132: dict(t="CLAIM", v=M, d=["Alignment.HgDim1Sanity.claim_mean_conditional", "Alignment.HgDim1Sanity.sign_change"]),
 133: dict(t="SCOPE", v=M, n="Scope sentence accurate, but 'in Lean for two edges' inherits the C:194 caveat."),
 144: dict(t="META", n="\\computed result, no Lean claim."), 145: dict(t="SCOPE", v=M),
 118: dict(t="CLAIM", rung="HG-DIM-1", v=M, d=["HgDim1Mean.enum_eq_sumP", "mod:HgDim1Mean9"]),
 # ---- HG-DIM-2
 64: dict(t="CLAIM", v=M, d=["HgDim2.link", "HgDim2.kappa_of_cost", "mod:HgDim2P4", "mod:HgDim2P5", "mod:HgDim2P6"], hid="Birkhoff reduction cited (C:572); n=4,5,6 only in Lean"),
 103: dict(t="CLAIM", v=M, d=["mod:HgDim2P4", "mod:HgDim2P5", "mod:HgDim2P6"], n="Gap 0 every edge is SIM; Lean n=4,5,6."),
 136: dict(t="CLAIM", v=M, d=["mod:HgDim2P4", "mod:HgDim2P5", "mod:HgDim2P6"], hid="Birkhoff (C:572)"),
 146: dict(t="META", n="\\computed."), 147: dict(t="SCOPE", v=M),
 120: dict(t="CLAIM", rung="HG-DIM-2", v=M, d=["mod:HgDim2P4", "mod:HgDim2P5", "mod:HgDim2P6"]),
 # ---- CAPPED-FORMAN-1
 65: dict(t="CLAIM", v=M, d=["CappedForman.face_term_le", "CappedForman.face_term_max", "CappedForman.capped_ge_forman", "CappedForman.capped_eq_forman_iff"],
          hid="face lemmas need 3 ≤ k (faces have k ≥ 3); prose 'for all k' fine", n="8 thm / 4 def correct."),
 66: dict(t="CLAIM", v=M, d=["mod:CappedFormanCerts"], n="42 thm / 48 def correct."),
 67: dict(t="SCOPE", v=M), 104: dict(t="CLAIM", v=M, d=["mod:CappedForman", "mod:CappedFormanCerts"], n="50 theorems correct."),
 134: dict(t="PAPER"), 135: dict(t="PAPER"), 137: dict(t="META", n="\\computed."),
 138: dict(t="CLAIM", v=M, d=["CappedForman.face_term_max", "CappedForman.capped_eq_forman_iff"]),
 139: dict(t="SCOPE", v=M),
 140: dict(t="CLAIM", v=M, d=["CappedForman.face_term_le", "CappedForman.face_term_max", "CappedForman.capped_ge_forman", "CappedForman.capped_eq_forman_iff"], hid="3 ≤ k"),
 141: dict(t="CLAIM", v=M, d=["mod:CappedFormanCerts"]), 142: dict(t="SCOPE", v=M),
 119: dict(t="PAPER", rung="CAPPED-FORMAN-1"),
 # ---- CURV-LEAN (curvature paper Lean section)
 143: dict(t="META"),
 148: dict(t="CLAIM", v=M, n="Toolchain v4.34.1 and Mathlib d13f23b match lean/lean-toolchain and the manifest."),
 149: dict(t="CLAIM", v=M, d=["mod:HgDim1", "mod:HgDim1Mean", "mod:HgDim1Mean9", "mod:HgDim2", "mod:HgDim2P4", "mod:HgDim2P5", "mod:HgDim2P6", "mod:CappedForman", "mod:CappedFormanCerts"],
           n="Table counts match AxiomsAll (thm incl. equation lemmas): 185 thm / 160 def."),
 150: dict(t="SCOPE", v=M), 151: dict(t="SCOPE", v=M), 152: dict(t="SCOPE", v=M),
 # ---- GENERAL rows with a checkable claim
 1: dict(t="CLAIM", rung="GENERAL", v=O, n="Omits the paper-proved and conjecture tags that the paper uses (e.g. HG-DIM-1 \\PAPERPROVED).",
         rw="Every claim carries one status tag: proved in Lean, proved on paper, computed in a preregistered simulation with locked checkers and planted controls, cited, or conjectural."),
 72: dict(t="CLAIM", rung="GENERAL", v=O, n="Paper I abstract tag list omits paper-proved (\\PAPERPROVED, defined at I:47).",
          rw="Every claim carries one epistemic tag (Lean-proved, paper-proved, simulated, cited, conjecture, speculation)."),
 81: dict(t="CLAIM", rung="GENERAL", v=O, n="Counterexamples: MR-1b coefficient->coupling step, HG-DIM-1 general-n per-edge formula and CAPPED-FORMAN-1 general bound are on paper.",
          rw="Every lemma tagged \\PROVED{} is proved in Lean~4 on Mathlib; steps proved only on paper are tagged \\PAPERPROVED{}."),
 105: dict(t="CLAIM", rung="GENERAL", v=NO, d=["IntChamber.invariant_chamber_constant", "MassiveLS.positivity_forces_chiral", "Cascade1.em_n5_zero_iff"],
           n="'ratio families ... stay free (PROVED)' names no declaration; freedom is proved per rung only in some cases.",
           rw="... stay free under the positivity and integrality constraints we studied (\\PROVED{} where a rung names its Lean module, e.g.\\ \\texttt{IntChamber}, \\texttt{Cascade1}; otherwise \\SIM)."),
 16: dict(t="CLAIM", rung="GENERAL", v=M, d=["mod:Alignment"], n="113 thm / 39 def in PositiveGeometryEmergentSpaceTime.Alignment.*, outside library counts (verified)."),
 84: dict(t="CLAIM", rung="GENERAL", v=M, d=["mod:Alignment"], n="Same 113/39 count."),
 85: dict(t="CLAIM", rung="HG-DIM-1", v=M, d=["Alignment.HgDim1Sanity.claim_mean_conditional"]),
 86: dict(t="CLAIM", rung="RG-IR-1", v=M, d=["Alignment.RgIr1Sanity.affine_time_map"]),
 115: dict(t="CLAIM", rung="GENERAL", v=M, n="decide / ordinary proofs, no native_decide (C:552 audit)."),
 122: dict(t="CLAIM", rung="GENERAL", v=M), 157: dict(t="CLAIM", rung="GENERAL", v=M),
}
