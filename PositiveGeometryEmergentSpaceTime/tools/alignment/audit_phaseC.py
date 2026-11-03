"""Phase C axiom audit: one `#print axioms` file per Phase C Sanity module (each run separately under the
memory guard). Writes lean/AlignmentPhaseCAxioms/<Mod>.lean; prints the module list.
Also greps the sources for `sorry`, `native_decide`, `axiom`, `admit`."""
import re, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]; S = ROOT / 'lean/PositiveGeometryEmergentSpaceTime/Alignment/Sanity'
MODS = ['LeanCert2K23', 'Jord1Bridge', 'Jord1JordanCheck', 'Jord1Jordan', 'Jord1DerData', 'Jord1DerPeel',
        'Jord1DerB0', 'Jord1DerB1', 'Jord1DerB2', 'Jord1DerB3', 'Jord1Der', 'IsingGPSign', 'Surf1K33Split',
        'Surf1K33Fast'] + [f'Surf1K33P{i}' for i in range(8)] + ['Surf1K33']
OUT = ROOT / 'lean/AlignmentPhaseCAxioms'; OUT.mkdir(exist_ok=True)
bad = []; tot = 0
for m in MODS:
    src = (S / f'{m}.lean').read_text()
    code = re.sub(r'/-.*?-/', '', src, flags=re.S); code = re.sub(r'--.*', '', code)
    for w in ['sorry', 'native_decide', 'admit']:
        if re.search(rf'\b{w}\b', code): bad.append((m, w))
    if re.search(r'^\s*axiom\b', code, re.M): bad.append((m, 'axiom'))
    ns = re.search(r'^namespace (\S+)', src, re.M).group(1)
    names = re.findall(r'^(?:private )?(?:theorem|lemma) (\S+)', code, re.M); tot += len(names)
    (OUT / f'{m}.lean').write_text(f'import PositiveGeometryEmergentSpaceTime.Alignment.Sanity.{m}\n' +
        ''.join(f'#print axioms {ns}.{n}\n' for n in names))
    print(m, len(names))
print('TOTAL', tot, 'BAD', bad)
