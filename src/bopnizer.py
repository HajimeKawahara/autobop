#!/usr/bin/python
import numpy as np

def generate_bridges(n):
#bridges lenq: length of a bridge, sumq: sum of a bridge, rootq: 1st note of a bridge
    lenq=[]
    sumq=[]
    bridgearr=[]
    rootq=[]
    for i in range(1,2**n):
        arr=np.array([int(d) for d in str(bin(i))[2:]])*2-1
        sumq.append(np.sum(arr))
        lenq.append(len(arr))
        bridgearr.append(arr)
        rootq.append(arr[0])

        arrm=np.copy(arr)
        arrm[0]=-1
        sumq.append(np.sum(arrm))
        lenq.append(len(arrm))
        bridgearr.append(arrm)
        rootq.append(arrm[0])

    bridgearr=np.array(bridgearr)
    sumq=np.array(sumq)
    lenq=np.array(lenq)
    rootq=np.array(rootq)

    return bridgearr, sumq, lenq, rootq

def open_branch(refnote,ndb=2,nub=2,firstb=-1,bridgearr=None,sumq=None, lenq=None, rootq=None, n=4):
    if bridgearr is None:
        bridgearr, sumq, lenq, rootq=generate_bridges(n)

    if nub>0:
        x=np.random.choice(bridgearr[(lenq==nub)*(rootq==firstb)],1)
    if ndb>0:
        y=np.random.choice(bridgearr[(lenq==ndb)*(rootq==-firstb)],1)
    # cumsum recovers the relative note from the note difference 
    if nub>0 and ndb>0:
        branch=np.append(np.cumsum(x[0]),np.cumsum(y[0]))[::-1]+refnote
    elif nub>0:
        mask=(lenq==nub)*(rootq==firstb)
        branch=np.cumsum(x[0])[::-1]+refnote
    elif ndb>0:
        branch=np.cumsum(y[0])[::-1]+refnote
    else:
        branch=None
    return branch

def connected_branch(bridge,bridgearr=None,sumq=None, lenq=None, rootq=None, n=4):
    if bridgearr is None:
        bridgearr, sumq, lenq, rootq=generate_bridges(n)

    notediff=bridge[0]-bridge[1]
    mask=(sumq==notediff)
    weight=1/np.array(lenq[mask]+0.0)**2
    weight=weight/np.sum(weight)
    if len(weight)>0:
        branch=np.cumsum(np.random.choice(bridgearr[mask],1,p=weight)[0])+bridge[1]
        branch=branch[::-1]
    else:
        branch=None
    return branch

def extract_pairs(note, dur):
    melline=np.transpose(note)
    mask=(melline>0)
    nrpnote=np.transpose(np.array([np.append([None],melline[mask][:-1]),melline[mask]]))
    nrpdur=np.transpose(np.array([np.append([None],dur[mask[0]][:-1]),dur[mask[0]]]))
    interrest=[]
    tre=0
    for i in range(0,len(note)):
        if note[i][0]>0:
            interrest.append(tre)
            tre=0
        else:
            tre=tre+dur[i]

    return nrpnote, nrpdur, interrest

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Branching and Pairing')
    args = parser.parse_args()    

