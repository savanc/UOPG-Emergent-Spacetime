#!/usr/bin/env python3
"""SC-3 step 0 locked checker (read-only). Decides whether a Lean amplitude file contains a Higgs
self-quartic coupling that SC-3's 'lambda(mu*) = g^2' could refer to.
Cells read: (A) the module docstring sentence(s) naming coupling `lam4`; (B) the argument list of `def N`.
Usage: sc3_step0_check.py <lean_file>"""
import re, sys
src = open(sys.argv[1]).read()
m = re.search(r'def N \(([^:]*):', src)
if not m:
    raise SystemExit("REJECT: no `def N (...)` found - cells absent")
args = m.group(1).split()
doc = re.search(r'/-!(.*?)-/', src, re.S)
doc = doc.group(1) if doc else ''
sent = [s.strip() for s in re.split(r'(?<=[.;])\s', doc) if '`lam4`' in s]
if 'lam4' not in args or not sent:
    raise SystemExit("REJECT: coupling lam4 missing from N args or docstring - cells absent")
print("cell A (lam4 docstring):", ' | '.join(sent))
print("cell B (N args):", ' '.join(args))
lam4_txt = ' '.join(sent).lower()
lam4_is_higgs = bool(re.search(r'lam4`?\s*\((?:higgs|scalar|hhhh|h\^?4)', lam4_txt)) or 'higgs quartic' in lam4_txt
lam4_is_gauge = bool(re.search(r'lam4`?\s*\((?:vvvv|wwww|4-gauge|quartic gauge)', lam4_txt))
other_higgs = [a for a in args if re.fullmatch(r'(lam|lamH|lambda|lh|lamh|lam_h)', a)]
print(f"lam4_is_higgs_quartic={lam4_is_higgs} lam4_is_gauge_contact={lam4_is_gauge} other_higgs_quartic_args={other_higgs}")
if lam4_is_higgs or other_higgs:
    print("VERDICT: WELL-POSED")
elif lam4_is_gauge and not other_higgs:
    print("VERDICT: NOT-WELL-POSED")
else:
    print("VERDICT: UNCLASSIFIED")
