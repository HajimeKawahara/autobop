#!/usr/bin/python
import argparse
import numpy as np
import sound_driver as sd
import pyaudio
import wave
import gcc
import sys
import matplotlib
import matplotlib.pyplot as plt
import pylab 
import sound_definition as sd
import generate_cp as gcp
import chord_probability as cp


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interactive')
    parser.add_argument('-key', nargs=1, default="C",help='key',type=str)
    parser.add_argument('-c', nargs=1, required=True, help='chord',type=str)
    parser.add_argument('-cel', nargs=1, required=True, help='cel list',type=str)
    parser.add_argument('-t', nargs=2, default=[0.01,10.0],help='tmin,tmax',type=float)
    args = parser.parse_args()   
    ng=sd.getng()
    ikey=ng[args.key[0]]
    tmin=args.t[0]
    tmax=args.t[1]

    col=["#E60012","#F39800","#FFF100","#8FC31F","#009944","#009E96","#00A0E9","#0068B7","#1D2088","#920783","#E4007F","#E5004F"]

    chord=args.c[0]
    noct=1
    if args.cel:
        pcel=gcp.read_cep_list(args.cel[0])
    print(pcel[chord])

    tlist=np.logspace(np.log10(tmin),np.log10(tmax),100)
    x=[]
    y=[]    
    for teff in tlist:
        prelative=gcp.pcel2prelative(pcel,teff)
    #    gcp.pcel2prelative(pcel,teff*pstab[ibeat])
        phg=cp.get_pchord(prelative,[ikey],chord,noct)
        phg=phg/np.sum(phg)
        chg=np.cumsum(phg)
        x.append(teff)
        y.append(np.hstack((0.0,chg)))

    x=np.array(x)
    y=np.array(y)
    tone=sd.getsg()
    hg=sd.gethg()
    xcap=[]
    ycap=[]
    for i in range(0,12):
        imax=np.argmax(y.transpose()[i+1]-y.transpose()[i])
        xcap.append(x[imax])
        tmp=(y.transpose()[i+1]+y.transpose()[i])/2.0
        ycap.append(tmp[imax])
        
    fig = plt.figure()
    ax = fig.add_subplot(111)
    pylab.title(args.key[0]+chord)
    ax.plot(x,y,color="black")
    pylab.xscale("log")
    pylab.xlabel("teff")
    pylab.ylabel("probability")
    pylab.xlim(tmin,tmax)
    for i in range(0,12):
        plt.fill_between(x,y.transpose()[i],y.transpose()[i+1],facecolor=col[i],alpha=0.5)
        ax.annotate(tone[i], xy=(xcap[i],ycap[i]), xycoords='data', fontsize=12,horizontalalignment="center",verticalalignment="center",color="black")

    plt.show()
