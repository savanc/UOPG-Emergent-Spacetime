import random; from ft5a import *
rng=random.Random(5)
mu={'u':Fr(1),'d':Fr(2),'s':Fr(7)}
for n,f in [(4,list('udsu')),(6,list('udsuds'))]:
  for t in range(2):
    ff=f+[f[0]]; msq=[mu[ff[k]]+mu[ff[k+1]] for k in range(n)]
    while True:
      try: g=kin(n,msq,[],rng); a=amp_ft2(n,g,mu,ff,'exp'); b=amp(n,g,mu,ff,'exp'); break
      except ZeroDivisionError: pass
    print(n,'LO engine match:',(a-b.a).iszero())
    for op in OPS:
      e=amp(n,g,mu,ff,'exp',eps_terms=OPS[op]).b; c=amp(n,g,mu,ff,'cay',eps_terms=OPS[op]).b
      print('  ',op,'exp==cay:',(e-c).iszero(),'nonzero:',not e.iszero())
