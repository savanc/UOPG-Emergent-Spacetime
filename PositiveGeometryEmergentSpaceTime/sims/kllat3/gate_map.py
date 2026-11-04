# KL-LAT3 gate: inputs-only map of |stat_KL - stat_N2| vs band floor 0.10 (stat=(mV-mrho)/(n*(mK-mpi)))
import math,json
c=0.411
out=[]
print("pi/rho  K/rho  d=(K-pi)/rho  dKs  dphi")
for y in [0.15,0.2,0.25,0.3,0.35,0.4,0.5]:
  for x in [0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.9]:
    if x<=y: continue
    u=x*x-y*y; d=x-y
    ks=(math.sqrt(1+u)-1-c*u)/d
    ph=(math.sqrt(1+2*u)-1-2*c*u)/(2*d)
    out.append(dict(pi=y,K=x,d=d,dKs=ks,dphi=ph)); print("%.2f %.2f %.3f %+.3f %+.3f"%(y,x,d,ks,ph))
json.dump(out,open("gate_map.json","w"),indent=1)
