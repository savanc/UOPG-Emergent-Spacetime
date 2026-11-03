"""Parse PACS-CS 0807.1661 Table (lattice-unit masses). Writes inputs.json (pi,K,rho,eta_ss) and SEALED targets_sealed.json (K*,phi) without printing targets."""
import re,json
t=open("src/0807.1661/tables.tex").read()
i=t.index("Meson and baryon masses in lattice units"); i=t.index("begin{tabular}",i); blk=t[i:i+6000]
def row(lbl):
    j=blk.index(lbl); seg=blk[j:j+260]
    return [(a,b) for a,b in re.findall(r"(\d\.\d{4,5})\((\d+)\)",seg)][:6]
def ku(lbl):
    j=blk.index(lbl); return re.findall(r"0\.\d{5}",blk[j:j+220])[:6]
def val(p):
    v,e=p; dec=len(v.split('.')[1]); return float(v),round(int(e)*10**(-dec),6)
kud=ku(r"$\kappa_{\rm ud}$"); ks=ku(r"$\kappa_{\rm s}$")
inp={}; tgt={}
P={k:row(l) for k,l in [("pi",r"$\pi$"),("K","$K$ "),("etass",r"$\eta_{\rm ss}$"),("rho",r"$\rho$ "),("Ks","$K^*$"),("phi",r"$\phi$")]}
for n in range(6):
    key=f"PACS-{kud[n]}-{ks[n]}"
    inp[key]={k:val(P[k][n]) for k in ["pi","K","etass","rho"]}
    tgt[key]={k:val(P[k][n]) for k in ["Ks","phi"]}
json.dump(inp,open("inputs_pacs.json","w"),indent=1); json.dump(tgt,open("targets_sealed_pacs.json","w"))
for k,v in inp.items(): print(k,v)
