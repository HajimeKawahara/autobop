#!/usr/bin/python
import sys
import argparse
import numpy as np
import rest

def seq2mn(seq, ioct=0):
    #if you wanna change octave, specify ioct.
    numrest=rest.get_numrest()

    mn=np.array(seq)+60+12*ioct
    mn[seq<0]=numrest

    return mn

def sentence_midinotes(mn):
    if mn is None:
        return 
    # convert midinotes to a sentence (for debug)
    sgv=np.array(['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'])
    return " ".join(sgv[np.mod(mn,12)].tolist())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert seq to midi note')
    parser.add_argument('-H', nargs="+", default=[0.0], help='',type=float)    
    numrest=rest.get_numrest()

    bseq=np.array([[9], [2], [11], [4], [0], [0], [11], [4], [9], [2], [numrest], [4], [9], [2], [11], [4], [9], [2], [11], [4], [9]])
#    cseq=[[0,4,9], [4,7], [3,4], [numrest], [3,8,10], [2,6], [0], [0,4,7,11], [3,4], [numrest], [3,8], [2,6], [0], [4,7], [3,4], [numrest], [3,8], [2,6], [4,7], [2,4,9], [3,8]]
    cseq=np.array([[0,4,9], [4,7,1], [3,4,numrest], [numrest,numrest,numrest], [3,8,10], [2,6,numrest], [0,numrest,numrest], [0,4,7], [3,4,numrest], [numrest,numrest,numrest], [3,8,numrest], [2,6,numrest], [0,numrest,numrest], [4,7,numrest], [3,4,numrest], [numrest,numrest,numrest], [3,8,numrest], [2,6,numrest], [4,7,numrest], [2,4,9], [3,8,numrest]])

    bmn=seq2mn(bseq)
    print(bmn)

    cmn=seq2mn(cseq)
    print(cmn)
