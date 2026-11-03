"""Parse CP-PACS Nf=2 (hep-lat/0105015, tab:meson) and UKQCD Nf=2 (hep-lat/0107021, tb:ps/tb:vector).
Writes inputs (all PS masses, unitary V=rho) to inputs_pq.json; seals non-unitary V (K*, phi targets) to targets_sealed_pq.json. Prints no target."""
import re,json,glob
def err(v,e): d=len(v.split('.')[1]); return round(int(e)*10**(-d),6)
data={}
# CP-PACS
t=open(glob.glob("src/cppacs2/*.tex")[0]).read()
i=t.index(r"\label{tab:meson}"); j=t.index(r"\end{tabular}",i); blk=t[i:j]
for sec in re.split(r"\\multicolumn\{16\}\{c\}\{",blk)[1:]:
    m=re.match(r"\$\\beta=([\d.]+)\$, \$\\kappa_\{\\rm sea\} = ([\d.]+)\$",sec); b,ks=m.groups()
    rows=re.findall(r"(0\.\d{4}) & (0\.\d{4}) & (\d)&(\d+)\((\d+)\)\s*& \[[^\]]*\] &\s*\d&[\d.]+\([\d.]+\)\s*& (\d)&(\d+)\((\d+)\)",sec)
    for k1,k2,pi,pf,pe,vi,vf,ve in rows:
        ps=pi+"."+pf; v=vi+"."+vf
        data.setdefault(("CPPACS",b,ks),{})[(k1,k2)]=dict(ps=(float(ps),err(ps,pe)),v=(float(v),err(v,ve)))
# UKQCD
u=open(glob.glob("src/ukqcd/*.tex")[0]).read()
def tab(lbl):
    i=u.index(lbl); j=u.rindex(r"\begin{tabular}",0,i); return u[j:i]
pat=r"& (\d\.\d+) & (0\.\d+) & (0\.\d+) & (0\.\d+) & [\d.]+\\err\{\s*\d+\}\{\s*\d+\} & (\d\.\d+)\\err\{\s*(\d+)\}\{\s*(\d+)\}"
for lbl,key in [(r"\label{tb:ps}","ps"),(r"\label{tb:vector}","v")]:
    for b,ks,k1,k2,a,ep,em in re.findall(pat,tab(lbl)):
        e=err(a,str(max(int(ep),int(em))))
        data.setdefault(("UKQCD",b,ks),{}).setdefault((k1,k2),{})[key]=(float(a),e)
inp={};tgt={}
for (g,b,ks),d in data.items():
    key=f"{g}-b{b}-ks{ks}"; I={};T={}
    for (k1,k2),r in d.items():
        kk=f"{k1},{k2}"
        if "ps" in r: I["PS:"+kk]=r["ps"]
        if "v" in r:
            if k1==ks and k2==ks: I["V:"+kk]=r["v"]
            else: T["V:"+kk]=r["v"]
    inp[key]=I; tgt[key]=T
json.dump(inp,open("inputs_pq.json","w"),indent=1); json.dump(tgt,open("targets_sealed_pq.json","w"))
for k in inp: print(k,"nPS",sum(1 for x in inp[k] if x.startswith("PS")),"rho" ,any(x.startswith("V") for x in inp[k]),"nT",len(tgt[k]))
