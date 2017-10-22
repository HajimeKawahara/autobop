#!/usr/bin/python
import sys
import argparse
import numpy as np
#import sound_driver as sdr
#import pyaudio
#import wave
import matplotlib
import matplotlib.pyplot as plt
import pylab 
#import gcc
import brownianbridge as bb
#import mbop
#import chord_probability as cp
import gate_timer as gt
import makelily as ml
import maketakt as mt
import generate_cp as gcp
import rest
import pianist
import sheet
import rhythm_generator as rg
import story 
import sound_definition as sd
import transfer as tr
import gaussprocess as gp
import control as cl
from classAutobop import track
import velocgen as vg

def initialize(option):
    disp=False #for display
    tr.set_global(disp)    
    #------------------
    opt=option.split(",")
    inst=opt[0]
    sheet=opt[1]
    storydict=story.read_story_sheet(sheet)
    #control
    eachcontrol={}
    eachcontrol["storydict"]=storydict
    eachcontrol["onoff"]=True
    eachcontrol["iphrase"]=0
    eachcontrol["inst"]=inst
    eachcontrol["H"]=storydict[inst]["H"][0]
    eachcontrol["J"]=storydict[inst]["J"][0]
    eachcontrol["teff"]=storydict[inst]["teff"][0]
    if "off" in storydict[inst]: 
        eachcontrol["off"]=list(map(int,storydict[inst]["off"]))

    if "gauss-farey" in storydict[inst]:
        eachcontrol["gauss"]="gauss-farey"
        file=storydict[inst]["gauss-farey"][0]
        nf, amp, weight=gp.read_fareyfile(file)
        eachcontrol["gauss-farey-n"]=nf
        eachcontrol["gauss-farey-amp"]=amp
        eachcontrol["gauss-farey-weight"]=weight

    if "velocgen" in storydict[inst]:
        velfile=storydict[inst]["velocgen"][0]
        eachcontrol["velarr"]=np.loadtxt(velfile)

    return eachcontrol

def improvise(tseq, tkseq, ttime, part, control):
    tcur=control["tcur"][part]
    inst=control[part]["inst"]
    storydict=control[part]["storydict"]
    finger,celfile,noct,hlist,tlist,jlist,stab,blen,bpos,master,oct,teff_estab,len_estab,velstab,rhyfile=tr.load_inst(inst,storydict)
    trk = track(-5)
    #-------------------
    #chordlength=int(storydict["general"]["chordlenght"][0])
    #tdur = np.full( len(tseq), chordlength, dtype=int ) ## Tonic sequence
    #-------------------

    nbeat = len(bpos)            
    pstab=np.array(stab)
    pcel=gcp.read_cep_list(celfile)                

    nbeat=len(bpos)            
    lseq=len(tseq)
    if "next" not in control[part]:
        control[part]["next"]="play"
 
    # did not work
    #control[part]["next"]="play" if "next" not in control[part] else None

        
    ######## REST #######
    loc, width=storydict[inst]["timer_start_c"][0],storydict[inst]["timer_start_width"][0]
    if "off" in control[part]:
        for i in range(0,int(len(control[part]["off"])/2)):
            if tcur > control[part]["off"][2*i] and tcur < control[part]["off"][2*i+1]:
#                print "REST-",tcur,  control[part]["off"]
                control[part]["next"] = "rest"
                loc, width=storydict[inst]["timer_stop_c"][0],storydict[inst]["timer_stop_width"][0]

    if control[part]["next"] == "rest":
        numrest=rest.get_numrest()
        restdur=rest.get_restdur() #- duration of the rest 
        iseq=np.digitize([tcur],ttime)[0]  #-        
        jrest=max(0,int(np.random.logistic(loc,width))) #logistic distribution
        tcur=tcur+restdur #-
        seq=[np.array(numrest*np.ones(finger,dtype=int))]
        mn=mt.midinote.seq2mn(np.array(seq),oct)
        dur=[restdur*jrest]

        control[part]["next"] = "play"        
        if part=="melody": 
            print("#####",part," REST length=", np.sum(dur))

#        return mn, dur, control
        vel=np.ones(np.shape(mn),dtype=int)*80
        trk.extend( mn, dur, vel )
        return trk, control

    #-------------------------------------------------
    #generate mRNA 
    iphrase=control[part]["iphrase"] #tmp
    var=0.3 #tmp
    #---------    
    imodt=np.mod(iphrase,len(tlist))
    teff=tlist[imodt] 
    imodj=np.mod(iphrase,len(jlist))
    J=jlist[imodj] 
    imodh=np.mod(iphrase,len(hlist))
    H=hlist[imodh] 
    #---------
    #interactive mode (now debugging)
    if False:
        print("Interactive mode ON (under debugging)")
        hcurlist=cl.extract_control(control,"H")
        H=(H+np.random.choice(hcurlist))/2.0
        jcurlist=cl.extract_control(control,"J")
        J=(J+np.random.choice(jcurlist))/2.0

#    tcurlist=cl.extract_control(control,"teff")
#    teff=np.random.choice([teff,np.random.choice(tcurlist)])

    control[part]["H"]=H
    control[part]["J"]=J
    control[part]["teff"]=teff
    print(part,"H=",H,"J=",J,"teff",teff)
    #---------
    beta=2.0**(2.0*H)
    x0,y0,x1,y1=0.0,0.0,1.0,0.0
    mRNAsingle=[]
    bb.brownianbridge_mRNA(x0,y0,x1,y1,var, beta, mRNAsingle)

    mRNA=np.array(mRNAsingle).transpose()[0]
    shiftarray=np.array([0.0,0.1,-0.1,0.2,-0.2,0.3,-0.3,0.4,-0.4,0.5,-0.5])*10.0    

    if "gauss" in control[part]:
        if control[part]["gauss"]=="gauss-farey":
            ngpfarey=control[part]["gauss-farey-n"]
            gpampfarey=control[part]["gauss-farey-amp"]
            gpwfarey=control[part]["gauss-farey-weight"]
            gaus=gp.farey_gp(ngpfarey,gpampfarey,gpwfarey)[0:len(mRNA)]            
        else:
            gaus=gp.simple_gp()[0:len(mRNA)]
    else:        
        gaus=np.zeros(len(mRNA))

    #print "sig brown =",np.std(np.array(mRNAsingle).transpose()[1])
