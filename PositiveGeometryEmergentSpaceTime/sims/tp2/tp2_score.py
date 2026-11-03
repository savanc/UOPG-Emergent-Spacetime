pred=[1.0,1.28558,1.87939,1.96962,2.53209,2.87939,3.70167]
cells=[1.286,1.286,1.97,1.97,2.532,2.543,0.684,0.694]
for x in cells:
    if 1<x<4:
        p=min(pred,key=lambda q:abs(q-x)); print(x,"nearest",p,f"dev {100*abs(x-p)/p:.3f}%")
    else: print(x,"outside (1,4): not scored")
