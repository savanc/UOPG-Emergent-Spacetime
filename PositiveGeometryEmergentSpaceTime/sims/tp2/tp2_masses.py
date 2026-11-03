import numpy as np
edges=[(0,1),(1,2),(2,3),(3,4),(4,5),(2,6)]  # E7: arms 2,3,1 from node 2
A=np.zeros((7,7))
for i,j in edges: A[i,j]=A[j,i]=1
w,V=np.linalg.eigh(A); v=np.sort(np.abs(V[:,-1])); m=v/v[0]
print("PF",w[-1],"2cos(pi/18)",2*np.cos(np.pi/18)); print("ratios"," ".join(f"{x:.5f}" for x in m))
