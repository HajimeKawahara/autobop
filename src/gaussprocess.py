#!/usr/bin/python
import sys
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab 


def farey( n, asc=True ):
    #from wikipedia
    arr=[]
    if asc: 
        a, b, c, d = 0, 1,  1 , n     # (*)
    else:
        a, b, c, d = 1, 1, n-1, n     # (*)
#    arr.append([a,b])
    while (asc and c <= n) or (not asc and a > 0):
        k = int((n + b)/d)
        a, b, c, d = c, d, k*c - a, k*d - b
        arr.append([a,b])

    return arr[:-1]

def simple_gp():
    nsamp=2*2*2*2*3*5
    f=np.ones(nsamp)/float(nsamp)
    val=np.random.rand(3)
    f[nsamp/2]=100.0*val[0]
    f[2*nsamp/3]=100.0*val[1]
    f[nsamp/3]=100.0*val[2]

    sig=np.sqrt(f/2)
    a=np.random.normal(loc=0.0, scale=1.0, size=nsamp)*sig
    b=np.random.normal(loc=0.0, scale=1.0, size=nsamp)*sig
    c=np.hstack((a+b*1j,0.0+0.0j))
    delta=np.fft.irfft(c)
    cumd=np.cumsum(delta)

    #amplitude
    val=np.random.rand()    
    mRNA=np.array(cumd)*4.0*val

    return mRNA


def farey_gp(ngpfarey,gpampfarey,cgpwfarey):
    n=ngpfarey
    nsamp=np.prod(n)*2*2*2*2
    f=np.ones(nsamp)/float(nsamp)*0.1
#    f=np.ones(nsamp)/float(nsamp)*10.0 ##more 
    farr=farey(n, asc=True)
    r=np.random.rand()
    iarr=np.digitize([r],cgpwfarey)[0]
    f[int(nsamp*farr[iarr][0]/farr[iarr][1])]=gpampfarey
    print("Farey =",farr[iarr][0],"/",farr[iarr][1])

    sig=np.sqrt(f/2)
    a=np.random.normal(loc=0.0, scale=1.0, size=nsamp)*sig
    b=np.random.normal(loc=0.0, scale=1.0, size=nsamp)*sig
    c=np.hstack((a+b*1j,0.0+0.0j))
    delta=np.fft.irfft(c)
    cumd=np.cumsum(delta)

    #amplitude
    val=np.random.rand()    
    mRNA=np.array(cumd)*4.0*val

    return mRNA

def read_fareyfile(file):
    g=open(file,"r")
    n=int(g.readline())
    amp=float(g.readline())
    g.close()
    
    data=np.loadtxt(file,dtype={'names': ('numden','weight'), 'formats': ('S8','f4')},skiprows=2)
    gpwfarey=data["weight"]

    print("READ",file) 
    print("n",n)
    print("amplitude",amp)
    print(data["numden"],"<=")

    cgpwfarey=np.cumsum(gpwfarey/np.sum(gpwfarey))
    return n,amp,cgpwfarey

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Gauss process')
    parser.add_argument('-n', nargs=1, help='Generate Farey Sequence', type=int)
    parser.add_argument('-f', nargs=1, default=["test.farey"],help='Farey file', type=str)
    args = parser.parse_args()    

#    nf,val,weight=read_fareyfile("test.farey")
#    sys.exit()
    
    if args.n:
        file=args.f[0]
        farr=farey(args.n[0], asc=True)
        print(file)
        g=open(file,"w")
        g.writelines(str(args.n[0])+"\n")
        g.writelines("30.0\n")
        for ff in farr:
            g.writelines(str(ff[0])+"/"+str(ff[1])+" 1.0\n")
        g.close()
        sys.exit()

    ngpfarey,gpampfarey,cgpwfarey=read_fareyfile(args.f[0])
    mRNA=farey_gp(ngpfarey,gpampfarey,cgpwfarey)
    x=np.array(list(range(0,len(mRNA))))

    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(x,mRNA,".")
    ax.plot(x,mRNA)
    plt.show()
    
