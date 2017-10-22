import matplotlib
import matplotlib.pyplot as plt
import pylab 
import numpy as np


def plot_midiseq(ax,test_notes, test_dur, color="red"):

    cumt=np.cumsum(np.append([0],test_dur))
    t=np.transpose([cumt[0:-1],cumt[1:]])
    pylab.ylabel("MIDI note")
    pylab.xlabel("time")
    for j in range(np.min(test_notes[test_notes>0]-1),np.max(test_notes)+2):
        ax.axhline(j,color="gray",alpha=0.2)
    for i in range(0,len(test_notes)):
        if test_notes[i]>0:        
        #ax.plot(t[i],[test_notes[i],test_notes[i]],".",color="red")
            ax.plot(t[i],[test_notes[i],test_notes[i]],color=color)
            ax.axvline(t[i][0],color="gray",alpha=0.1)
            ax.axvline(t[i][1],color="gray",alpha=0.1)

    

