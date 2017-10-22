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

def onclick(event):
    global xr
    global yr


    col=["black","red","blue","green"]
    if len(xr)<11:
        ax.set_title(str(11-len(xr))+" notes remain")
    elif len(xr)==11:
        ax.set_title("Complete")

    ax.plot([int(event.xdata),int(event.xdata)+1], [event.ydata,event.ydata],color=col[event.button])
    ax.plot([-2,0], [event.ydata,event.ydata],color=col[event.button],lw=2)
    ax.plot([event.xdata], [event.ydata],"o",color=col[event.button])
    i=int(event.xdata)
    ax.annotate(tone[i], xy=(-1.0, event.ydata), xycoords='data', fontsize=16,horizontalalignment="center")
    xr.append(i)
    yr.append(event.ydata)

    fig.canvas.draw()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Interactive')
    parser.add_argument('-c', nargs=1, required=True, help='chord',type=str)
    parser.add_argument('-cel', nargs=1, help='cel list',type=str)
    parser.add_argument('-log', help='log', action='store_true')
    parser.add_argument('-t', nargs='+', default=[0.01,0.03,0.1,0.3,1.0,3.0,10.0], help='temperature list',type=float)

    args = parser.parse_args()   
    tlist=args.t

    chord=args.c[0]
    if args.cel:
        pcel=gcp.read_cep_list(args.cel[0])

    tone=sd.getsg()
    hg=sd.gethg()
    xr=[]
    yr=[]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    if args.log:
        pylab.yscale("log")
        pylab.ylim(0.01,10.0)    
    else:
        pylab.ylim(0.0,10.0)    


    if args.cel:
        pylab.xlim(0.0-len(pcel)-8,12.0)    
        i=0
        for dispchord in pcel:
#            print pcel[dispchord]
            ax.annotate(dispchord, xy=(float(-i)-7.5, 10.0), xycoords='data', fontsize=12,horizontalalignment="center")
            pylab.axvline(float(i),ls="dashed")
            for energy in pcel[dispchord]:
                ax.plot([-i-8,-i-7],[energy,energy],color="blue")
                
            i=i+1

    plist=np.linspace(0,10,10000)
    for t in tlist:
        ax.plot(gcp.pmb(plist,t)*t*10-6,plist)
        ax.annotate(str(t), xy=(gcp.pmb(t,t)*t*10-6, t), xycoords='data', fontsize=12)


    for i in range(0,12):
        ax.annotate(tone[i], xy=(float(i)+0.5, 0.01), xycoords='data', fontsize=14,horizontalalignment="center")
        pylab.axvline(float(i),ls="dashed")

    for i in range(1,11):
        pylab.axhline(i,ls="dotted",color="gray")
        pylab.axhline(i*0.1,ls="dotted",color="gray")
        pylab.axhline(i*0.01,ls="dotted",color="gray")

    for shg in hg[chord]: 
        ax.plot([float(shg),float(shg)+1],[0.01,0.01],lw=5,color="green")
        ax.plot([float(shg),float(shg)+1],[10.0,10.0],lw=5,color="red")
        

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    xr=np.array(xr)
    yr=np.array(yr)
    ind=np.argsort(xr)
    if len(yr)==12:
        print('"'+chord+'":'+",".join(map(str,yr[ind])))
    else: 
        print("Invalid Number")
