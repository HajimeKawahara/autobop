#!/usr/bin/python
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab 
import argparse

def brownianbridge_mRNA(x0,y0,x1,y1,var, beta, mRNA):
    if x1-x0 < 0.01:
#        ax.plot(x1,y1,".")
        mRNA.append([x1,y1])
        return 

    xm=(x0+x1)/2.0
    ym=(y0+y1)/2.0
    sigma=np.sqrt(var)
    delta = sigma*np.random.randn()
    brownianbridge_mRNA(x0,y0,xm,ym+delta,var/beta, beta, mRNA)
    brownianbridge_mRNA(xm,ym+delta,x1,y1,var/beta, beta, mRNA)
    return


def curve(x0,y0,x1,y1,var, beta, data):
    if x1-x0 < 0.01:
#        ax.plot(x1,y1,".")
        data.append([x1,y1])
        return 

    xm=(x0+x1)/2.0
    ym=(y0+y1)/2.0
    sigma=np.sqrt(var)
    delta = sigma*np.random.randn()
    curve(x0,y0,xm,ym+delta,var/beta, beta, data)
    curve(xm,ym+delta,x1,y1,var/beta, beta, data)

    return 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Markov bebop')
    parser.add_argument('-H', nargs=1, default=[0.5], help='Hurst parameter',type=float)    
    args = parser.parse_args()    

    H=args.H[0]
    var=0.3

    x0=0.0
    y0=0.0
    x1=1.0
    y1=0.0

    beta=2.0**(2.0*H)

    data=[[x0,y0]]
    curve(x0,y0,x1,y1,var,beta,data)
    data=np.array(data)
    print(data.shape)

    fig=plt.figure()
    ax=fig.add_subplot(111)
    pylab.title("Brownian Bridge: H="+str(H))
    pylab.ylim([-3*np.std(data[:,1]),3*np.std(data[:,1])])
    ax.plot(data[:,0],data[:,1])    
    pylab.xlabel("normalized time t")
    pylab.ylabel("y")
    plt.show()
    #print x0,y0
    #print x1,y1
