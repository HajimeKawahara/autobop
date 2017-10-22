#!/usr/bin/python
import argparse
import numpy as np
import sys
import matplotlib
import matplotlib.pyplot as plt
import pylab 

def read_story_sheet(file):
    data=np.loadtxt(file,dtype={'names': ('inst','tag','p'), 'formats': ('S32','S32','S512')}, delimiter=':')
    story={}    
    eachstory={}
    currentinst=""
    for i in range(0,len(data)):                
        inst=str(data["inst"][i],"utf-8")
        tag=str(data["tag"][i],"utf-8")
        val=str(data["p"][i],"utf-8").split(",")
        if val[0].replace(".","").isdigit():
            vec=list(map(float,val))
        elif val[0] == "inf":
            vec=[np.inf]
        else:
            vec=val
        if currentinst == "": currentinst=inst
        if currentinst==inst :
            eachstory[tag]=vec
        else:
            story[currentinst]=eachstory
            currentinst=inst
            eachstory={}
            eachstory[tag]=vec
    story[currentinst]=eachstory
    
    return story

def clickst(event):
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
    parser.add_argument('-f', nargs=1, required=True, help='story sheet (.ss)',type=str)
    args = parser.parse_args()    

    story=read_story_sheet(args.f[0])
    print(story)
    sys.exit("--")


    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    
    
#    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
