#!/usr/bin/python
import sys
import argparse
import numpy as np
import rest
import midinote
from classAutobop import track


def get_lilynote():
    note=["c","des","d","es","e","f","ges","g","aes","a","bes","b"]
    invdict={"des":"cis","es":"dis","ges":"fis","aes":"gis","bes":"ais","cis":"des","dis":"es","fis":"ges","gis":"aes","ais":"bes"}
    
    return note, invdict


def make_lilynote():
    note, invdict=get_lilynote()
    octave=[",,,,",",,,",",,",",","","'","''","'''","''''","'''''","''''''"]
    lilynote=np.empty(0)

    for i in range(0, 11):
        addnote=np.core.defchararray.add(note, octave[i])
        lilynote=np.r_[lilynote, addnote]

    lilynote[128]='r'

    return lilynote

def convert_track_lilytrack(trk):
    nv_digit=[   108, 144,432,648, 864,1296,1512,1728]
    notevalue=["0","16","8","4","4.","2","2.","2..","1"]
    lilynote=make_lilynote()
    nd_seq=np.empty(0)
    nd_dur=np.empty(0)
    position=0
    
    for n,d in zip(trk.note[:,0], trk.dur):
        if (n < 0).any():
            n[n<0]=128
        str_note = lilynote[n]

        if position+d < 1920:
            nd_seq=np.append(nd_seq,str_note)
            idx=np.digitize([d], nv_digit)
            nd_dur=np.append(nd_dur,notevalue[idx])
            position = (position + d) % 1920
            continue

        while position + d >= 1920:
            trunc = 960 - position % 960
            position = (position + trunc) % 1920
            d = d - trunc

            nd_seq=np.append(nd_seq, str_note)
            idx=np.digitize([trunc], nv_digit)
            nd_dur=np.append(nd_dur,notevalue[idx])

        nd_seq=np.append(nd_seq, str_note)
        idx=np.digitize([d], nv_digit)
        nd_dur=np.append(nd_dur,notevalue[idx])
        position = (position + d) % 1920
        

    mask = (nd_dur!="0")
    combine = np.core.defchararray.add(nd_seq[mask], nd_dur[mask])

    return combine

def export( file, trk ):
    g=open(file,"w")

    lilytrack = convert_track_lilytrack( trk )
    tseq=" ".join(lilytrack)        
    g.writelines('\\absolute {\n')
    g.writelines(tseq+'}')
    g.close()

    return
        

if __name__ == "__main__":
    test=track()

    test.extend([[56,60],[54,48],[60,52]], [480,480,240],[[120,80],[120,60],[60,90]])

    comb = convert_track_lilytrack( test )
    print(comb)
