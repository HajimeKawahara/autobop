#!/usr/bin/python
import argparse
import numpy as np
import sound_driver as sdr
import pyaudio
import wave
import gcc
import sys
import matplotlib
import matplotlib.pyplot as plt
import pylab 
import chord_probability as cp
import gate_timer as gt

def markovbop1(bseq,cseq,tkseq,nsamp,ndiv,noct,prelative):
    #ndov=8 : 8 buonpu
    if len(cseq) != len(bseq):
        sys.exit("Inconsistent lengths for base and chord sequences. ")
    else:
        lseq=len(cseq)
    mnow=0
    mseq=[]
    counter=1
    for iseq in range(0,lseq):
        for idiv in range(0, ndiv):
            if mnow<0:
                mnow,counter=mbop_gate_start(mnow,counter,bseq[iseq],tkseq[iseq],noct,prelative)
                
            else:
                counter=counter+1
                plocal=get_plocal(mnow,noct)
                pchord=cp.get_pchord(prelative,bseq[iseq],tkseq[iseq],noct)
                phg=plocal*pchord
                mnow=get_next_melody(phg)
                mnow,counter=gt.gate_stop(mnow,counter)

#            print mnow,
            mseq.append([mnow])

    return mseq


def get_plocal(mnow,noct,alpha=-1.0):
    plocal=np.zeros(noct*12)
    for j in range(-noct*12,noct*12):
        jd=mnow+j
        if jd>=0 and jd<noct*12 :
            if j==0:
                plocal[jd]=0.01
            else:
                plocal[jd]=plocal[jd]+np.abs(float(j))**alpha
    return np.array(plocal)

def mbop_gate_start(mnow,counter,bseqiseq,tkseqiseq,noct,prelative,width=3.0,c=15.0):
    stopp=1.0/(1+np.exp(-(float(-counter)-c)/width)) #stop probability (sigmoid type)
    j=np.random.random()
    if j < stopp:    
        phg=cp.get_pchord(prelative,bseqiseq,tkseqiseq,noct)
        mnow=get_next_melody(phg)[0]
        counter=1
    else:
        counter=counter-1

    return mnow, counter

def get_next_melody(phg):
    chg=np.cumsum(phg)
    n=np.sum(phg)
    j=np.random.random()
    mx=np.digitize([j*n],chg)
    return mx


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Markov bebop')
    parser.add_argument('-nk', nargs="+", default=[5,5,-3,5], help='nk',type=int)
    parser.add_argument('-tk', nargs="+", default=["m7","7(B)","mb5","7(A)"], help='tk',type=str)
    parser.add_argument('-key', nargs=1, default=[9], help='key',type=int)
    parser.add_argument('-o', nargs=1, default=["out.wav"], help='output wave file',type=str)    
    parser.add_argument('-n', nargs=1, default=[10], help='# of refrain',type=int)    
    parser.add_argument('-l', nargs=1, default=[0.12], help='length of division',type=float)    
    parser.add_argument('-ndiv', nargs=1, default=[8], help='# of sound for one chord',type=int)    
    parser.add_argument('-noct', nargs=1, default=[2], help='# of sound for one chord',type=int)    
    parser.add_argument('-f', nargs=1, help='chord probability list',type=str)

    args = parser.parse_args()    

    if args.f:
        prelative=cp.read_pchord_list(args.f[0])
    else:
        prelative=cp.sample_prelative()

    btone=[[0.0,0.0]]    #tone for base
    ctone=[[1.0,np.pi*0.0],[0.2,np.pi/3.0],[0.05,np.pi/5.0],[0.01,np.pi/8.0]]  #tone for chord+
    mtone=[[1.0,np.pi*0.3],[0.4,np.pi/9.0],[0.08,np.pi],[0.02,np.pi/2.0]]  #tone for Markov bop+

    FORMAT = pyaudio.paInt16
    VOLUME = 1500
    RATE = 44100
    nsamp=args.n[0]

    #generalized coltrane changes
    bseq,cseq,tkseq=gcc.generalized_coltrane_change(args.nk,args.key[0],args.tk,nsamp)  
    #Markov bop
    ndiv=args.ndiv[0]
    noct=args.noct[0]
    mseq=markovbop1(bseq,cseq,tkseq,nsamp,ndiv,noct,prelative=prelative)

    #play a song
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,channels=1, rate=RATE, output=1)
    bline=sdr.create_cline(bseq,btone,length=args.l[0]*ndiv,fA=110.5,vol=3) #base line
    cline=sdr.create_cline(cseq,ctone,length=args.l[0]*ndiv,fA=442.0,vol=1.4) #chord line
    mline=sdr.create_cline(mseq,mtone,length=args.l[0],fA=442.0,vol=1.2) #melody line

#    sys.exit("--")
    aline=(cline+bline+mline)*VOLUME #chord+base+melody and volume increase  
#    aline=(bline+mline)*VOLUME #chord+base+melody and volume increase  
    
    song=aline.astype(np.int16).tostring()
    stream.write(song)
    #SAVE AS WAV
    wf = wave.open(args.o[0],'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(song))
    wf.close()

    stream.close()
    p.terminate()


