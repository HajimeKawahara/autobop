#!/usr/bin/python
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab 
import argparse
#import chord_probability as cp
import rest

def gate_stop(mnow,counter,finger=1,width=5.0,c=65.0):
    if c==np.inf:
        counter=counter+1
        return mnow, counter
        
    numrest=rest.get_numrest()
    stopp=1.0/(1+np.exp(-(1.0/width)*(float(counter)-c))) #stop probability (sigmoid type)
    j=np.random.random()
    if j < stopp:    
        mnow=numrest*np.ones(finger,dtype=int)
        counter=-1
    else:
        counter=counter+1
    return mnow, counter

