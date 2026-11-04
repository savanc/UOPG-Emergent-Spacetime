"""KL-LAT predictions (inputs only; no K* value read). m_K*^2 = m_K^2 + m_rho^2 - m_pi^2 (Lean UnequalLS.kstar_relation);
m_K2*^2 = m_K^2 + 3(m_rho^2 - m_pi^2) (mass_formula, J=2). Units: lattice (a_t or a); ratios only."""
import json,math
E={ # id: group, mpi, dmpi, mK, dmK, mrho, dmrho, sources, note
"G1-391":("HadSpec",0.06906,0.00013,0.09698,0.00009,0.15095,0.00015,"1904.03188 T.I; rho 1507.02599 T.III (BW mR)","PARTIAL memory"),
"G1-239":("HadSpec",0.03928,0.00018,0.08344,0.00007,0.13175,0.00035,"1904.03188 T.I; rho 1507.02599 (BW mR, mpi 236/239 same ensemble)",""),
"G2-317":("Alexandrou/Rendon et al.",0.18295,0.00036,0.30475,0.00017,0.4609,0.0021,"K input 2006.14035; rho 1704.05439 (amrho stat+sys)",""),
"G4-230":("Bulava/Morningstar et al.",0.03938,0.00019,0.08354,0.00015,3.350*0.03938,math.hypot(0.024*0.03938,3.350*0.00019),"1802.03100 T.1; rho 1604.05593 (mrho/mpi=3.350(24))",""),
}
out={}
for k,(g,p,dp,K,dK,r,dr,src,note) in E.items():
    m1=math.sqrt(K*K+r*r-p*p); m2=math.sqrt(K*K+3*(r*r-p*p))
    d=(m1-r)/(K-p); sel=(K-p)/r
    out[k]=dict(group=g,inputs=dict(mpi=p,mK=K,mrho=r,dmrho=dr),sel=round(sel,3),mKstar_pred=round(m1,5),mKstar_over_mrho=round(m1/r,4),mK2star_pred=round(m2,5),delta_pred=round(d,4),src=src,note=note)
    print(k,g,"sel %.3f"%sel,"pred m_K* %.5f (m_K*/m_rho %.4f) m_K2* %.5f delta_pred %.4f"%(m1,m1/r,m2,d))
json.dump(out,open("sims/kllat/predictions.json","w"),indent=1)
