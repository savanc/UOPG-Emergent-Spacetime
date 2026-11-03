#!/usr/bin/env python3
"""Build the PositiveGeometryEmergentSpaceTime theorem graph (2026-10-13).
Input : graph/raw_decls.jsonl  (from `cd lean && lake env lean GraphExport.lean`)
Output: graph/theorems.json, graph/edges.csv, graph/hub_edges.csv, graph/theorem-graph.graphml,
        graph/analysis.json, graph/theorem-graph.html, figures/theorem-graph-2026-10-13.png
Overlay facts are keyword-extracted from reviews/notes and carry a source file:line; they are
[EXTRACTED, UNCERTAIN] unless they come from the audit table or MISSION.md tally line.
"""
import json, re, csv, collections, pathlib, html
import networkx as nx, sys
R = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'scripts'))
from primary_rung import primary_rungs, mentions, RUNG_RE
ACCEPT = '--accept-primary-changes' in sys.argv  # regression gate below: refuse to change an existing primary_rung without this flag
decls = [json.loads(l) for l in open(R/'graph/raw_decls.jsonl')]
decls = [d for d in decls if d['kind'] in ('thm', 'def')]
byname = {d['name']: d for d in decls}
# Module key = path below `PositiveGeometryEmergentSpaceTime.` (nested modules keep their full path, e.g. `LeanCert2.Core`).
mod = lambda d: d['module'].split('.', 1)[1] if '.' in d['module'] else d['module']

# ---- curated stage map (CURATED by hand from module headers; see notes) ----
STAGE = {
 'S0 kinematics/spinors': 'Spinor Null LightCone Lorentz Klein SliceBridge FlagRelation MassiveSpinor BR6',
 'S1 positive geometry/networks': 'Associahedron IntChamber BridgePLAssoc BridgePLCharge GradedPositroid PositroidCells Network MarkovTrace IsingOG IsingLoop IsingTiling IsingTiling8 IsingTiling10 TP1a TP1b TP1bMatrix Hankel BR3',
 'S2 hidden zeros (NLSM/ChPT)': 'NLSM MassShift ShiftForced ShiftForcedConverse LECRatio Coon SplitZeroGate FT2Mesh DecayZeroNoGo FT5aL COS1 COS1b COS1d BR2 Cascade1 Cascade1b Cascade1bR2',
 'S3 dual/LS resonance amplitudes': 'Legendre LSResidue MassiveLS ThresholdLS UnitarisedLS UnequalLS KLPhi Dispersion PionBound BR1',
 'S4 hadron observable gates': 'HadronKinematics MassiveZero MassiveZeroOneLoop MassiveZeroSU3 MassiveZeroSU3Phys PiKZero SubthresholdGate EtaGate KEtaGate LatticeGate PiNGate PiNSubGate FT3Gate FT4Gate GB1a CoulombZero PauliZero FermionBridge',
 'S5 electroweak': 'EWZ1b BR5p',
 'S6 scale': 'ScaleNoGo OrderParameter SG1 SG1b BR4 PG1 SC2 SC2b SC1 FCoulomb FDim FDimMass FScatLen FRhoWidth FDeltaNLSM',
 'S7 gravity/entropy': 'RelEntropy KerrMinimal',
 'S8 SM structure': 'FL1Z STRUCT1 STRUCT1b STRUCT2 X6 STRUCT3 Separation FRMU R4Indep STRUCTNGen FRWZW TrialityWhy Jord1 Surf1 JordConv SurfConv',
 'audit': 'AuditWitnesses LeanCert LeanCert2 LeanCertConv'}
stage_of = {m: s for s, ms in STAGE.items() for m in ms.split()}
# Nested modules (A.B) inherit the stage of their top-level module A; any other unregistered module is an error.
for _M in sorted({mod(d) for d in decls}):
    if _M not in stage_of and _M.split('.')[0] in stage_of: stage_of[_M] = stage_of[_M.split('.')[0]]
