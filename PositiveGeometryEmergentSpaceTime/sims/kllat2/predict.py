"""KL-LAT2 predictions from INPUTS ONLY (pseudoscalars + same-ensemble unitary rho). No target read.
K*: m^2 = mK^2 + mrho^2 - mpi^2 (UnequalLS.kstar_relation). phi: m^2 = 2mK^2 + mrho^2 - 2mpi^2 (KLPhi.phi_relation, LO GMOR).
phi_alt (secondary): m^2 = m_etass^2 + mrho^2 - mpi^2 (lattice etass instead of GMOR)."""
import json,math
P=[]
pac=json.load(open("inputs_pacs.json"))
for k,d in pac.items():
    P.append(dict(id=k,group="PACS-CS",pi=d["pi"],K=d["K"],ess=d["etass"],rho=d["rho"],tkey=k))
pq=json.load(open("inputs_pq.json"))
for ens,d in pq.items():
    g=ens.split("-")[0]; ks=ens.split("-ks")[1]
    if ks=="0.0000": continue
    rho=d.get(f"V:{ks},{ks}"); pi=d.get(f"PS:{ks},{ks}")
    if not rho or not pi: continue
    vals=set()
    for x in d:
        a,b=x[3:].split(","); vals|={a,b}
    for k2 in sorted(vals):
        if float(k2)>=float(ks): continue   # strange-like = heavier valence quark (smaller kappa)
        K=d.get(f"PS:{ks},{k2}") or d.get(f"PS:{k2},{ks}"); ess=d.get(f"PS:{k2},{k2}")
        if not K or not ess: continue
        P.append(dict(id=f"{ens}-s{k2}",group=g,pi=pi,K=K,ess=ess,rho=rho,tkey=ens,ks=ks,k2=k2))
out=[]
for p in P:
    pi,K,es,r=p["pi"][0],p["K"][0],p["ess"][0],p["rho"][0]
    sel=(K-pi)/r; ratio=pi/r
    p["mKs_pred"]=math.sqrt(K*K+r*r-pi*pi)
    p["mphi_pred"]=math.sqrt(2*K*K+r*r-2*pi*pi)
    p["mphi_alt"]=math.sqrt(es*es+r*r-pi*pi)
    p["dKs_pred"]=(p["mKs_pred"]-r)/(K-pi)
    p["ephi_pred"]=(p["mphi_pred"]-r)/(2*(K-pi))
    p["sel"]=sel; p["mpi_over_mrho"]=ratio
    p["scored"]= sel>=0.10 and ratio<=0.80 and pi>=0  # PACS m_pi>=200 MeV checked below
    out.append(p)
# PACS-CS: exclude m_pi<200 MeV (a^-1 ~ 2.2 GeV => a m_pi < 0.09) by prereg
for p in out:
    if p["group"]=="PACS-CS" and p["pi"][0]<0.09: p["scored"]=False
json.dump(out,open("predictions.json","w"),indent=1)
n={}
for p in out:
    if p["scored"]: n[p["group"]]=n.get(p["group"],0)+1
    print(p["id"],"scored" if p["scored"] else "--","sel %.3f mpi/mrho %.3f | K* %.4f d %.3f | phi %.4f e %.3f | phi_alt %.4f"%(p["sel"],p["mpi_over_mrho"],p["mKs_pred"],p["dKs_pred"],p["mphi_pred"],p["ephi_pred"],p["mphi_alt"]))
print("scored per group",n)
