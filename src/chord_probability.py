#!/usr/bin/python
import argparse
import numpy as np
#import sound_driver as sd
#import pyaudio
#import wave
#import gcc
import sys
import matplotlib
import matplotlib.pyplot as plt
import pylab 
#import sound_definition as sd

def sample_prelative():

    prelative={"":[1.0,0.01,1.0,0.01,1.5,0.05,0.01,1.5,0.01,0.5,0.01,0.01], \
                  "Maj":[1.0,0.01,0.7,0.01,1.5,0.02,0.01,1.5,0.01,0.5,0.01,0.6], \
                  "M":[1.0,0.01,1.0,0.01,1.5,0.5,0.01,1.5,0.01,0.5,0.01,0.01], \
                  "Maj7":[1.0,0.01,1.0,0.0,1.5,0.05,0.01,1.5,0.1,0.5,0.0,1.5], \
                  "7":[1.0,0.01,1.0,0.1,1.5,0.1,0.1,1.5,0.05,0.5,1.5,0.0], \
                  "7(A)":[0.5,0.01,1.0,0.1,1.5,1.0,0.01,1.5,0.05,0.5,1.5,0.0], \
                  "7(B)":[0.5,0.01,0.3,0.01,0.5,0.01,0.01,1.5,0.05,0.5,1.5,0.0], \
                  "m":[1.0,0.1,1.0,1.5,0.0,0.5,0.1,1.5,0.1,0.5,1.0,1.0], \
                  "m7":[1.0,0.1,1.0,1.5,0.0,0.5,0.1,1.5,0.1,0.5,1.0,0.5], \
                  "mb5":[1.0,0.1,1.0,1.5,0.0,0.5,1.5,0.1,0.1,0.5,1.0,0.1], \
                  "dim":[1.0,0.1,1.0,1.5,0.0,0.5,1.5,0.1,0.1,1.5,0.1,0.1]} 
    
    return prelative

def read_pchord_list(file):

    data=np.loadtxt(file,dtype={'names': ('tag','x'), 'formats': ('S8','S128')}, delimiter=':')
    prelative={}    
    for i in range(0,len(data)):        
        tag=data["tag"][i]
        vec=list(map(float,data["x"][i].split(",")))
        prelative[tag.replace('"','')]=vec

    return prelative

def get_pchord(prelative,b,tk,noct):

    pf=prelative[tk]
    pchord=[]
    for i in range(0,noct):    
        pchord=pchord+pf[-b[0]:]+pf[:-b[0]]

    return np.array(pchord)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Chord Probability')
    parser.add_argument('-f', nargs=1, required=True, help='chord probability list',type=str)
    args = parser.parse_args()    
    
    file=args.f[0]
    prelative=read_pchord_list(file)
    pchord=get_pchord(prelative,[1],"7",1)
    print(pchord)