_unstaged = sorted({mod(d) for d in decls} - set(stage_of))
if _unstaged: sys.exit('theorem_graph: modules with no STAGE entry: %s' % _unstaged)
STAGE_MODS = {s: [x for m in ms.split() for x in [m] + sorted(k for k in stage_of if k.startswith(m + '.'))] for s, ms in STAGE.items()}

# ---- triviality ----
src_cache = {}
def src(d):
    p = R/'lean'/(d['module'].replace('.', '/') + '.lean')
    if p not in src_cache: src_cache[p] = p.read_text().splitlines()
    return '\n'.join(src_cache[p][d['line']-1:d['end_line']])
_T = r'(rfl|decide|norm_num|trivial|simp|exact rfl|ring|ring_nf|omega|positivity|push_cast|simpa|norm_num \[[^\]]*\]|simp \[[^\]]*\]|simpa \[[^\]]*\])'
TRIV = re.compile(r':=\s*(by\s+)?%s(\s*;\s*%s)*\s*$' % (_T, _T), re.S)
A8 = {'lo_zero_at_P', 'g1_poly_vanishes', 'g1_poly_at_11', 'lo_zero_on_line', 'iam_degenerate', 'swave_slope_shifted',
      'eigenvalue_coxeter', 'modelA_intercept', 'threshold_dot_same'}  # notes/LEAN-AUDIT-2026-10-13.md row A-8
for d in decls:
    s = src(d)
    body = s.split(':=', 1)[1] if ':=' in s else ''
    one = len([l for l in body.strip().splitlines() if l.strip()]) <= 1
    d['proof_source_lines'] = s.count('\n') + 1
    h = one and bool(TRIV.search(s.strip()))
    a8 = d['name'].split('.')[-1] in A8
    d['trivial'] = d['kind'] == 'thm' and (h or d['value_size'] <= 20 or a8)
    d['trivial_reason'] = ('one-line closing tactic' if h else 'proof term <=20 nodes' if d['value_size'] <= 20 else 'audit A-8 list') if d['trivial'] else ''
    d['stage'] = stage_of.get(mod(d), 'unassigned')

# ---- edges ----
G = nx.DiGraph()
for d in decls: G.add_node(d['name'])
int_edges, ext_count, ext_edges = [], collections.Counter(), []
for d in decls:
    for part in ('type_uses', 'value_uses'):
        for u in d[part]:
            if u['n'] in byname and u['n'] != d['name']:
                int_edges.append((d['name'], u['n'], part[:-5]))
                G.add_edge(d['name'], u['n'])
            elif u['m'].startswith(('Mathlib', 'Physlib', 'PhysLean')):
                ext_edges.append((d['name'], u['n'], u['m'], part[:-5]))
ext_users = collections.defaultdict(set)
for a, b, m, _ in ext_edges: ext_users[(b, m)].add(a)
HUBINFRA = re.compile(r'(^inst|\.inst|Inst|\.to[A-Z]|^DFunLike|^FunLike|EquivLike|^Eq$|^OfNat|^H(Add|Mul|Sub|Div|Pow)|^Real$|^Complex$|^Nat$|^Fin$|^Mathlib\.(Meta|Tactic)|_simp_|congr_simp|vecCons|vecEmpty|^Finset\.univ$)')
HUBS = sorted([k for k in ext_users if not HUBINFRA.search(k[0])], key=lambda k: -len(ext_users[k]))[:40]  # 'main hubs' = most-used non-infrastructure Mathlib/Physlib constants
hubset = {h[0] for h in HUBS}

# ---- overlay ----
reviews = sorted((R/'reviews').glob('*.md'))
mod_rungs = collections.defaultdict(list)
for f in reviews:
    t = f.read_text(errors='ignore')
    m = RUNG_RE.match(f.name)
    if not m: continue
    for M in set(stage_of):
        k = mentions(M, t, [])  # code contexts only; backtick spans tokenised so a match cannot straddle two spans
        if k: mod_rungs[M].append((k, m.group(1), 'reviews/' + f.name))
