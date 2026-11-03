# BR-5′ (post-prereg 52611fe): explicit ns, nt, ct on the hidden-zero locus from ewz1b.py rules, for Lean lemma statements.
import os,sys; D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','ewz1b'); sys.path.insert(0,D); os.chdir(D)  # read-only use of EW-Z1b rules
src=open('run2.py').read(); exec(src.split("print('CONTROL-0")[0])
hz={ee[(1,3)]:0,ep[(1,3)]:0,ep[(3,1)]:0}
tsol=S.solve(S.Eq(u-m2(1)-m2(3),2*k[0]*k[2]),t)[0]
f=lambda x:S.expand(S.sympify(x).subs(hz).subs(t,tsol))
out=[]
for (A_,B_),(C_,D_) in (((0,1),(2,3)),((1,2),(3,0))):
    Ja=J(*gen[A_],*gen[B_]); Jb=J(*gen[C_],*gen[D_])
    v4,_=parts(V(Ja.d,0),V(Jb.d,0)); out.append(f(v4-Ja.f*Jb.f))
_,ct=amp(gen); out.append(f(ct))
ren={k[0]:S.Symbol('x.k1'),k[1]:S.Symbol('x.k2'),k[2]:S.Symbol('x.k3')}
for nm,e in zip(('ns','nt','ct'),out):
    e=e.subs(ren,simultaneous=True)
    txt=S.sstr(e).replace('**','^')
    import re
    txt=re.sub(r'\b(a|e\dp\d|ee\d\d|lam3|lam4|s|gs|b)\b',lambda m:'x.'+m.group(1),txt)
    print(nm,'gs' in str(e.free_symbols),'b' in {str(v) for v in e.free_symbols})
    open(f'/tmp/{nm}.txt','w').write(txt)
