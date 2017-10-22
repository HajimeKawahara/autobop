#!/usr/bin/python
import argparse
import numpy as np
import sound_definition as sd
import pianist
import maketakt
import rest

numrest = rest.get_numrest()

def read(file):
    regexp = sd.get_chord_regexp()
    chords=np.fromregex(file, regexp, ('S4',2)) # [['root', 'type'],...]

    for i in range(0, len(chords)):
        if chords[i][0]=='%':
           chords[i]=chords[i-1]
    
    read=np.swapaxes(chords,0,1)

    bseq=[]
    ng=sd.getng()
    for i in read[0]:
        bseq.append([ng[str(i,"utf-8")]])
    tka=[]
    for tt in read[1]:
        tka.append(str(tt,"utf-8"))
    tkseq=np.char.strip(tka, " ")
    nd_bseq = np.array(bseq) #

    return nd_bseq, tkseq


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate Chord Probability')
    parser.add_argument('-f', nargs=1, default=['default.abs'], help='file with chord changes',type=str)

    args = parser.parse_args()    
    file=args.f[0]

    bseq, tkseq = read(file)
    
    cseq = pianist.gen_cseq(bseq, tkseq)

    mseq = np.full(len(bseq), 40, dtype=int)
    mseq = mseq[:,np.newaxis]

    mdur = np.full( len(mseq), 960, dtype=int )
    bdur = np.full( len(mseq), 960, dtype=int )

    maketakt.auto_taktfile("sheet.takt",mseq,mdur,bseq,bdur,cseq,180)


    