for M in mod_rungs: mod_rungs[M].sort(reverse=True)
mission = (R/'MISSION.md').read_text().splitlines()
tally_line = next(i for i, l in enumerate(mission, 1) if l.startswith('**OFFICIAL OP-2 tally'))
CREDIT = {'MR-1b': ('blind', 1), 'MR-4': ('blind', 1), 'KL-LAT': ('blind', 0.5),
          'MR-2': ('VR', 0.5), 'KS-1': ('VR', 0.25), 'MR-1f': ('VR', 0.25)}
blk = {}
for l in (R/'notes/BLOCKER-INDEX-2026-10-13.md').read_text().splitlines():
    m = re.match(r'\| ([^|]+?) \| ((?:`[A-Z\-]+` ?)+) \|', l)
    if m: blk[m.group(1).strip()] = re.findall(r'`([A-Z\-]+)`', m.group(2))
audit = []
alines = (R/'notes/LEAN-AUDIT-2026-10-13.md').read_text().splitlines()
for i, l in enumerate(alines, 1):
    if l.startswith('| ') and '**' in l or re.search(r'\| (ALIGNED|\*\*OVERCLAIM)', l):
        cells = [c.strip() for c in l.strip('|').split('|')]
        if len(cells) >= 4 and ('ALIGNED' in cells[3] or 'OVERCLAIM' in cells[3]):
            audit.append((cells[0], cells[3], i))
PARAMS = {'m_pi': r'm_?\\?pi|Mπ|mπ|M_pi', 'm_rho': r'm_?\\?rho|mρ|M_rho', 'f_pi': r'f_?\\?pi|Fπ|fπ|F_pi',
  'm_K': r'm_?K\b|MK', 'scale': r'\bscale\b|dimensionful|\bunit\b', 'Nc': r'N_?c\b|1/N|large-N', 'alpha_prime': r"α'|alpha'|Regge slope",
  'couplings(g,lambda)': r'\bcoupling', 'LECs(L_i,l_i)': r'\bLECs?\b|\bL[0-9]\b|\bl[12]\b', 'vev': r'\bvev\b|v\.e\.v', 'spurion/quark mass': r'spurion|quark mass|m_q\b',
  'theta_W': r'θ_W|theta_W|weak mixing', 'shift ansatz': r'linear.shift|δ-shift|shift ansatz', 'sigma-term': r'σ-term|sigma-term', 'curvature c': r'curvature'}
STATUS = [('free', r'\bfree\b|not fixed|unfixed|leaves? .*free|undetermined|scale-blind|blind to'),
          ('input', r'\binputs?\b|fitted|hypothes|declared'), ('fixed', r'\bfix(es|ed)\b|forces?d?\b|predict')]
def param_hits(path, limit=40):
    out = []
    for i, l in enumerate((R/path).read_text(errors='ignore').splitlines(), 1):
        for p, rx in PARAMS.items():
            if re.search(rx, l):
                st = next((s for s, sx in STATUS if re.search(sx, l, re.I)), None)
                if st: out.append({'param': p, 'status': st, 'source': f'{path}:{i}', 'text': l.strip()[:160],
                                   'tag': 'EXTRACTED-UNCERTAIN'})
    return out[:limit]
# Primary rung (2026-10-28 deep review): first rung record in git history that mentions the module (scripts/primary_rung.py).
# Replaces the hand-pinned PRIMARY_OVERRIDE / PRIMARY_NONE lists and the most-mentions rule that let later reviews
# (R4-DM*, FT-5c, BR-4, ...) capture older modules. Regression gate: graph/primary_rungs.json is the committed baseline;
# a regen that changes any existing module's primary rung fails unless --accept-primary-changes is given.
PRIM = primary_rungs(R, sorted(stage_of), [(d['name'], mod(d)) for d in decls])
_base_p = R/'graph/primary_rungs.json'
_base = json.loads(_base_p.read_text()) if _base_p.exists() else {}
_changed = {M: (_base[M][0], PRIM[M][0]) for M in _base if M in PRIM and _base[M][0] != PRIM[M][0]}
if _changed and not ACCEPT:
    sys.exit('theorem_graph: primary_rung would change for %d modules (rerun with --accept-primary-changes after review): %s'
             % (len(_changed), _changed))
