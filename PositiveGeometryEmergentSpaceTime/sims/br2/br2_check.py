# BR-2 exploratory check (run AFTER prereg? no -- see review: run before prereg commit is disclosed)
import sympy as sp
X=dict((k,sp.Symbol('X'+k)) for k in ['13','14','15','24','25','26','35','36','46'])
n1,n2,n3=sp.symbols('n1 n2 n3')
def A6N(a): 
    X13,X14,X15,X24,X25,X26,X35,X36,X46=[a[k] for k in ['13','14','15','24','25','26','35','36','46']]
    return ((X13+X24)*(X15+X46)/X14-X13-X24)+((X35+X46)*(X13+X26)/X36-X35-X46)+((X15+X26)*(X35+X24)/X25-X15-X26)
nu={1:n1,2:n2,3:n3,4:-n1,5:-n2,6:-n3}
Y={k:X[k]+nu[int(k[0])]+nu[int(k[1])] for k in X}
print("general nu (pole-preserving) invariant:",sp.simplify(A6N(Y)-A6N(X))==0)
