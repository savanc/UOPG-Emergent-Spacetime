# TP-1c: E8 Toda masses = PF eigenvector of E8 Dynkin adjacency (Freeman 1991). Sorted, normalised to m1.
import numpy as np
edges=[(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(2,7)]  # E8: chain 0..6, branch 7 at node 2 (arms 2,4,1)
A=np.zeros((8,8))
for i,j in edges: A[i,j]=A[j,i]=1
w,V=np.linalg.eigh(A); v=np.abs(V[:,-1]); m=np.sort(v)/np.sort(v)[0]
print("PF eigenvalue",w[-1],"2cos(pi/30)",2*np.cos(np.pi/30))
for k,x in enumerate(m,1): print(f"m{k}/m1 = {x:.6f}")
