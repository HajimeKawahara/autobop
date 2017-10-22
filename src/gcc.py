#!/usr/bin/python
import argparse
import numpy as np
import sound_driver as sd
import pyaudio
import wave
import sound_definition as sd
import sound_driver as sdr

def generalized_coltrane_change(n,n0,tk,nsamp=12):
    sg=sd.getsg()
    print("GCC: for","n_k=",n,"and","t_k=",tk)
    hg=sd.gethg()
    L=len(tk)
    M=len(n)
    k=0
    a=n0
    bseq=[[a]]
    cseq=[np.mod(np.array(hg[tk[0]])+a,12)]
    tkseq=[tk[0]]
    print(sg[a]+tk[0], end=' ')
    
    for i in range(0,nsamp):
        for j in range(0,L):        
            if j==L-1:  print("\n", end=' ')
            k=k+1
            a=np.mod(a+n[np.mod(k,M)],12)
            bseq.append([a])
            cseq.append(np.mod(np.array(hg[tk[np.mod(k,L)]])+a,12))
            tkseq.append(tk[np.mod(k,L)])
            print(sg[a]+tk[np.mod(k,L)], end=' ')
    return bseq,cseq,tkseq

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generalized Coltrane Changes')
    parser.add_argument('-nk', nargs="+", default=[5,3], help='nk',type=int)
    parser.add_argument('-tk', nargs="+", default=["","7"], help='tk',type=str)
    parser.add_argument('-key', nargs=1, default=[11], help='key',type=int)
    parser.add_argument('-o', nargs=1, default=["out.wav"], help='output wave file',type=str)    
    parser.add_argument('-n', nargs=1, default=[12], help='# of refrain',type=int)    
    parser.add_argument('-l', nargs=1, default=[0.2], help='length of a chord',type=float)    

    args = parser.parse_args()    

    btone=[[0.0,0.0]]    #tone for base
    ctone=[[1.0,np.pi*0.0],[0.2,np.pi/3.0],[0.05,np.pi/5.0],[0.01,np.pi/8.0]]  #tone for chord+

    FORMAT = pyaudio.paInt16
    VOLUME = 4096
    RATE = 44100

    #generalized coltrane changes
    bseq,cseq,tkseq=generalized_coltrane_change(args.nk,args.key[0],args.tk,nsamp=args.n[0])  

    bline=sdr.create_cline(bseq,btone,length=args.l[0],fA=110.5,vol=3) #base line
    cline=sdr.create_cline(cseq,ctone,length=args.l[0],fA=442) #chord line
    aline=(cline+bline)*VOLUME #chord+base and volume increase  

    #play a song
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,channels=1, rate=RATE, output=1)
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
