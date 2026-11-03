exec(open('run2.py').read().split("print('CONTROL-0")[0])
kd={k[2]:-k[1]}  # t-channel internal diagonal: exchanged 5th comp = physical neutral Higgs (massless here), unitary-gauge-physical
e=HZ(A4(gen),2*k[0]*k[2],kd)
solve_forced(e,'FORCE WW->WW with physical h in t-channel:',[a,lam4])
print('SSB value:',HZ(A4(gen).subs(one),2*k[0]*k[2],kd))
