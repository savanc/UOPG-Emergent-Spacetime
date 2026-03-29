# UOPG-Emergent-Spacetime
UOPG: Emergent Spacetime and Particles from the Positive Grassmannian  A geometric bootstrap model where positivity-preserving Plücker mutations on Gr+(k,n) generate an emergent curved metric projecting to 3+1D Lorentzian spacetime. Wave interference produces particles, entanglement, annihilation, and chiral asymmetry. Calibrated to the LHC W-boson

# UOPG: Emergent Spacetime and Particles from the Positive Grassmannian

**A Geometric Model Calibrated to LHC W-Boson Mass**

- **Paper**: [article.pdf](https://doi.org/10.5281/zenodo.19291218))
- **Zenodo DOI**: [10.5281/zenodo.19291218](https://doi.org/10.5281/zenodo.19291218)
- **Lean 4 formalisation**: [UOPG.lean](UOPG.lean)
- **Numerical notebook**: [UOPG_Notebook.ipynb](UOPG.ipynb)

## Abstract
We present a geometric model in which the positive Grassmannian Gr+(k,n) serves as the single underlying structure. Positivity-preserving mutations generate curvature that projects to 3+1D Lorentzian spacetime. Wave interference on the emergent metric produces particles, entanglement, annihilation, and chiral asymmetry. The model is calibrated so the W-boson mass is exactly 80.4 GeV.

## Files
- `Article.pdf` – Full preprint
- `UOPG.lean` – Complete Lean 4 formalization of every mathematical claim
- `UOPG.ipynb` – Executable SymPy notebook (harmonic emergence, emergent metric, mutations, wave interference, Monte-Carlo calibration to 80.4 GeV)

## How to run
```bash
# Lean 4
lake exe UOPG          # prints calibrated W-boson mass

# Jupyter notebook
jupyter notebook UOPG_Notebook.ipynb
