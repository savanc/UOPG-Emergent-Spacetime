"""M2e: Lean certificates for the algebraic core of "the delta-shift is forced at n = 6".

After scripts/m2e_shift_scan.py:
 * 503 of the 511 non-empty supports die because some coefficient equation is a nonzero constant or a monomial
   in the b's (impossible for b != 0); re-checked by trivial_supports();
 * the 8 survivors all shift the six (e,e)/(o,o) chords, plus a subset of {X14, X25, X36}.
For those 8 the coefficient equations are rewritten in a = 1/b (numerator after b -> 1/a, monomial a-factors
stripped, legitimate as every a in the support is nonzero). A search finds a derivation (linear facts,
case splits on products of linear factors) and emits Lean, where every step is re-checked
(linear_combination / simp / rcases / linarith).
Output: lean/PositiveGeometryEmergentSpaceTime/ShiftForced.lean and scripts/m2e_certificates_summary.json."""
import itertools, json
import sympy as sp
_src = open('scripts/m2e_shift_scan.py').read()
exec(_src[:_src.index("if __name__ == '__main__':")])
A = {c: sp.Symbol(f'a{c[0]}{c[1]}') for c in CH}
OE = [(1,4),(2,5),(3,6)]
FB = [c for c in CH if c in FORB]
L = lambda e: str(e).replace('**', '^')

def trivial_supports():
    triv, rest = 0, []
    for r in range(1, 10):
        for S in itertools.combinations(CH, r):
            S = list(S); U, P, Pk, eqs = conditions(S, 4)
            E = [e for e in eqs if e != 0]
            if any(e.is_number or len(sp.Add.make_args(e)) == 1 for e in E): triv += 1
            else: rest.append(S)
    return triv, rest

def a_equations(S):
    U, P, Pk, eqs1 = conditions(S, 4, use_C3=False)
    U, P, Pk, eqsA = conditions(S, 4)
    c1 = {sp.expand(e) for e in eqs1 if e != 0}
    av = [A[c] for c in S]; sub = {B[c]: 1 / A[c] for c in S}
    out = {}
    for e in sorted({sp.expand(e) for e in eqsA if e != 0}, key=str):
        n = sp.expand(sp.numer(sp.together(e.subs(sub))))
        cst, fl = sp.factor_list(n)
        g = sp.expand(sp.Mul(*[q ** m for q, m in fl if not (q.is_Symbol and q in av)]))
        if g == 0: continue
        if g not in out or e in c1: out[g] = 'C1' if e in c1 else 'C3'
    return av, sorted(out.items(), key=lambda kv: (len(str(kv[0])), str(kv[0])))

def split_form(p, av):
    if p == 0: return None
    cst, fl = sp.factor_list(p)
    return [q for q, m in fl if not (q.is_Symbol and q in av)]

def subs_dict(subs):
    sd = {}
    for v, ex in subs:
        sd = {k: sp.expand(w.subs(v, ex)) for k, w in sd.items()}; sd[v] = sp.expand(ex.subs(sd))
    return sd

def Lcoeffs(S):
    """The X-coefficients of P_4 (the limit L, times the unshifted denominators), rewritten in a."""
    U, P = numerators(S, 4)
    av = [A[c] for c in S]; sub = {B[c]: 1 / A[c] for c in S}; out = []
    for cf in coeff_eqs(P[4]):
        n = sp.expand(sp.numer(sp.together(cf.subs(sub))))
        cst, fl = sp.factor_list(n)
        out.append(sp.expand(sp.Mul(*[q ** m for q, m in fl if not (q.is_Symbol and q in av)])))
    return out

