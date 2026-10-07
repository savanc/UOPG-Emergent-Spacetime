# UOPG-Emergent-Spacetime
UOPG: Emergent Spacetime and Particles from the Positive Grassmannian  A geometric bootstrap model where positivity-preserving Plücker mutations on Gr+(k,n) generate an emergent curved metric projecting to 3+1D Lorentzian spacetime. Wave interference produces particles, entanglement, annihilation, and chiral asymmetry. Calibrated to the LHC W-boson

# UOPG: Emergent Spacetime and Particles from the Positive Grassmannian

**A Geometric Model Calibrated to LHC W-Boson Mass**

## Status

The mission is unchanged: spacetime and particles come from one positive Grassmannian, and the Standard Model is a geometric bootstrap from that field. The first checked piece is [MVP-0](mvp0/README.md). It proves the Klein dictionary for `Gr⁺(2,4)`: the Plücker relation, the real `GL(2)` weight, one positive rational point, null separation, and four massless conserved edge momenta. The only experimental comparison is the PDG photon-mass bound, with no fitted scale. See [mvp0/DICTIONARY.md](mvp0/DICTIONARY.md).

`UOPG.lean` and `UOPGv2.lean` are drafts from March and April 2026. They are not kernel-checked proofs. `m_W = 80.4 GeV` is not a theorem of this repository.

- **Paper**: [article.pdf](https://doi.org/10.5281/zenodo.19291218)
- **Zenodo DOI**: [10.5281/zenodo.19291218](https://doi.org/10.5281/zenodo.19291218)
- **MVP-0 (proved)**: [mvp0/README.md](mvp0/README.md)
- **Lean 4 formalisation (draft concept)**: [UOPGv2.lean](UOPGv2.lean)
- **Numerical notebook**: [uopgv2.ipynb](uopgv2.ipynb)
- **Slide Deck**: [UOPG v2 Slide deck](https://github.com/savanc/UOPG-Emergent-Spacetime/blob/main/Unified_Positive_Geometry.pdf)
  
## Abstract
We present a geometric model in which the positive Grassmannian Gr+(k,n) serves as the single underlying structure. Positivity-preserving mutations generate curvature that projects to 3+1D Lorentzian spacetime. Wave interference on the emergent metric produces particles, entanglement, annihilation, and chiral asymmetry. The model is calibrated so the W-boson mass is exactly 80.4 GeV.

## Files
- `mvp0/` – Kernel-checked Klein dictionary. Start here.
- `Article.pdf` – Full preprint
- `UOPG.lean` – Draft Lean 4 sketch. Not a proof.
- `UOPG.ipynb` – Executable SymPy notebook (harmonic emergence, emergent metric, mutations, wave interference, Monte-Carlo calibration to 80.4 GeV)

## How to run
```bash
# MVP-0, the part that is actually proved
cd mvp0/lean
lake exe cache get
lake build
lake exe uopg0

# Historical draft sketches (not proofs)
# UOPG.lean and UOPGv2.lean do not form a Lake project.
```