#    gausfac=10.6 #DEBUGGINH
    gausfac=0.1 #DEBUGGINH
    for ifinger in range(0,finger):
        mRNA=np.vstack((mRNA,np.array(mRNAsingle).transpose()[1]+gausfac*gaus+shiftarray[ifinger]))            

        # only quasi-periodic
#        if part == "melody":
#            mRNA=np.vstack((mRNA,gaus+shiftarray[ifinger]))            
#        else:
#            mRNA=np.vstack((mRNA,np.array(mRNAsingle).transpose()[1]+gaus+shiftarray[ifinger]))            

    mRNA=mRNA.transpose()
    #-------------------------------------------------
    #save mRNA
    if True:
        np.savetxt(str(part,"utf-8")+str(iphrase)+".mrna",mRNA)
    #-------------------------------------------------
    #transfering 
    iseq=np.digitize([tcur],ttime)[0]  #-
    if iseq < lseq:        

        if "velarr" in control[part]:
            velarr=control[part]["velarr"]
        else:
            velarr=None
        mn, dur, vel = tr.RNAtransfer(mRNA,tcur,tseq,tkseq,ttime,noct,teff,J,pcel,pstab,bpos,blen,finger, nbeat, lseq,teff_estab,len_estab,oct,velarr,velstab,rhyfile)

        control[part]["iphrase"]=iphrase+1

        if storydict[inst]["timer_start_c"][0]==0.0: # for non-rest instruments
            control[part]["next"]="play"
        else:
            control[part]["next"]="rest"
            if part=="melody":
                print("#####",part," PLAY length=",np.sum(dur)) 

        trk.extend( mn, dur, vel )
        return trk, control
    else: 
        trk.extend( mn, dur, vel )
        return trk, control
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Brownian Bop Generator')
    parser.add_argument('-f', nargs=1, help='story sheet', type=str)
    parser.add_argument('-o', nargs=1, default=["out"], help='output',type=str)    
    parser.add_argument('-display', help='display phrases', action='store_true')
    parser.add_argument('-sheet', nargs=1, default=['default.abs'], help='file for chord changes', type=str)
    args = parser.parse_args()    

    if args.display:
        disp=True
        ixp=0
    else:
        disp=False
    tr.set_global(disp)

    storydict=story.read_story_sheet(args.f[0])
    ##### general settings #####
    bpm=int(storydict["general"]["bpm"][0])
    chordlength=int(storydict["general"]["chordlenght"][0])
    nsamp=int(storydict["general"]["n"][0])
    instlist=storydict["general"]["inst"]

    tseq, tkseq = sheet.read(args.sheet[0])
    tseq = np.tile(tseq, (nsamp,1))
#    tdur = np.full( len(tseq), 960, dtype=int ) ## Tonic sequence
    tkseq = np.tile(tkseq, nsamp)
    tdur = np.full( len(tseq), chordlength, dtype=int ) ## Tonic sequence
    
    
    #default bass line
    bseq=np.copy(tseq)
    bdur = np.full( len(bseq), chordlength, dtype=int ) ##
    bmn=mt.midinote.seq2mn(np.array(bseq),-3)

    #default pianist
    cseq, cdur = pianist.gen_cseq(tseq, tkseq)
    cmn=mt.midinote.seq2mn(np.array(cseq),-2)

    #dna
    dna=[]
    tdna=[]

    ##### generate melody #####
    g=mt.manual_open_taktfile(args.o[0]+".takt", bpm)
    taktlist=""
    for iinst in range(0,len(instlist)):
        inst=instlist[iinst]
        print("######",inst,"######")
        finger,celfile,noct,hlist,tlist,jlist,stab,blen,bpos,master,oct=tr.load_inst(inst,storydict)
        nbeat = len(bpos)            
        pstab=np.array(stab)
        pcel=gcp.read_cep_list(celfile)                
        plistmulti=[]        
        for teff in tlist:
            peach=[]
            for ibeat in range(0,nbeat):
                peach.append(gcp.pcel2prelative(pcel,teff*pstab[ibeat]))                
                plistmulti.append(peach)

        seq, dur, nphrase, dna, tdna=tr.All_RNAtransfer(tseq,tdur,tkseq,nsamp,noct,plistmulti,hlist,jlist,bpos,blen,finger,dna,tdna,master)

        mn=mt.midinote.seq2mn(np.array(seq),oct)
        taktlist=mt.manual_add_taktfile(g,iinst+1,inst,mn,dur,taktlist,tie=False)

    taktlist=mt.manual_add_drumtaktfile(g, dur, taktlist, len(instlist)+1)
    mt.manual_close_taktfile(g, taktlist)

    #takt output
    #mt.auto_taktfile(args.o[0]+".takt",mseq, mdur, bseq, bdur, cseq, cdur, bpm)

    #lilypond output
    #        ml.auto_lilyfile(args.o[0].replace(".wav","")+".ly",mseq,tseq,tkseq,noct,ndivq,ndivchord,title="brownian bop")

