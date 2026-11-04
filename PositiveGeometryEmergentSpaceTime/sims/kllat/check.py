"""KL-LAT check vs lattice K* (read AFTER 00dbe80). Rule from prereg/KL-LAT-prereg-2026-10-13.md."""
import json,math
P=json.load(open("sims/kllat/predictions.json"))
W=1672.45 # Omega MeV (HadSpec scale convention of 1904.03188)
T={ # id: (a m_K*, err, source)
"G1-391":(936/(W/0.2951),math.hypot(1/936,0.0022/0.2951)*936/(W/0.2951),"1904.03188 T.II BW mR=936(1) MeV, scale aΩ=0.2951(22)"),
"G1-239":(904/(W/0.2751),math.hypot(1/904,0.0006/0.2751)*904/(W/0.2751),"1904.03188 T.II BW mR=904(1) MeV, scale aΩ=0.2751(6)"),
"G2-317":(0.8951/(0.197327/0.11403),0.0064/(0.197327/0.11403),"2006.14035 pole Re 0.8951(64) GeV, a=0.11403 fm (same a as rho paper)"),
"G4-230":(3.808*0.03938,math.hypot(0.018*0.03938,3.808*0.00019),"1802.03100 eq.4.1 mK*/mpi=3.808(18)"),
}
R={}
for k,(m,dm,src) in T.items():
    p=P[k];i=p["inputs"];pi,K,r,dr=i["mpi"],i["mK"],i["mrho"],i["dmrho"]
    d=(m-r)/(K-pi); sd=math.hypot(dm,dr)/(K-pi)
    band=max(2*sd,0.10); dp=p["delta_pred"]; ok=abs(d-dp)<=band
    lo,hi=max(0,dp-band),min(1,dp+band); f=hi-lo
    R[k]=dict(delta_obs=round(d,4),sigma=round(sd,4),delta_pred=dp,band=round(band,3),PASS=ok,null_f=round(f,3),
             mKstar_obs=round(m,5),mKstar_pred=p["mKstar_pred"],rel_err_m=round(p["mKstar_pred"]/m-1,4),src=src)
    print(k,R[k])
json.dump(R,open("sims/kllat/check.json","w"),indent=1)