def search(av, eqs, subs, goal):
    sd = subs_dict(subs)
    cur = lambda p: sp.expand(p.subs(sd, simultaneous=True)) if sd else p
    for v in av:
        if v in sd and sd[v] == 0: return ('zero', v)
    if goal is not None and all(cur(g) == 0 for g in goal): return ('goal',)
    cands = []
    for i, (p, o) in enumerate(eqs):
        q = cur(p); fs = split_form(q, av)
        if fs is None: continue
        if not fs: return ('mono', i)
        if all(sp.Poly(f, *av).total_degree() == 1 for f in fs):
            cands.append((len(fs), o != 'C1', i, fs))
    cands.sort(key=lambda x: (x[0], x[1]))
    for n, _, i, fs in cands:
        branches = []
        for f in fs:
            free = [v for v in reversed(av) if f.has(v)]
            v = free[0]; ex = sp.solve(f, v)[0]
            r = search(av, eqs, subs + [(v, ex)], goal)
            if r is None: break
            branches.append((v, ex, r))
        else:
            return ('derive', i, branches)
    return None

class Emit:
    def __init__(self, av, eqs, hzero):
        self.av, self.eqs, self.hzero, self.k, self.used = av, eqs, hzero, 0, set()
        self.goal = []
        self.simp = ', '.join(['mul_eq_zero', 'pow_eq_zero_iff', 'ne_eq', 'OfNat.ofNat_ne_zero', 'not_false_eq_true',
                               'false_or', 'or_false', 'or_assoc'] + list(hzero.values()))
    def combo(self, i, subs):
        """p_i minus sum q_k*(v_k - ex_k) equals p_i with all substitutions applied (sequentially)."""
        p = self.eqs[i][0]; terms = [f'e{i}']; self.used.add(i)
        for (v, ex, name) in subs:
            pn = sp.expand(p.subs(v, ex))
            q = sp.cancel((p - pn) / (v - ex))
            if q != 0: terms.append(f'- ({L(sp.expand(q))}) * {name}')
            p = pn
        return ' '.join(terms), p
    def tree(self, t, subs, ind):
        p = ' ' * ind
        if t[0] == 'zero': return f'{p}exact absurd (by linarith) {self.hzero[t[1]]}\n'
        if t[0] == 'goal':
            out = f'{p}refine ⟨{", ".join("?_" for _ in self.goal)}⟩\n' if len(self.goal) > 1 else ''
            for g in self.goal:
                terms = []; q0 = g
                for (v, ex, name) in subs:
                    pn = sp.expand(q0.subs(v, ex)); q = sp.cancel((q0 - pn) / (v - ex))
                    if q != 0: terms.append(f'({L(sp.expand(q))}) * {name}')
                    q0 = pn
                assert q0 == 0
                lc = ' + '.join(terms) if terms else '0'
                out += f'{p}{"· " if len(self.goal) > 1 else ""}linear_combination {lc}\n'
            return out
        cert, q = self.combo(t[1], subs); self.k += 1; d = f'd{self.k}'
        cst, fl = sp.factor_list(q)
        prod = ' * '.join(f'({L(f)})' + (f'^{m}' if m > 1 else '') for f, m in fl) or '1'
        s = f'{p}have {d} : {prod} = 0 := by linear_combination (1 / ({cst})) * ({cert})\n'
        if t[0] == 'mono':
            return s + f'{p}simp [{", ".join(self.hzero.values())}] at {d}\n'
        # Audit A-9: superset list; prune unused args after generation with scripts/lean_prune_simp.py
        s += f'{p}try simp only [{self.simp}] at {d}\n'
        br = t[2]
        if len(br) > 1: s += f'{p}rcases {d} with {" | ".join([d] * len(br))}\n'
        for (v, ex, sub) in br:
            self.k += 1; ln = f'l{self.k}'
            if len(br) > 1:
                s += f'{p}· have {ln} : {v} = {L(ex)} := by linarith\n' + self.tree(sub, subs + [(v, ex, ln)], ind + 2)
            else:
                s += f'{p}have {ln} : {v} = {L(ex)} := by linarith\n' + self.tree(sub, subs + [(v, ex, ln)], ind)
        return s

def full_support_block():
    """Full support: no unshifted denominators, so L = P_4 is a linear form in X (script). Lean proves that a
    linear form with the Adler zero on all six legs is identically zero. Generator: m2e_gen_full_support.py."""
    ns = {'sp': sp, 'softmap': softmap}
    exec(open('scripts/m2e_gen_full_support.py').read(), ns)
    return ns['BLOCK']

