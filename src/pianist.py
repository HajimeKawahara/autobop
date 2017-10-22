#!/usr/bin/python
import numpy as np
import argparse
import scale
import sound_definition as sd
#import cel_plot
import maketakt
import rest
import midinote
import sheet
import rhythm_generator as rg

ChordName=sd.gethg()
numrest=rest.get_numrest()

ChordRange = 4
G_distance=np.r_[np.linspace(0.7, 0.1, 7), np.zeros(12*(ChordRange-1)), np.linspace(0.2, 0.6, 5)]

G_center=np.logspace(0, -1, 12*ChordRange/2)
G_center=1-(G_center*G_center)
Gm_center=np.r_[G_center,G_center[::-1]]

def G_chord(b, tk):
    G_nextChord=np.zeros(12)
    n_tk = np.array(tk)

    G_nextChord[ n_tk[(n_tk>=0)] ] = 1.0
    G_nextChord=scale.transpose(G_nextChord, b)
    G_nextChord=np.tile(G_nextChord, ChordRange)

    return G_nextChord

def G_selectedTone(selectedTones):
    if selectedTones==[]:
        return np.ones(12*ChordRange)

    freeTone=np.ones(12)
    a_sTones=np.array(selectedTones, dtype=int)

    index=a_sTones % 12
    freeTone[index]=0.3
#    freeTone=extend(freeTone, ChordRange)
    freeTone=np.tile(freeTone, ChordRange)

    range_sTones=np.clip([a_sTones.min()-12, a_sTones.max()+12], 0, 12*ChordRange)
#    range_sTones=np.clip([a_sTones.min(), a_sTones.max()+12], 0, 12*ChordRange)
    mask=np.zeros(12*ChordRange)
    mask[range_sTones[0]:range_sTones[1]]=1
    freeTone=freeTone*mask
    
    return freeTone
    
def gen_next_chord(chord_present, t_next, tk_next):
    nextChord=[]
    index=np.arange(12*ChordRange)
    sg = np.array(['C','Db','D','Eb','E','F','F#','G','Ab','A','Bb','B'])

    Gm_nextChord=G_chord(t_next, ChordName[tk_next])

    for t in chord_present:
        Gm_distance = scale.transpose(G_distance, t)

        Gm_selectedTone=G_selectedTone(nextChord)

        Gm_nextTone = Gm_nextChord * Gm_distance * Gm_selectedTone * Gm_center
        
        nextTone = np.argmax(Gm_nextTone)
        nextChord.append(nextTone)

    nextChord.sort()

    return nextChord


def gen_cseq(tseq, tkseq):
    cseq=[]
    cdur=[]
    shift=24
    p_cseq=[0+shift,4+shift,7+shift,10+shift]
    shift_range = [ shift-8, shift]
    p_set = [[0, 0.1, 0.7, 0.2], [0.1, 0.3, 0.4, 0.2], [0.1, 0.6, 0.3, 0]]

    tdur = 0
    while tdur < len(tseq)*960:
        
        durlist = rg.piano_comp()
        for tmpdur in durlist:
            num_now = (tdur) / 960
            position_now = tdur % 960
            
            if position_now >= 720:
                num_now = num_now + 1
            
            if num_now >= len(tseq):
                num_now = num_now - 1

            n_cseq = gen_next_chord(p_cseq, tseq[num_now], tkseq[num_now])
            if n_cseq == p_cseq: # change position
                probability = p_set[ np.digitize([p_cseq[0]], shift_range) ]
                p_cseq[0] = p_cseq[0]+np.random.choice([-6,-3, 3, 6],p=probability)
                n_cseq = gen_next_chord(p_cseq, tseq[num_now], tkseq[num_now])

            if tmpdur > 0:
                cseq.append(n_cseq)
                cdur.append(tmpdur)
                tdur = tdur + tmpdur
            elif tmpdur < 0:
                cseq.append([numrest, numrest, numrest, numrest])
                cdur.append(-tmpdur)
                tdur = tdur - tmpdur
        p_cseq = list(n_cseq)

#    mn_cseq = midinote(cseq, -2)

    nd_cseq = np.array(cseq) # convert list to ndarray
    nd_cdur = np.array(cdur, dtype=int)

    return nd_cseq, nd_cdur

def initialize(option):
    #control
    eachcontrol={}
    eachcontrol["onoff"]=True
    return eachcontrol


def improvise(tseq, tkseq, ttime, part, control):
    chordlength = 960

    pos = int(tcur / chordlength)

    if 'prev_position' in list(control[part].keys()):
        prev_position = control[part]['prev_position']
    else:
        shift=24
        prev_position = [0+shift, 4+shift, 7+shift, 10+shift]

    new_position = np.array( gen_next_chord(prev_position, tseq[pos], tkseq[pos]), dtype=int)
   
    mn = midinote.seq2mn( new_position, -2 )
    seq = np.array([mn], dtype=int)
    dur = np.array([chordlength], dtype=int)
    
    return seq, dur, control


if __name__ == "__main__":
    tseq, tkseq = sheet.read('default.abs')
    cseq, cdur = gen_cseq(tseq, tkseq)

    tdur = np.full( len(tseq), 960, dtype=int)

    maketakt.auto_taktfile("pianist.takt",tseq, tdur, tseq, tdur, cseq, cdur, 180)
