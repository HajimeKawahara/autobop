#!/usr/bin/python
import sys
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab 
import brownianbridge as bb
import gate_timer as gt
import makelily as ml
import maketakt as mt
import generate_cp as gcp
import rest
import pianist
import sheet
import rhythm_generator as rg
import story 
import sound_definition as sd
import transfer as tr
import gaussprocess as gp
import control as cl
from classAutobop import track
from scipy import interpolate

def onclick(event):
    global nmidi
    global xr,yr,zr
    global dvvarr

    currmidi=int(event.ydata)
    dmidi=int(event.xdata)
    prvmidi=currmidi-dmidi
#    print "Previous MIDI=",prvmidi,"Current MIDI=",currmidi, "delta MIDI=",dmidi
    if dmidi > -128.0 and len(xr)==len(zr):
        xr.append(dmidi)
        yr.append(currmidi)
    elif dmidi > -128.0 and len(xr)>len(zr):
        xr[-1]=dmidi
        yr[-1]=currmidi
    elif len(xr)==len(zr)+1:
        zr.append(int(currmidi))
        ax.annotate(str(int(currmidi)), xy=(xr[-1],yr[-1]), xycoords='data', fontsize=12, color="white")
        

    if len(xr) > 9 and len(xr)==len(zr):
#        print xr,yr,zr
#        f=interpolate.interp2d(xr, yr, zr)        
        f=interpolate.SmoothBivariateSpline(xr, yr, zr, kx=2,ky=2) 
        for idmidi in range(-nmidi,nmidi):
            for jmidi in range(0,nmidi):
                if jmidi-idmidi >= 0 and jmidi-idmidi < 128:
                    dvvarr[jmidi,idmidi+nmidi]=max(0,min(127,int(f(float(idmidi),float(jmidi)))))
                    
        a=ax.imshow(dvvarr,extent=[-nmidi+1,nmidi-1,nmidi,0],interpolation="nearest",vmin=np.min(np.array(dvvarr)),vmax=np.max(np.array(dvvarr)))
        ax.colorbar(a)
        plt.gca().invert_yaxis()
            
    fig.canvas.draw()

def comp_dvvarr(velarr,nmidi):
    dvvarr=np.zeros([nmidi,nmidi*2+1],dtype=int)
    for imidi in range(0,nmidi):
        for jmidi in range(0,nmidi):
            idv=imidi-jmidi+nmidi
            dvvarr[imidi,idv]=velarr[imidi,jmidi]
    return dvvarr

def comp_velarr(dvvarr,nmidi):
    velarr=np.zeros([nmidi,nmidi],dtype=int)
    for imidi in range(0,nmidi):
        for idv in range(0,2*nmidi):
            jmidi=imidi-idv+nmidi
            if jmidi>=0 and jmidi<nmidi:
                velarr[imidi,jmidi]=dvvarr[imidi,idv]
    return velarr

def velapply(mn,velarr):
    velarr=np.array(velarr)    
    mn=np.array(mn)
    if len(mn)>0:
        start=velarr[mn[0][0],mn[0][0]]    
    else:
        start=80
    restnum=rest.get_numrest()      
    indr=(mn==restnum)
    ind=(mn!=restnum)

    mnind=mn[ind]
    if len(mnind)>0:
        vel=np.zeros(len(mn))
        velq=np.hstack([[start],velarr[[mnind[1:].transpose(),mnind[0:-1].transpose()]]])
        vel[ind.transpose()[0]]=velq
    else:
        vel=np.ones(len(mn))*80

    return list(map(int,vel))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='velocity generator')
    parser.add_argument('-o', nargs=1, default=["out"], help='output',type=str)    
    parser.add_argument('-f', nargs=1, help='output',type=str)    
    args = parser.parse_args()    
    nmidi=128
    vel_def=80

    if args.f:
        velarr=np.loadtxt(args.f[0])
#        mn=[[60],[45],[76],[58],[45],[65],[29],[40]]
#        vel=velapply(mn,velarr)
        dvvarr=comp_dvvarr(velarr,nmidi)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        a=ax.imshow(dvvarr,extent=[-nmidi+1,nmidi-1,nmidi,0],vmin=np.min(dvvarr),vmax=np.max(dvvarr))
        pylab.colorbar(a)
        pylab.ylabel("MIDI note")
        pylab.xlabel("Delta MIDI note (Current - Previous)")
        pylab.axvline(0.0,color="gray",ls="dotted")
        pylab.axvline(12.0,color="gray",ls="dotted")
        pylab.axvline(-12.0,color="gray",ls="dotted")
        pylab.axvline(24.0,color="gray",ls="dotted")
        pylab.axvline(-24.0,color="gray",ls="dotted")
        plt.gca().invert_yaxis()
        plt.show()
        sys.exit()

#    velarr=np.random.random([nmidi,nmidi])*vel_def
    velarr=np.ones([nmidi,nmidi],dtype=int)*vel_def
    dvvarr=comp_dvvarr(velarr,nmidi)

    xr=[]
    yr=[]
    zr=[]

    fig = plt.figure()
    ax = fig.add_subplot(121)
    a=ax.imshow(dvvarr,extent=[-nmidi+1,nmidi-1,nmidi,0],vmin=0,vmax=127)
    pylab.colorbar(a)
    pylab.ylabel("MIDI note")
    pylab.xlabel("Delta MIDI note (Current - Previous)")
    pylab.axvline(0.0,color="gray",ls="dotted")
    pylab.axvline(12.0,color="gray",ls="dotted")
    pylab.axvline(-12.0,color="gray",ls="dotted")
    pylab.axvline(24.0,color="gray",ls="dotted")
    pylab.axvline(-24.0,color="gray",ls="dotted")
    plt.gca().invert_yaxis()
    ax2 = fig.add_subplot(122)
    ax2.plot([-1128.0,-1000],[0.0,128.0])
    ax2.set_aspect(10.0/ax.get_data_ratio())
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

    velarr=comp_velarr(dvvarr,nmidi)
    np.savetxt(args.o[0]+".vel",np.array(velarr).astype(np.int8),fmt="%i")