_base_p.write_text(json.dumps({M: list(v) for M, v in sorted(PRIM.items())}, indent=1, ensure_ascii=False) + '\n')
mod_over = {}
for M in stage_of:
    rungs = mod_rungs.get(M, [])
    prim = (0,) + tuple(PRIM[M]) if PRIM.get(M, (None,))[0] else None
    rnames = sorted({r for _, r, _ in rungs})
    a = [{'row': c, 'verdict': v, 'source': f'notes/LEAN-AUDIT-2026-10-13.md:{i}'} for c, v, i in audit if re.search(r'\b%s\b' % M, c)]
    mod_over[M] = {'stage': stage_of[M], 'primary_rung': prim[1] if prim else None, 'primary_review': prim[2] if prim else None,
        'rungs_mentioning': rnames,
        'credit': {r: {'line': CREDIT[r][0], 'value': CREDIT[r][1], 'source': f'MISSION.md:{tally_line}', 'via': fn,
                       'note': 'module cited in a review whose filename names this credited rung [EXTRACTED]'}
                   for _, _, fn in rungs for r in CREDIT if re.search(r'(^|[/-])%s-(result|gate|MR|KS|[0-9])' % re.escape(r), fn.split('/')[-1]) or fn.split('/')[-1].startswith(r + '-result')},
        'blocker_tags': {r: blk[r] for r in rnames if r in blk},
        'audit': a, 'params': param_hits(prim[2]) if prim else []}

# ---- analysis ----
U = G.to_undirected()
comps = sorted(nx.connected_components(U), key=len, reverse=True)
comp_id = {n: i for i, c in enumerate(comps) for n in c}
# module-level graph via declaration edges
MG = nx.Graph(); MG.add_nodes_from(stage_of)
for a, b, _ in int_edges:
    ma, mb = mod(byname[a]), mod(byname[b])
    if ma != mb: MG.add_edge(ma, mb, w=MG.get_edge_data(ma, mb, {'w': 0})['w'] + 1)
MG_noaudit = MG.subgraph([m for m in MG if m != 'AuditWitnesses'])
mcomps = sorted(nx.connected_components(MG_noaudit), key=len, reverse=True)
pr = nx.pagerank(G, alpha=0.85)  # edge a->b = a uses b, so mass flows to used lemmas
indeg = dict(G.in_degree())
thm = [d for d in decls if d['kind'] == 'thm']
orph = [d['name'] for d in thm if indeg[d['name']] == 0]
used_thm_by_thm = collections.Counter()
for a, b, part in int_edges:
    if byname[b]['kind'] == 'thm': used_thm_by_thm[b] += 1
central = sorted(thm, key=lambda d: (-used_thm_by_thm[d['name']], -pr[d['name']]))[:15]
central_defs = sorted([d for d in decls if d['kind'] == 'def'], key=lambda d: -indeg[d['name']])[:10]
# recurring params across modules
rec = collections.defaultdict(lambda: collections.Counter())
for M, o in mod_over.items():
    for p in o['params']: rec[p['param']][p['status']] += 1
rec_mods = {p: sorted({M for M, o in mod_over.items() for h in o['params'] if h['param'] == p}) for p in rec}
# bridge candidates: module-components sharing external hub lemmas (Jaccard)
mext = collections.defaultdict(set)
for a, b, m, _ in ext_edges: mext[mod(byname[a])].add(b)
cext = [set().union(*(mext[m] for m in c)) for c in mcomps]
# keep only "mathematical" external constants: not instances/coercions/structure projections, used by <=4 module components
INFRA = re.compile(r'(^inst|\.inst|Inst|\.to[A-Z]|^DFunLike|^FunLike|EquivLike|^Eq\b|^OfNat|^HAdd|^HMul|^HSub|^HDiv|^HPow|^Neg\b|^Real$|^Complex$|^Nat$|^Fin$|vecCons|vecEmpty|Matrix\.of$|^Finset\.sum$|^Finset\.univ$)')
df = collections.Counter(x for c in cext for x in c)
cext_f = [{x for x in c if not INFRA.search(x) and df[x] <= 4} for c in cext]
cand = []
for i in range(len(mcomps)):
    for j in range(i+1, len(mcomps)):
        inter = cext_f[i] & cext_f[j]
        if len(inter) >= 2:
            cand.append((round(sum(1.0/df[x] for x in inter), 3), sorted(mcomps[i]), sorted(mcomps[j]), sorted(inter)[:12]))
