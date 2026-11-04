import math;c=0.411
mx=(0,None)
for y in [i/100 for i in range(10,60,5)]:
  for x in [i/100 for i in range(50,101,5)]:
    if x<=y: continue
    u=x*x-y*y
    a=(math.sqrt(1+u)-(1+c*u))/(1+c*u); b=(math.sqrt(1+2*u)-(1+2*c*u))/(1+2*c*u)
    if max(abs(a),abs(b))>mx[0]: mx=(max(abs(a),abs(b)),(y,x,a,b))
print("max rel mass diff KL vs N2 over pi/rho 0.10-0.55, K/rho 0.50-1.00:",mx)
