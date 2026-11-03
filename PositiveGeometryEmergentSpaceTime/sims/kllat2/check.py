import json,math
pred=json.load(open("predictions.json"))
TP=json.load(open("targets_sealed_pacs.json")); TQ=json.load(open("targets_sealed_pq.json"))
c=0.411; dphys=0.336; ephys=0.341
rows=[]
for p in pred:
    if not p["scored"]: continue
    pi,K,r=p["pi"][0],p["K"][0],p["rho"][0]; dr=p["rho"][1]; dK=p["K"][1]; dpi=p["pi"][1]
    if p["group"]=="PACS-CS":
        Ks=TP[p["tkey"]]["Ks"]; ph=TP[p["tkey"]]["phi"]
    else:
        T=TQ[p["tkey"]]; ks,k2=p["ks"],p["k2"]
        Ks=T.get(f"V:{ks},{k2}") or T.get(f"V:{k2},{ks}"); ph=T.get(f"V:{k2},{k2}")
    grp="Tsukuba" if p["group"] in("PACS-CS","CPPACS") else "UKQCD"
    D=K-pi
    for name,obs,predm,scale,phys,nshift in [("Kstar",Ks,p["mKs_pred"],D,dphys,1),("phi",ph,p["mphi_pred"],2*D,ephys,2)]:
        if not obs: continue
        o=(obs[0]-r)/scale; pr=(predm-r)/scale
        sig=math.hypot(obs[1],dr)/scale; sig=math.hypot(sig,abs(pr-o)*math.hypot(dK,dpi)/D)
        band=max(2*sig,0.10)
        n2m=r+nshift*c*(K*K-pi*pi)/r; n2=(n2m-r)/scale
        f=min(1,max(0,min(1,pr+band)-max(0,pr-band)))
        rows.append(dict(id=p["id"],grp=grp,obs=name,o=o,pr=pr,band=band,ok=abs(o-pr)<=band,n2ok=abs(o-n2)<=band,n3ok=abs(o-phys)<=band,res=abs(o-pr),n2res=abs(o-n2),n3res=abs(o-phys),f=f,mres=(predm-obs[0])/obs[0],mres_alt=((p["mphi_alt"]-obs[0])/obs[0] if name=="phi" else None)))
for r_ in rows: print("%-34s %-7s %-5s obs %.3f pred %.3f band %.3f %s | N2 %s N3 %s f %.2f | mass res %+.2f%%"%(r_["id"],r_["grp"],r_["obs"],r_["o"],r_["pr"],r_["band"],"PASS" if r_["ok"] else "FAIL","y" if r_["n2ok"] else "n","y" if r_["n3ok"] else "n",r_["f"],100*r_["mres"]))
S={}
for ob in["Kstar","phi"]:
    for g in["Tsukuba","UKQCD"]:
        R=[x for x in rows if x["obs"]==ob and x["grp"]==g]
        if not R: continue
        m=lambda k:sum(x[k] for x in R)/len(R)
        s=dict(n=len(R),pass_=m("ok"),n2=m("n2ok"),n3=m("n3ok"),res=m("res"),n2res=m("n2res"),n3res=m("n3res"),f=m("f"),high=sum(x["mres"]>0 for x in R)/len(R),mres=m("mres"))
        S[f"{ob}/{g}"]=s; print(ob,g,{k:round(v,3) for k,v in s.items()})
json.dump(dict(rows=rows,summary=S),open("check_output.json","w"),indent=1)