if __name__ == '__main__':
    triv, rest = trivial_supports()
    print('supports killed by a constant/monomial coefficient:', triv, '; survivors:', len(rest), flush=True)
    assert triv == 503 and all(set(FB) <= set(S) for S in rest)
    blocks, summary = [], []
    for r in range(4):
        for ex in itertools.combinations(OE, r):
            S = sorted(FB + list(ex), key=CH.index)
            av, eqs = a_equations(S)
            full = len(ex) == 3
            if full:
                U, P = numerators(S, 4); assert not U and sp.Poly(P[4], *XS).total_degree() == 1
                assert set(map(sp.expand, Lcoeffs(S))) <= {sp.expand(p) for p, o in a_equations(S)[1]} | {sp.expand(-p) for p, o in a_equations(S)[1]}
                blocks.append(full_support_block())
                summary.append({'support': [f'{c[0]}{c[1]}' for c in S], 'theorem': 'full_support_L_vanishes', 'equations_used': 0, 'from': ['C3 (all six legs)']})
                print('full_support_L_vanishes: linear L with Adler zero on all six legs vanishes', flush=True)
                continue
            if full: goal = Lcoeffs(S)
            else: goal = None if ex else [sp.expand(A[c] - (A[(1,3)] if c in [(1,5),(3,5)] else -A[(1,3)])) for c in S if c != (1,3)]
            tree = search(av, eqs, [], goal)
            assert tree is not None, ex
            hzero = {v: f'h{str(v)[1:]}' for v in av}
            em = Emit(av, eqs, hzero); em.goal = goal or []; body = em.tree(tree, [], 2)
            ids = sorted(em.used)
            hyps = ' '.join(f'({hzero[v]} : {v} ≠ 0)' for v in av)
            ehyps = '\n    '.join(f'(e{i} : {L(eqs[i][0])} = 0)  -- from {eqs[i][1]}' for i in ids)
            origins = sorted({eqs[i][1] for i in ids})
            if full:
                name = 'full_support_L_vanishes'
                concl = ' ∧ '.join(f'{L(g)} = 0' for g in goal)
            elif ex:
                name = 'no_solution_' + '_'.join(f'{c[0]}{c[1]}' for c in ex); concl = 'False'
            else:
                name = 'forced_main'
                concl = ' ∧ '.join(f'{A[c]} = {"" if c in [(1,5),(3,5)] else "-"}a13' for c in S if c != (1,3))
            doc = (f'Support: the six (e,e)/(o,o) chords' + (' + ' + ', '.join(f'X{c[0]}{c[1]}' for c in ex) if ex else '') + '.' +
                   (' The conclusion: every X-coefficient of the limit L (in a) vanishes, so L ≡ 0 and the nonzero clause of C1 fails.' if full else '') + f' Hypotheses: {len(ids)} script-derived coefficient equations (in a = 1/b), from {"+".join(origins)}.')
            blocks.append(f'/-- {doc} -/\ntheorem {name} {{{" ".join(map(str, av))} : ℝ}} {hyps}\n    {ehyps}\n    : {concl} := by\n{body}')
            summary.append({'support': [f'{c[0]}{c[1]}' for c in S], 'theorem': name, 'equations_used': len(ids), 'from': origins})
            print(name, 'uses', len(ids), 'equations from', origins, flush=True)
    hdr = open('scripts/m2e_lean_header.txt').read()
    open('lean/PositiveGeometryEmergentSpaceTime/ShiftForced.lean', 'w').write(hdr + '\n\n'.join(blocks) + '\n\nend PositiveGeometryEmergentSpaceTime.ShiftForced\n')
    json.dump({'trivially_killed': triv, 'survivors': [[f'{c[0]}{c[1]}' for c in S] for S in rest], 'lean': summary},
              open('scripts/m2e_certificates_summary.json', 'w'), indent=1)
