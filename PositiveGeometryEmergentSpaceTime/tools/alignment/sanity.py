"""Phase B (2026-11-03): add the `sanity` column to notes/alignment/blueprint.tsv and re-point claim rows to the
current paper lines (II v8 / I v9 / C v4).

Run after build.py and recheck_v8.py (both rewrite the TSV). Idempotent.
* Line re-pointing: build.py searches each v7 claim tail within +40 lines of its v7 line; rows whose tail is no
  longer on the reported line are re-pointed via out/claims_v8.json (the v8 claim whose v7_match.index is the row),
  using whitespace-normalised search of the v8 tail. Rows still not found keep their line and are listed.
* Sanity column: verdicts of the Lean modules in lean/PositiveGeometryEmergentSpaceTime/Alignment/Sanity (see SANITY-2026-11-03.md, Phase C addendum SANITY-2026-11-03b.md).
"""
import json, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import glossary_terms
ROOT = pathlib.Path(__file__).resolve().parents[2]; OUT = ROOT / "tools/alignment/out"; NOTES = ROOT / "notes/alignment"
PL = {k: (ROOT / p).read_text().splitlines() for k, p in glossary_terms.PAPERS.items()}
C7 = json.load(open(OUT / "claims.json"))["claims"]
C8 = json.load(open(OUT / "claims_v8.json"))["claims"]
S = "Alignment.Sanity."
MOD = {"MR-1b": "LSConvention", "SURF-1′": "Surf1Ties", "JORD-1": "Jord1Sanity", "HG-DIM-1": "HgDim1Nbhd",
       "H-T5": "IsingStar", "FL-1Z": "FL1ZSanity", "EW-Z1b": "EWZ1bSanity", "LEAN-CERT-2": "LeanCert2Sanity",
       "RP-TN-1": "RpTn1Sanity"}  # Phase C modules: see SANITY-2026-11-03b.md
ROW = {
 "7": "MR-1b sign wording: extraction PROVED (LSConvention.rho3_coeff, f4_coeff, rho3_ratio_derived); c_J=-g^2m^2 applied literally gives g_rho^2=-1/2, so 5/16 and 49/240 are ratios of magnitudes (signed: -5/16, -49/240). Correction g_J^2=|c_J|/m^2 applied in II v8.1 and I v9.1 (glossary)",
 "19": "as row 7: PROVED extraction + gsq_values/ratios; finding = ratios are of |c_J|/m^2 (wording; numbers unchanged); corrected in II v8.1",
 "D161": "PROVED tie: IsingStar.C_eq_gpRule, C_cast_eq_gpY (C = GP matrix of the star Ising network at t=(1/2,1/3,1/4)); Phase C: IsingGPSign.pos_unique, gp_eq (n=3 sign rule recovered by exhaustion: unique positive pattern of 64); general-n sign rule still transcribed",
 "D165": "sanity PROVED (finite checks): Jord1Sanity.E1_idem, E1_peirce, unit_ok, jordan_basis, jordan_mixed; gsm_nontrivial, gsm_sub_stab. Phase C PROVED: Jord1Jordan.jordan (full Jordan identity on Q^27) and Jord1Der.finrank_der (dim_Q Der = 52, kernel). Iso Der ≅ f4 itself not in Lean",
 "D166": "sanity PROVED: Jord1Sanity.stab_empty (stab ∅ = Der), gsm_sub_stab",
 "D169": "PROVED tie: FL1ZSanity.mnu_eq_D3 (D3 = model mass matrix f M* g M† fᵀ at τ=ω, up to 2s²/9·b0²·bm·(ae−b0(be+ce))²)",
 "D170": "SIMULATED (independent): sims/ewz1b_indep 5D index-sum Feynman-rule derivation agrees with Lean EWZ1b.N 200/200 exact, controls fail (run EWZ1B-INDEP-2026-11-03-r1); Lean-side Feynman-rule tie open. Lean sanity: EWZ1bSanity",
 "D173": "PROVED tie k=0: LeanCert2Sanity.eps_cyc, eps_rev, eps_par, k0p_rows_zero, k0m_rows_pattern; k=2,3 formal dims PROVED: LeanCert2K23.k2p/k2m/k3p/k3m_finrank = 5/0/10/2, *_N_rows (rows vanish symbolically); sampled checks remain SIMULATED",
 "D174": "PROVED tie: Surf1Ties.boxU_eq_K33 (boxU ≅ completeBipartiteGraph 3 3); Phase C PROVED (kernel): Surf1Sanity.coeffs_K33, claimEnumerated (colour vector, 64 orientations x 4 blocks; SIMULATED hypothesis discharged)",
 "D175": "PROVED tie: Surf1Ties.ttU_vEdges, ttU_mult (ttU = double square)",
 "D177": "PROVED tie: HgDim1Nbhd.NA_neg_tie, NB_neg_tie, NA_pos_tie, NB_pos_tie (lists = computed closed flip neighbourhoods); tris_complete (42 = C5)",
 "D184": "PROVED tie: RpTn1Sanity.gram_form, gram_nonneg (RP for every finite family)",
}
def nrm(s): return re.sub(r"\s+", " ", s).strip()
def on_line(p, ln, text):
    L = PL[p]; t = text.strip()[-40:]
    return 0 < ln <= len(L) and t in L[ln - 1]
def find(p, text):
    L = PL[p]; t = nrm(text)[-50:]
    for i in range(len(L)):
        if t in nrm(" ".join(L[i:i + 6])):
            for j in range(i + 5, i - 1, -1):  # last line where the tail ends
                if nrm(t)[-15:] in nrm(" ".join(L[i:j + 1])) and nrm(t)[-15:] not in nrm(" ".join(L[i:j])): return j + 1
            return i + 1
    return None
tsv = NOTES / "blueprint.tsv"
L = tsv.read_text().splitlines(); h = L[0].split("\t")
if "sanity" in h:
    k = h.index("sanity"); L = ["\t".join(x for j, x in enumerate(l.split("\t")) if j != k) for l in L]; h = L[0].split("\t")
out = [L[0] + "\tsanity"]; moved, lost = [], []
for l in L[1:]:
    r = l.split("\t"); rid = r[0]
    if not rid.startswith("D"):
        p, ln = r[2].split(":"); c7 = C7[int(rid)]
        if not on_line(p, int(ln), c7["text"]):
            cand = sorted((c for c in C8 if c["v7_match"]["index"] == int(rid)), key=lambda c: -c["v7_match"]["ratio"])
            new = find(p, cand[0]["text"]) if cand else None
            new = new or find(p, c7["text"])
            if new and new != int(ln): moved.append((rid, r[2], f"{p}:{new}")); r[2] = f"{p}:{new}"
            elif not new: lost.append((rid, r[2]))
    s = ROW.get(rid) or (f"rung sanity: {MOD[r[1]]} (no row-specific tie)" if r[1] in MOD else "")
    out.append("\t".join(r) + "\t" + s)
tsv.write_text("\n".join(out) + "\n")
print("moved", len(moved), moved); print("not found (line kept)", lost)