cand.sort(reverse=True)

for d in decls:
    d['component'] = comp_id[d['name']]; d['in_degree'] = indeg[d['name']]; d['pagerank'] = round(pr[d['name']], 6)
    d['overlay'] = {k: mod_over[mod(d)][k] for k in ('primary_rung', 'primary_review', 'credit', 'blocker_tags')} if mod(d) in mod_over else {}
    d['overlay']['audit'] = [a for a in mod_over.get(mod(d), {}).get('audit', []) if d['name'].split('.')[-1] in a['row'] or mod(d) + ' ' in a['row'] + ' ']
    d['hub_uses'] = sorted({u['n'] for u in d['type_uses'] + d['value_uses'] if u['n'] in hubset})
out = [{k: d[k] for k in ('name', 'module', 'kind', 'stage', 'statement', 'doc', 'axioms', 'trivial', 'trivial_reason', 'type_size',
        'value_size', 'line', 'end_line', 'component', 'in_degree', 'pagerank', 'overlay', 'hub_uses')} for d in decls]
json.dump({'generated': '2026-10-13', 'source': 'lean/GraphExport.lean + scripts/theorem_graph.py', 'nodes': out,
           'modules': mod_over, 'hubs': [{'name': h[0], 'module': h[1], 'users': len(ext_users[h])} for h in HUBS]},
          open(R/'graph/theorems.json', 'w'), indent=1, ensure_ascii=False)
with open(R/'graph/edges.csv', 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['source', 'target', 'via', 'target_kind', 'scope'])
    for a, b, p in sorted(set(int_edges)): w.writerow([a, b, p, byname[b]['kind'], 'PositiveGeometryEmergentSpaceTime'])
    for a, b, m, p in sorted(set(ext_edges)):
        if b in hubset: w.writerow([a, b, p, 'external', m.split('.')[0]])
GX = G.copy()
for n in GX: GX.nodes[n].update(module=byname[n]['module'], kind=byname[n]['kind'], stage=byname[n]['stage'], trivial=byname[n]['trivial'])
nx.write_graphml(GX, R/'graph/theorem-graph.graphml')

A = {'n_nodes': len(decls), 'n_thm': len(thm), 'n_def': len(decls)-len(thm), 'n_internal_edges': len(set((a, b) for a, b, _ in int_edges)),
     'n_external_edges_total': len(set((a, b) for a, b, _, _ in ext_edges)), 'n_hub_edges': len(set((a, b) for a, b, _, _ in ext_edges if b in hubset)),
     'n_decl_components': len(comps), 'decl_component_sizes_top': [len(c) for c in comps[:10]],
     'n_singletons': sum(1 for c in comps if len(c) == 1),
     'module_components_excl_audit': [sorted(c) for c in mcomps],
     'module_edges': sorted([(a, b, MG[a][b]['w']) for a, b in MG.edges()], key=lambda x: -x[2]),
     'trivial': sum(d['trivial'] for d in thm), 'substantive': sum(not d['trivial'] for d in thm),
     'trivial_by_reason': collections.Counter(d['trivial_reason'] for d in thm if d['trivial']),
     'central_theorems': [(d['name'], used_thm_by_thm[d['name']], round(pr[d['name']], 5)) for d in central],
     'central_defs': [(d['name'], indeg[d['name']]) for d in central_defs],
     'orphan_theorems': len(orph), 'orphan_substantive': sum(1 for n in orph if not byname[n]['trivial']),
     'thm_used_by_other_thm': sum(1 for d in thm if used_thm_by_thm[d['name']]),
     'recurring_params': {p: {'status_counts': dict(c), 'modules': rec_mods[p]} for p, c in sorted(rec.items(), key=lambda kv: -len(rec_mods[kv[0]]))},
     'bridge_candidates': cand[:25], 'hubs_top': [(h[0], len(ext_users[h])) for h in HUBS[:20]],
     'stage_counts': collections.Counter(d['stage'] for d in decls)}
