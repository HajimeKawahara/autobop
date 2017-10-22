#!/usr/bin/python
import sys
import argparse
import numpy as np
import rest
import midinote
from classAutobop import track


def get_taktnote():
    note=["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
    invdict={"Db":"C#","Eb":"D#","Gb":"F#","Ab":"G#","Bb":"A#","C#":"Db","D#":"Eb","F#":"Gb","G#":"Ab","A#":"Bb"}
    
    return note, invdict


def make_taktnote():
    note, invdict=get_taktnote()
    taktnote=np.empty(0)

    for i in range(-1, 10):
        addnote=np.core.defchararray.add(note, str(i))
        taktnote=np.r_[taktnote, addnote]

    taktnote[128]='R'

    return taktnote


def convert_seq_taktseq(seq, dur, taktnote):
    nd_seq=np.empty(0)
    
    for s in seq:
        if (s < 0).any():
            s[s<0]=128
        scseq='['+" ".join(taktnote[s])+']'
        nd_seq=np.append(nd_seq, scseq)

    str_dur = np.array(dur, dtype=str)
    takt_dur = np.core.defchararray.add(str_dur, 'u')

    combine = np.core.defchararray.add(takt_dur, nd_seq)

    return combine

def tie(mseq):
    pm = mseq[0]
    for i in range(1, len(mseq)):
        if pm == mseq[i]:
            mseq[i]='~'
        else:
            pm=mseq[i]
        
    return mseq

def manual_open_taktfile(file, bpm):
    g=open(file,"w")
    g.writelines('tempo('+str(bpm)+')\n\n')

    return g

def manual_add_taktfile(g,iinstin,name,seq,dur,list,tie=False):
    taktnote=make_taktnote()
    iinst=str(iinstin+1)
    list=list+name+'1 '
    taktseq=convert_seq_taktseq(seq, dur, taktnote)

    if tie:
        taktseq=tie(taktseq)
        
    tseq=" ".join(taktseq)        
    g.writelines('newtrack('+name+') { ch='+iinst+' tk='+iinst+' }\n')
    g.writelines('var '+name+'1 = { '+name+': { '+tseq+'} }\n\n')
    return list

def manual_close_taktfile(g,list):
    g.writelines('[ '+list+' ]\n')
    g.close()
    return 

def convert_track_takttrack(trk):
    taktnote=make_taktnote()
    nd_seq=np.empty(0)
    
    for n,v in zip(trk.note, trk.vel):
        if (n < 0).any():
            n[n<0]=128

        str_v = np.array(v, dtype=str)
        takt_v = np.core.defchararray.add("v=", str_v)
        takt_v = np.core.defchararray.add(takt_v, " ")

        vn = np.core.defchararray.add(takt_v, taktnote[n])

        str_note='['+" ".join(vn)+']'
        nd_seq=np.append(nd_seq,str_note)

    str_dur = np.array(trk.dur, dtype=str)
    takt_dur = np.core.defchararray.add(str_dur, 'u')

    combine = np.core.defchararray.add(takt_dur, nd_seq)

    return combine

def export( file, band, trkband, bpm ):
    nn="1"
    nnn=nn+" "
    g=open(file,"w")
    g.writelines('tempo('+str(bpm)+')\n\n')



    ch_list=['']*len(band)
    for part in band:
        partstr=str(part,"utf-8")
        takttrack = convert_track_takttrack( trkband[part] )
        tseq=" ".join(takttrack)        
        g.writelines('newtrack('+partstr+') { ch='+str(band[part]['ch'])+' tk='+str(band[part]['ch'])+' }\n')
        g.writelines('var '+partstr+nn+' = { '+partstr+': { '+tseq+'} }\n\n')

        ch_list[band[part]['ch']-1]=part

    bs=[]
    for i in band.keys():
        bs.append(str(i,"utf-8"))
    listx=nnn.join(list(bs))
    g.writelines('[ '+listx+nn+' ]\n')
    g.close()

    for i in range(0, len(ch_list)):
        print("ch",i+1,": "+str(ch_list[i],"utf-8"))

    return
        

if __name__ == "__main__":
    test=track()

    test.extend([[55,60],[55,48],[60,52]], [480,480,240],[[120,80],[120,60],[60,90]])

    comb = convert_track_takttrack( test )
    print(comb)
