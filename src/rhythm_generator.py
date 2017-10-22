#!/usr/bin/python
import sys
import argparse
import numpy as np
import rest
    ## dur > 0 -> sound (duration is + dur)
    ## dur < 0 -> rest (duration is - dur)
    ## dur == 0 -> ignored


def test_random_rythm():
    k=np.random.random()
    delay=-int(3.0*k)
    dur = [[delay,960*2+delay,],[delay,240+delay,-240-960], [delay,240+delay,-480], [delay,960+delay],[-240],[-480]]
    indar=list(range(0,len(dur)))
    probability = [0.25, 0.15, 0.25, 0.15, 0.05,0.15]
    probability = probability/np.sum(np.array(probability))
    ind = np.random.choice(indar, p=probability)
    
    return dur[ind]

def test_random_rythm2():
    k=np.random.random()
    delay=-int(3.0*k)
    dur = [[delay,960+delay,],[delay,240+delay,-240-480], [delay,240+delay,-480], [delay,960+delay],[-240],[-480]]
    indar=list(range(0,len(dur)))
    probability = [0.2, 0.1, 0.2, 0.15, 0.05,0.1]
    indar=list(range(0,len(dur)))
    probability = [0.2, 0.1, 0.2, 0.15, 0.15,0.2]
    probability = probability/np.sum(np.array(probability))
    ind = np.random.choice(indar, p=probability)
    
    return dur[ind]

def read_rhyfile(rhyfile):
    data=np.loadtxt(rhyfile,dtype={'names': ('tag','rhyarr','allow','count','weight'), 'formats': ('S32','S512','S512','S512','S512')}, delimiter=':')
    allarr=[]
    rhyarr=[]
    nmaxphrase=500
    nrhythm=len(data)
    timeweight=np.zeros([nmaxphrase,nrhythm])    

    for i in range(0,nrhythm):        
        val0=str(data["rhyarr"][i],"utf-8").split(",")
        vec0=list(map(int,val0))
        rhyarr.append(vec0)

        val=str(data["allow"][i],"utf-8").split(",")
        vec=list(map(int,val))
        allarr.append(vec)

        val3=str(data["count"][i],"utf-8").split(",")
        vec3=list(map(int,val3))

        val2=str(data["weight"][i],"utf-8").split(",")
        vec2=list(map(float,val2))
                    
        for k in range(0,len(vec3)):
            timeweight[vec3[k]:,i]=vec2[k]        
    
    beatentry=np.sort(np.unique(np.array(sum(allarr, []))))
    allow=[]
    for i in range(0,nrhythm):        
        alloweach=[]
        for j in beatentry: alloweach.append(j in allarr[i])
        allow.append(alloweach)

    return np.array(rhyarr),beatentry,np.array(allow),timeweight 

def rythmgen(counter,tcur,blen,rhyarr,beatentry,allow,timeweight):
    foward_allowance = 2
    k=np.random.random()
    delay=-int(2.0*k)
    restt=np.mod(tcur,blen)
    ipos=np.digitize([restt],beatentry)[0]-1
    wrhyarr=timeweight[counter,:]
    j=np.random.random()
    cumrhyarr=np.cumsum(wrhyarr[allow[:,ipos]])/np.sum(wrhyarr[allow[:,ipos]])
    irhy=np.digitize([j],cumrhyarr)[0]
    durlist=rhyarr[allow[:,ipos]][irhy]
#    if counter > 10: sys.exit()
    return delay,durlist[0]+delay,durlist[1]


def piano_comp():
    dur = np.array([[-160,320,-320,160], [-480, 320, 160], [-320,160,-320,160], [-800,160], [-960,0]])
    probability = [0.2, 0.1, 0.2, 0.45, 0.05]

    durlist = np.random.choice(dur, p=probability)

    return durlist


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Rhythm Generator')
    
    rhyarr,beatentry,allow,timeweight =read_rhyfile("test.rhy")
#    for i in range(0,10):
 #       w=np.random.random()
 #       r=np.random.random()
 #       rythmgen(int(100*w),int(1000*r),480)
