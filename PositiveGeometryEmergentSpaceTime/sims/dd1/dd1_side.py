# UNSCORED side note (not a prereg cell): rho_Lambda^{1/4} ~ 2.3e-3 eV is a MEMORISED input, flagged.
hbar_c=1.97327e-7  # eV*m (CODATA, memorised)
E=2.3e-3
L=hbar_c/E; print(f"Lambda^-1/4 length = {L*1e6:.1f} um; implied prefactor for l=1e-6 m: {1e-6/L:.3g}; bound 38.6 um")
