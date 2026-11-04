#!/usr/bin/env python3
"""SC-1 locked checker. Extracts ONLY the large-N value of m_rho/sqrt(sigma) from a LaTeX source dir,
then scores vs sqrt(pi) with rivals and a null rate. Never prints source text.
Usage: sc1_score.py presence <dir>...   (counts only)
       sc1_score.py live <dirA> <dirB>   (extract + score)"""
import sys, re, glob, math, itertools
RATIO = re.compile(r'm_\{?\\rho\}?\s*/\s*\\sqrt\{?\\sigma\}?')
NUM = re.compile(r'=\s*\$?\s*(\d\.\d+)\s*(?:\((\d+)\))?')
INF = re.compile(r'\\infty|large[- ]?\$?N|N\s*\\to\s*\\infty')
def segments(d):
    txt = ''
    for f in sorted(glob.glob(f'{d}/**/*.tex', recursive=True)):
        txt += '\n' + re.sub(r'(?<!\\)%.*', '', open(f, errors='ignore').read())
    return re.split(r'\\\\|\n\s*\n|(?<=[.;])\s+(?=[A-Z\\])', txt)
def cands(d):
    out = []
    for s in segments(d):
        m = RATIO.search(s)
        if not m or not INF.search(s): continue
        n = NUM.search(s, m.end(), m.end() + 60)
        if n:
            v = float(n.group(1)); dec = len(n.group(1).split('.')[1])
            e = int(n.group(2)) * 10**-dec if n.group(2) else None
            out.append((v, e))
    return out
CELLS = {  # pre-registered exact cells: (table label, row-label regex, column index, caption-systematic?)
    '1304.4437': ('tab:largeNsummary', r'^\$\\rho\$$', 2, True),
    '2011.13061': ('t:finaltable', r'^\$\\frac\{m_X\^\{\(0\)\}\}\{\\sqrt\{\\sigma\}\}\$$', 1, False),
}
VAL = re.compile(r'^\$?\s*(\d+\.\d+)((?:\s*\(\d+\))*)\s*\$?$')
def table_cell(d, key):
    lab, rowre, col, syst = CELLS[key]
    txt = ''.join(re.sub(r'(?<!\\)%.*', '', open(f, errors='ignore').read()) for f in sorted(glob.glob(f'{d}/**/*.tex', recursive=True)))
    tabs = [b for b in re.findall(r'\\begin\{table\}(.*?)\\end\{table\}', txt, re.S) if '\\label{' + lab + '}' in b]
    if len(tabs) != 1: raise ValueError(f"{key}: table {lab} found {len(tabs)}x")
    rows = [r for r in re.split(r'\\\\', tabs[0]) if '&' in r]
    hits = []
    for r in rows:
        cells = [c.strip() for c in re.sub(r'\\hline|\\cline\{[^}]*\}', '', r).split('&')]
        if re.match(rowre, cells[0]): hits.append(cells)
    if len(hits) != 1: raise ValueError(f"{key}: row matched {len(hits)}x")
    cell = hits[0][col]
    pm = re.search(r'\\begin\{pmatrix\}\s*\+\s*(\d+)\s*\\cr\s*-\s*(\d+)\s*\\end\{pmatrix\}', cell)
    cell_main = re.sub(r'\\begin\{pmatrix\}.*?\\end\{pmatrix\}', '', cell)
    m = VAL.match(cell_main.strip())
    if not m: raise ValueError(f"{key}: cell not numeric")
    v = float(m.group(1)); dec = len(m.group(1).split('.')[1])
    errs = [int(e) * 10**-dec for e in re.findall(r'\((\d+)\)', m.group(2))]
    if pm: errs.append(max(int(pm.group(1)), int(pm.group(2))) * 10**-dec)   # asymmetric sys: take the larger
    stat = math.sqrt(sum(e*e for e in errs))
    sys_pct = 0.0
    if syst:
        sm = re.search(r'systematic\s+error\s+of\s*(\d+)\\%', tabs[0])
        if not sm: raise ValueError(f"{key}: caption systematic missing")
        sys_pct = float(sm.group(1))
    return v, math.sqrt(stat**2 + (sys_pct/100*v)**2)
def extract(d):
    key = d.rstrip('/').split('/')[-1]
    if key in CELLS: return table_cell(d, key)
    c = cands(d); vals = sorted({v for v, _ in c})
    if not vals: raise ValueError(f"{d}: NO CELL")
    if max(vals) - min(vals) > 0.01 * min(vals): raise ValueError(f"{d}: AMBIGUOUS ({len(vals)} distinct values)")
    v = vals[0]; errs = [e for vv, e in c if vv == v and e is not None]
    return v, (max(errs) if errs else 0.0)
TARGET = math.sqrt(math.pi)
RIVALS = {'sqrt(2pi) [alpha\'=1/m^2]': math.sqrt(2*math.pi), 'sqrt(pi/2) [closed-string slope]': math.sqrt(math.pi/2)}
BASIS = sorted({math.sqrt(p/q*math.pi**k) for p in range(1,7) for q in range(1,7) for k in (0,1,2)})
BASIS = [b for b in BASIS if 1 <= b <= 3]
def tol(e): return max(3*e, 0.05*TARGET)
if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'presence':   # prints only whether each pre-registered cell parses as a number
        for d in sys.argv[2:]:
            try: extract(d); print(f"{d}: cell numeric = True")
            except ValueError as ex: print(f"{d}: cell numeric = False ({ex})")
        sys.exit(0)
    res = {}
    for d in sys.argv[2:4]:
        try: res[d] = extract(d)
        except ValueError as ex: print("REJECT:", ex); res[d] = None
    if any(v is None for v in res.values()): print("VERDICT: UNCLASSIFIED (extraction)"); sys.exit(2)
    inside = []
    for d, (v, e) in res.items():
        t = tol(e); dT = abs(v - TARGET); dR = {k: abs(v - r) for k, r in RIVALS.items()}
        null = sum(abs(b - v) <= dT for b in BASIS) / len(BASIS)   # look-elsewhere: basis constants at least as close as sqrt(pi)
        ok = dT <= t; beats = all(dT < x for x in dR.values())
        inside.append((ok, beats, null))
        print(f"{d}: value={v} err={e} tol={t:.4f} |v-sqrt(pi)|={dT:.4f} within={ok} rivals={ {k: round(x,4) for k,x in dR.items()} } beats_rivals={beats} null_rate={null:.3f} (basis n={len(BASIS)})")
    nin = sum(o for o, _, _ in inside)
    if nin == 2 and all(b and n < 0.2 for _, b, n in inside): verdict = 'PASS'
    elif nin == 0: verdict = 'FAIL'
    elif nin >= 1: verdict = 'PARTIAL'
    else: verdict = 'UNCLASSIFIED'
    print("VERDICT:", verdict)
