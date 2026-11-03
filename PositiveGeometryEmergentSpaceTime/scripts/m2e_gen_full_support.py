# Lean block for the full-support case (exec'd by m2e_certificates.py, which supplies sp and softmap).
order=['X13','X14','X15','X24','X25','X26','X35','X36','X46']
cs=['c'+n[1:] for n in order]
lines=[]
lines.append('''/-- Full support (all nine chords shifted). There are no unshifted denominators, so the would-be limit
L is a linear form Σ c_f X_f (its coefficients c_f are polynomials in a; script). If L has the Adler zero on all
six legs, then L ≡ 0, and the nonzero clause of C1(4) fails. This needs no input about a. -/
def Llin (c13 c14 c15 c24 c25 c26 c35 c36 c46 X13 X14 X15 X24 X25 X26 X35 X36 X46 : ℝ) : ℝ :=
  c13*X13 + c14*X14 + c15*X15 + c24*X24 + c25*X25 + c26*X26 + c35*X35 + c36*X36 + c46*X46
''')
hyps=[];specs=[]
for i in range(1,7):
    sm=softmap(i); args=[str(sm.get(sp.Symbol(n),sp.Symbol(n))) for n in order]
    free=sorted({str(s) for a in args for s in sp.sympify(a).free_symbols},key=order.index)
    hyps.append(f'(h{i} : ∀ {" ".join(free)} : ℝ, Llin {" ".join(cs)} {" ".join("("+a+")" for a in args)} = 0)')
    for v in free:
        vals=' '.join('1' if w==v else '0' for w in free)
        specs.append(f'  have := h{i} {vals}')
lines.append(f'''theorem full_support_L_vanishes {{{" ".join(cs)} : ℝ}}
    {chr(10).join("    "+h if k else h for k,h in enumerate(hyps))} :
    {" ∧ ".join(c+" = 0" for c in cs)} := by
  simp only [Llin] at *
{chr(10).join(specs)}
  norm_num at *
  refine ⟨{", ".join("?_" for _ in cs)}⟩ <;> linarith''')
BLOCK = '\n'.join(lines)
