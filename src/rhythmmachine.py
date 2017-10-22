#!/usr/bin/python
import numpy as np
import argparse
import sound_definition as sd
import maketakt
import rest
import sheet
import rhythm_generator as rg
from classAutobop import track

def pattern(style):
    dr=sd.get_drumkit()
    R=rest.get_numrest()    

    pattern={'swing':[ [ dr['Kick'], R, R, R, R, R ],  # Right foot
                       [ R, R, R, R, R, R ],  # Left Hand
                       [ dr['Ride'], R, R, dr['Ride'], R, dr['Ride'] ], # Right Hand
                       [ R, R, R, dr['P-HH'], R, R ] ],  # Left foot
            '8beat': [ [ dr['Kick'], R, R, R, dr['Kick'], dr['Kick'], R, R ],
                       [ R, R, dr['Snare'], R, R, R, dr['Snare'], R ],
                       [ dr['C-HH'], dr['C-HH'], dr['C-HH'], dr['C-HH'], dr['C-HH'], dr['C-HH'], dr['C-HH'], dr['C-HH'] ],
                       [ R, R, R, R, R, R, R, R ] ],
             'bossa':[ [ dr['Kick'], R, R, dr['Kick'], dr['Kick'], R, R, dr['Kick'], dr['Kick'], R, R, dr['Kick'], dr['Kick'], R, R, dr['Kick'] ],
                       [ dr['Rim'], R, R, dr['Rim'], R, R, dr['Rim'], R, R, R, dr['Rim'], R, R, dr['Rim'], R, R ],
                       [ dr['C-HH'], dr['C-HH'], dr['C-HH'], dr['C-HH'], dr['C-HH'], dr['C-HH'], dr['C-HH'], dr['C-HH'], dr['C-HH'], dr['C-HH'], dr['C-HH'], dr['C-HH'], dr['C-HH'], dr['C-HH'], dr['C-HH'], dr['C-HH']],
                       [ R, R, R, R,  R, R, R, R,  R, R, R, R,  R, R, R, R]]
            }

    resolution={'swing':160, '8beat':240, 'bossa':240}

    dur=[ resolution[style] ] * len(pattern[style][0])
   
    return pattern[style], dur

def initialize(option):
    opt=option.split(",")

    #control
    eachcontrol={}
    eachcontrol["onoff"]=True
    eachcontrol["style"]=opt[0]

    return eachcontrol

def improvise(tseq, tkseq, ttime, part, control):
    trk = track(-5)
    option = control[part]["style"]
    beatseg, durseg = pattern(option)

    ## insert fill-in generator here ##

    seq = np.dstack(beatseg)[0]
    vel=np.ones(np.shape(seq),dtype=int)*80 #mod by HK
    trk.extend( seq, durseg, vel )

    return trk, control


if __name__ == "__main__":
    tseq, tkseq = sheet.read('default.abs')
    seq, dur = improvise(0, tseq, tkseq, 0, '8beat', 0, 0)

    taktlist=''
    file = maketakt.manual_open_taktfile('rhythmmachine.takt', 150)
    taktlist = maketakt.manual_add_taktfile(file, 0, 'drums', seq, dur, taktlist)
    maketakt.manual_close_taktfile(file, taktlist)