json.dump(A, open(R/'graph/analysis.json', 'w'), indent=1, ensure_ascii=False, default=list)

# ---- figure ----
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
cols = dict(zip(STAGE, plt.cm.tab10.colors))
fig, ax = plt.subplots(1, 2, figsize=(20, 10), gridspec_kw={'width_ratios': [3, 2]})
MGf = MG_noaudit
pos = {}
big = [c for c in mcomps if len(c) > 1]; single = sorted([next(iter(c)) for c in mcomps if len(c) == 1], key=lambda m: (list(STAGE).index(stage_of[m]), m))
for i, c in enumerate(big):  # multi-module components on the top row
    sub = nx.spring_layout(MGf.subgraph(c), seed=1, k=1.2)
    for m, xy in sub.items(): pos[m] = (i * 3.0 + 1.2 * xy[0], 3.2 + 1.2 * xy[1])
ncol = 9
for j, m in enumerate(single):   # isolated modules in a grid, ordered by stage
    pos[m] = ((j % ncol) * (3.0 * max(len(big), 1) / ncol), 1.2 - (j // ncol) * 0.85)
MG = MGf
nsz = {m: 60 + 6*sum(1 for d in decls if mod(d) == m) for m in MG}
for e in MG.edges(): ax[0].plot(*zip(pos[e[0]], pos[e[1]]), color='grey', lw=0.4 + 0.15*min(MG[e[0]][e[1]]['w'], 20), alpha=.6, zorder=1)
for m in MG:
    ax[0].scatter(*pos[m], s=nsz[m], color=cols[stage_of[m]], edgecolor='k', lw=.4, zorder=2)
    ax[0].annotate(m, pos[m], fontsize=7, ha='center', va='bottom', xytext=(0, 4), textcoords='offset points')
for s, c in cols.items(): ax[0].scatter([], [], color=c, label=s)
ax[0].legend(fontsize=8, loc='upper center', bbox_to_anchor=(0.5, -0.01), ncol=3); ax[0].set_axis_off()
ax[0].set_title(f'PositiveGeometryEmergentSpaceTime Lean module graph (declaration-level uses)\n{len(thm)} thms, {len(decls)-len(thm)} defs, {len(mcomps)} module components; top row = linked clusters, grid = isolated', fontsize=11)
sc = collections.Counter((d['stage'], d['trivial']) for d in thm)
st = list(STAGE)
ax[1].barh(st, [sc[(s, False)] for s in st], color='tab:blue', label='substantive')
ax[1].barh(st, [sc[(s, True)] for s in st], left=[sc[(s, False)] for s in st], color='tab:orange', label='trivial (rfl/decide/norm_num/simp/ring one-liner or term ≤20)')
ax[1].invert_yaxis(); ax[1].legend(fontsize=8); ax[1].set_xlabel('theorems')
ax[1].set_title(f'Substantive {A["substantive"]} / trivial {A["trivial"]} (heuristic)', fontsize=11)
fig.text(0.01, 0.01, 'Generated 2026-10-13 by scripts/theorem_graph.py from the elaborated environment (lean/GraphExport.lean). Stage map is CURATED; overlay keyword-extracted.', fontsize=8)
plt.tight_layout(); plt.savefig(R/'figures/theorem-graph-2026-10-13.png', dpi=130)

# ---- standalone HTML (no CDN): precomputed spring layout on declarations, canvas render ----
P = nx.spring_layout(U, k=0.08, seed=3, iterations=60)
nodes = [{'id': d['name'], 'x': round(float(P[d['name']][0]), 4), 'y': round(float(P[d['name']][1]), 4), 'k': d['kind'], 's': d['stage'],
          't': d['trivial'], 'm': mod(d), 'st': d['statement'][:400], 'r': d['overlay'].get('primary_rung')} for d in decls]
idx = {n['id']: i for i, n in enumerate(nodes)}
E = [[idx[a], idx[b]] for a, b in set((a, b) for a, b, _ in int_edges)]
tpl = (R/'scripts/theorem_graph_template.html').read_text()
(R/'graph/theorem-graph.html').write_text(tpl.replace('/*DATA*/', 'const NODES=%s;const EDGES=%s;const COLS=%s;' % (
    json.dumps(nodes, ensure_ascii=False), json.dumps(E), json.dumps({s: matplotlib.colors.to_hex(c) for s, c in cols.items()}))))
print(json.dumps({k: A[k] for k in ('n_nodes', 'n_thm', 'n_def', 'n_internal_edges', 'n_hub_edges', 'n_decl_components', 'decl_component_sizes_top',
      'n_singletons', 'trivial', 'substantive', 'orphan_theorems', 'orphan_substantive', 'thm_used_by_other_thm')}, default=list))

BRIDGES = [('BR-1','UnequalLS','MassShift'),('BR-2','FT2Mesh','MassShift'),('BR-3','Network','Klein'),('BR-4','ScaleNoGo','SG1'),('BR-5','MassiveSpinor','EWZ1b'),('TG-6','RelEntropy','MarkovTrace')]
# 2026-10-14: graph-proposed bridge 'BR-6' renamed TG-6 (label only) to avoid clash with rung BR-6 (Spinor<->MassiveSpinor, PASS).
# BR-5 here = original MassiveSpinor<->EWZ1b proposal (NOT-FEASIBLE); BR-5' (BR5p) is the Lean EWZ1b.N rebuild, an internal module in S5.
# ---- minimal leanblueprint skeleton (not built here; needs `pip install leanblueprint`, https://github.com/PatrickMassot/leanblueprint) ----
bp = R/'blueprint/src'; bp.mkdir(parents=True, exist_ok=True)
lab = lambda m: 'mod:' + m
L = ['% AUTO-GENERATED by scripts/theorem_graph.py (2026-10-13). One node per Lean module (= rung artefact).',
     '% \\leanok = all its theorems compile with 0 sorry and standard axioms; \\uses = real declaration-level uses.',
     '% Mission links with NO Lean edge are listed as open (no \\leanok) nodes in the last section.']
for s, ms in STAGE_MODS.items():
    L.append('\\section{%s}' % s.replace('&', '\\&'))
    for m in ms:
        ds = [d for d in thm if mod(d) == m]
        if not ds: continue
        key = sorted(ds, key=lambda d: (d['trivial'], -d['value_size']))[:4]
        uses = sorted({lab(n) for n in MG.neighbors(m) if n != 'AuditWitnesses' and
                       any(mod(byname[b]) == n for a, b, _ in int_edges if mod(byname[a]) == m)}) if m in MG else []
        o = mod_over.get(m, {})
        L += ['\\begin{theorem}[%s]\\label{%s}' % (m, lab(m)), '\\lean{%s}' % ','.join(d['name'] for d in key), '\\leanok']
        if uses: L.append('\\uses{%s}' % ','.join(uses))
        L += ['Rung: %s. Review: \\texttt{%s}. %d theorems (%d substantive).' % (o.get('primary_rung') or '?',
              (o.get('primary_review') or '-').replace('_', '\\_'), len(ds), sum(not d['trivial'] for d in ds)), '\\end{theorem}', '']
L += ['\\section{Open mission links (no Lean edge; PROPOSED bridge rungs, see notes/THEOREM-GRAPH-2026-10-13.md)}']
for bid, a, b in BRIDGES:
    L += ['\\begin{conjecture}[%s]\\label{br:%s}' % (bid, bid), '\\uses{%s,%s}' % (lab(a), lab(b)), 'PROPOSED bridge, not proved.', '\\end{conjecture}', '']
(bp/'content.tex').write_text('\n'.join(L))
