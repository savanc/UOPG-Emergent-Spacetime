exec(open('run2.py').read().split("print('CONTROL-0")[0])
cK=S.Symbol('cK')
kh={k[2]:0,k[1]:-k[0]}
r,ct=amp([W(1),W(2),H(3),H(4)]); Aw=r+ct + (-1)*(a*ee[(1,2)]*(k[0]-k[1]))*kap3*E5[2]*E5[3]/s
print('[WWhh] SSB + h^3=cK*k1 on HZ:',HZ(Aw.subs(one).subs(kap3,cK*k[0]),0,kh))
kh2={k[1]:0,k[2]:-k[0]}
r,ct=amp([W(1),H(2),W(3),H(4)]); e=HZ(r+ct,2*k[0]*k[2],kh2)
print('[WhWh] deformed on HZ:',S.factor(e))
