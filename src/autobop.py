#!/usr/bin/python
import argparse
import numpy as np
import sheet
import maketakt
import sys
import makelily
from classAutobop import track

def read_personnel(file):
    data=np.loadtxt(file,dtype={'names': ('part','module','option'), 'formats': ('S32','S32','S32')}, delimiter=':')

    band={}
    for datum, ch in zip(data, list(range(1,len(data)+1))):
        band[datum['part']] = {'module': __import__( str(datum['module'],"utf-8") ), 'option': datum['option'], 'ch': ch}
   
    return band

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Automated Be-bop Performer')
    parser.add_argument('-band', nargs=1, default=['house.band'], help='band', type=str)
    parser.add_argument('-sheet', nargs=1, default=['default.abs'], help='file for chord changes', type=str)
    parser.add_argument('-bpm', nargs=1, default=[240], help='bpm', type=int)
    parser.add_argument('-n', nargs=1, default=[3], help='# of repeat', type=int)
    parser.add_argument('-o', nargs=1, default=['out'], help='output',type=str)    
    parser.add_argument('-lily', nargs=1, help='export lily file. specify the part to export.',type=str)
    args = parser.parse_args()    

    band=read_personnel(args.band[0])
    tseq, tkseq = sheet.read(args.sheet[0])    
    nsamp = args.n[0]
    bpm = args.bpm[0]
    tkseq = np.tile(tkseq, nsamp)
    tseq = np.tile(tseq, (nsamp,1))

    #--------- Initialization ----------
    chordlength = 960 #!!!!! temporary

    tdur = np.full( len(tseq), chordlength, dtype=int ) ## Tonic sequence
    ttime=np.cumsum(tdur) #- time for tkseq and tseq

    nplayer=len(band)    

    control={} #current atmosphere
    trkband={}

    eachtcur={}

    for part in list(band.keys()):
        player = band[part]
        trkband[part]=track()
        #set control 
        eachtcur[part]=0
        control[part]=player['module'].initialize(str(player["option"],"utf-8"))
    control["tcur"]=eachtcur

    #--- main loop ---
    while min( control['tcur'].values() ) < ttime[-1]:
        part = min( list(control['tcur'].items()), key=lambda x:x[1])[0]
        player=band[part]

        print("now",part, "playing", "t(part)=",control["tcur"][part])         
        trk, control = player['module'].improvise(tseq, tkseq, ttime, part, control)
        trkband[part].join(trk)
        control['tcur'][part] = np.sum(trkband[part].dur)

    #--- truncate excess ---
    for part in trkband:
        trkband[part].truncate( ttime[-1] )

#--- output ----
    maketakt.export( args.o[0]+".takt", band, trkband, bpm )

    if args.lily:
        makelily.export( args.o[0]+".ly", trkband[args.lily[0]] )
