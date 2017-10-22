#!/usr/bin/python
import numpy as np
import pyaudio
import sys
import matplotlib
import matplotlib.pyplot as plt
import pylab 
import rest

def harmony(freq, length, rate, tone):
    samp=(2*np.pi)*freq/rate
    ti=np.arange(0,rate*length,1)
    harm=np.sum(np.sin((samp*np.tile(ti,(len(samp),1)).T).T),axis=0)

    for i in range(0,len(tone)):
        harm=harm+tone[i][0]*np.sum(np.sin(((2**i)*samp*np.tile(ti,(len(samp),1)).T).T+tone[i][1]),axis=0)

    #edge damp
    je=int(rate*0.002)
    tj=np.array(list(range(0,len(harm[-je:]))))
    damp=10.0
    if False:
        fig=plt.figure()
        ax=fig.add_subplot(111)
        tall=np.array(list(range(0,len(harm))))
        ax.plot(tall,harm)
        ax.plot(tj,np.exp(-tj*tj/float(2*je*je/damp)))
        ax.plot(tall[-je:],harm[-je:]*np.exp(-tj*tj/float(2*je*je/damp)))
        ax.plot(tall[0:je],harm[0:je]*np.exp(-(tj-je)*(tj-je)/float(2*je*je/damp)))
        plt.show()
        sys.exit("--")

    harm[0:je]=harm[0:je]*np.exp(-(tj-je)*(tj-je)/float(2*je*je/damp))
    harm[-je:]=harm[-je:]*np.exp(-tj*tj/float(2*je*je/damp))

    return  harm

def notone(length, rate): 
    ti=np.arange(0,rate*length,1)
    
    return np.zeros(len(ti))

def create_cline(cseq,tone,fA=440, length=0.2, rate=44100,vol=0.5):
    f0=fA*(2**(-9/12.0)) # C as a fiducial frequiency    
    cline=[]
    for iseq in range(0,len(cseq)):
        if cseq[iseq][0]<0:
            cline = np.hstack([cline,notone(length, rate)])        
        else:
            chordiseq=f0*2**(np.array(cseq[iseq])/12.0)
            cline = np.hstack([cline,harmony(chordiseq, length, rate,tone)])

    cline = cline*vol

    if False:
        fig=plt.figure()
        ax=fig.add_subplot(111)
        ti=np.array(list(range(0,len(cline))))
        ax.plot(ti,cline)
        plt.show()
        sys.exit("--")

    return cline

def create_continuous_cline(cseq,tone,fA=440, length=0.2, rate=44100,vol=0.5):
    f0=fA*(2**(-9/12.0)) # C as a fiducial frequiency    
    cline=[]
    cprev=cseq[0][0]
    lenunit=len(np.hstack([cline,notone(length, rate)]))
    istack=1
    for iseq in range(1,len(cseq)):
        if cprev<0:
            cline = np.hstack([cline,notone(length, rate)])        
            istack=1
        elif cprev==cseq[iseq][0]:
            istack=istack+1
        else:
            chordiseq=f0*2**(np.array([cprev])/12.0)
            iend=istack*lenunit
            newharm=harmony(chordiseq, istack*length, rate,tone)[0:iend]
#            if istack > 1:
#                print istack,len(harmony(chordiseq, istack*length, rate,tone)),iend,"-", istack*len(harmony(chordiseq,length, rate,tone))
            cline = np.hstack([cline,newharm])
            istack=1
        cprev=cseq[iseq][0]

    #last tone
    if cprev<0:
        cline = np.hstack([cline,notone(length, rate)])        
    else:
        chordiseq=f0*2**(np.array([cprev])/12.0)
        cline = np.hstack([cline,harmony(chordiseq, istack*length, rate,tone)])

    cline = cline*vol

    if False:
        fig=plt.figure()
        ax=fig.add_subplot(111)
        ti=np.array(list(range(0,len(cline))))
        ax.plot(ti,cline)
        plt.show()
        sys.exit("--")

    return cline


if __name__ == "__main__":
    numrest=rest.get_numrest()

    tone=[[0.0,0.1],[0.1,np.pi/3.0],[0.05,np.pi/5.0],[0.0,np.pi/8.0]]    
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,channels=1, rate=44100, output=1)
    cseq=[[0],[4,7],[3,4],[numrest],[3,8],[2,6],[0],[4,7],[3,4],[numrest],[3,8],[2,6],[0],[4,7],[3,4],[numrest],[3,8],[2,6]]
    cline=create_cline(cseq,tone)
    stream.write(cline.astype(np.float32).tostring())
    stream.close()
    p.terminate()
