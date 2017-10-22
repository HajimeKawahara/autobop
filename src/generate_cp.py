#!/usr/bin/python
import argparse
import numpy as np
#import sound_driver as sdr
#import pyaudio
#import wave
#import gcc
import sys
import matplotlib
import matplotlib.pyplot as plt
import pylab 
import sound_definition as sd

def read_cep_list(file):

    data=np.loadtxt(file,dtype={'names': ('tag','p'), 'formats': ('S8','S512')}, delimiter=':')
    pcel={}    
    for i in range(0,len(data)):        
        tag=str(data["tag"][i],"utf-8")
        vec=list(map(float,str(data["p"][i],"utf-8").split(",")))
        pcel[tag.replace('"','')]=vec

    return pcel

def pmb(e,T):
    return e*np.exp(-e/T)/T**2

def pcel2prelative(pcel,teff):
    prelative={}
    for chord in pcel:
        prelative[chord]=pmb(np.array(pcel[chord]),teff).tolist()    

    return prelative

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate Chord Probability')
    parser.add_argument('-f', nargs=1, required=True, help='chord probability list',type=str)
    parser.add_argument('-t', nargs='+', default=[0.1,0.5,1.0,2.0], help='temperature list',type=float)

    args = parser.parse_args()    
    file=args.f[0]
    pcel=read_cep_list(file)
    
    tlist=args.t

    fig = plt.figure()
    ax = fig.add_subplot(121)
    pylab.ylabel("Energy")
    pylab.xlabel("probability")

    plist=np.linspace(0,10,1000)
    for t in tlist:
        ax.plot(pmb(plist,t),plist)
        ax.annotate(str(t), xy=(pmb(t,t), t), xycoords='data', fontsize=12)
    ax = fig.add_subplot(122)
    pylab.ylabel("Energy")
    pylab.xlim(0.0,len(pcel))
    pylab.ylim(0.0,10.0)    
    i=0
    sg=sd.getsg()
    for chord in pcel:
        ax.annotate("C"+chord, xy=((i+0.5)/float(len(pcel)), 1.01), xycoords='axes fraction', fontsize=16,horizontalalignment="center")
        pylab.axvline(float(i),ls="dashed")
        if len(pcel[chord]) != 12:
            print("INVELID # of CELs for ", chord, "#=", len(pcel[chord]))            
        for j in range(0,len(pcel[chord])):
            energy = pcel[chord][j]
            ax.plot([i,i+1],[energy,energy],color="blue")
            ax.annotate(sg[j], xy=(j/float(13)+i, energy), xycoords='data', fontsize=8, color="gray")
        
        i=i+1
    plt.show()

    teff=0.2
    prelative=pcel2prelative(pcel,teff)
    print(prelative)
