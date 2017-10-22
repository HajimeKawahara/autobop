#!/usr/bin/python
import sys
import argparse
import numpy as np
#import sound_driver as sdr
import matplotlib
import matplotlib.pyplot as plt
import pylab 
#import gcc
import brownianbridge as bb
#import mbop
import chord_probability as cp
import gate_timer as gt
#import makelily as ml
import maketakt as mt
import generate_cp as gcp
import rest
import pianist
import sheet
import rhythm_generator as rg
import story 
import sound_definition as sd
import brownianbridge as bb
import gaussprocess as gp
import disp_transfer as disptr
import velocgen as vg

def set_global(dispin):
    global var
    var=0.3 # variance of fractional brownian motion
    global disp
    disp=dispin
    global ixp
    ixp=0
    
def load_inst(inst,storydict):
    #global
    global rhythm_pattern, timer_stop_width, timer_stop_c, timer_start_width, timer_start_c, finger, noct
    rhythm_pattern=storydict[inst]["rhythm_pattern"][0]
    timer_stop_width=storydict[inst]["timer_stop_width"][0]
    timer_stop_c=storydict[inst]["timer_stop_c"][0]
    timer_start_width=storydict[inst]["timer_start_width"][0]
    timer_start_c=storydict[inst]["timer_start_c"][0]
    #local
    finger=int(storydict[inst]["finger"][0])
    hlist=storydict[inst]["H"]
    tlist=storydict[inst]["teff"]
    jlist=storydict[inst]["J"]
    celfile=storydict[inst]["celfile"][0]
    noct=int(storydict[inst]["noct"][0])
    stab=storydict[inst]["stab"]
    blen=int(storydict[inst]["blen"][0])
    bpos=list(map(int,storydict[inst]["beat"]))
    master=float(storydict[inst]["master"][0])
    oct=int(storydict[inst]["oct"][0])
    teff_estab=float(storydict[inst]["teff_estab"][0])  
    len_estab=int(storydict[inst]["len_estab"][0]) 
    velstab=list(map(int,storydict[inst]["velstab"])) 
    if rhythm_pattern=="rhythmgen":
        rhyfile=storydict[inst]["rhyfile"][0]
    else:
        rhyfile=None
    return finger,celfile,noct,hlist,tlist,jlist,stab,blen,bpos,master,oct,teff_estab,len_estab, velstab,rhyfile


def gate_start(mnow,counter,bseqiseq,tkseqiseq,noct,prelative,finger=1,width=3.0,c=15.0,force=False):
    stopp=1.0/(1+np.exp(-(float(-counter)-c)/width)) #stop probability (sigmoid type)
    j=np.random.random()
    if j < stopp or force==True:    
        phg=cp.get_pchord(prelative,bseqiseq,tkseqiseq,noct)
        chg=np.cumsum(phg)
        n=np.sum(phg)
        j=np.random.random(finger)
        mnow=np.digitize(j*n,chg)        
        counter=1
    else:
        counter=counter-1

    return mnow, counter



def bbselect_chord(y, dy, phg, mprev, tseqiseq=None,tkseqiseq=None):        
    global disp
    global ixp
    global axp
    numrest=rest.get_numrest()
    endmask=(mprev<0) 
    lennorm=np.sum(phg)

    if np.prod(endmask)==1: # all elements of mnow < 0
        #
        yd=y+0.5
        mask=(yd<0)
        yd[mask]=-yd[mask]
        mask=(yd>1.0)
        yd[mask]=1.0-(yd[mask]-1.0)
        chg=np.cumsum(phg)
        sys.exit("Stop at a place in debugging. #db01")
        mnote=np.digitize(yd,chg)
        #print "A", mprev, "->", mnote
    else:
        #diminish previous notes
        nfac=0.1     
        previous_notes=mprev[list(range(0,finger))]
        mask=(previous_notes>0)
        phg[previous_notes[mask]]=nfac*phg[previous_notes[mask]]
#        phg=phg/np.sum(phg)*lennorm
        dupfac_same=0.1
        dupfac_octsame=0.01

        choff=[]
        mnote=[]
        ind=np.array(list(range(0,noct*12)))        
        for ifinger in range(0,finger):
            phg=phg/np.sum(phg)*lennorm
            chg=np.cumsum(phg)
            choff.append(chg[mprev[ifinger]])
            msel=0
            dl=0.0
            ic=0
            #print choff[ifinger]+dy[ifinger],"(",
            while msel >= noct*12 or msel <= 0 :
                ic=ic+1
                msel=np.digitize([choff[ifinger]+dy[ifinger]+dl],chg)[0]
                if msel>=noct*12:  
                    dl=dl-abs(10*dy[ifinger]/(ic*2))
                    #print ">",msel,
                elif msel<=0:
                    dl=dl+abs(10*dy[ifinger]/(ic*2))
                    #print ">",msel,
            #print msel,")"

            mnote.append(msel)
            #diminish duplicateed tones
#            print "msel:",msel,noct*12
            phg[msel]=dupfac_same*phg[msel]
                
            if msel-2>=0:
                phg[msel-1]=dupfac_same*phg[msel-1]
                phg[msel-2]=dupfac_same*phg[msel-2]
            if msel+2<noct*12:
                phg[msel+1]=dupfac_same*phg[msel+1]
                phg[msel+2]=dupfac_same*phg[msel+2]

            dupmask=(np.mod(ind,12)==np.mod(msel,12))
            phg[dupmask]=dupfac_octsame*phg[dupmask]
            if disp:
                ixp=ixp+1
                disptr.disp_scales(ixp,ifinger,y,dy,mnote,chg,choff,tseqiseq,tkseqiseq)

                
        choff=np.array(choff)
        mnote=np.array(mnote)

    return mnote

def RNArest():
    numrest=rest.get_numrest()
    restdur=rest.get_restdur() #- duration of the rest 


def RNAtransfer(mRNA,tcur,tseq,tkseq,ttime,noct,teff,J,pcel,pstab,bpos,blen,finger,nbeat,lseq,teff_estab,len_estab,oct,velarr,velstab,rhyfile,mnow_start=0):
    #ndov=8 : 8 buonpu
    global axp
    global timer_start_width
    global timer_start_c

    if disp==True:
        ixp=0
        disptr.disp_start()
        print("DISPLAY START")

    if rhythm_pattern == "rhythmgen":
        print(rhythm_pattern)
        print(rhyfile)
        rhyarr,beatentry,allow,timeweight=rg.read_rhyfile(rhyfile)

    numrest=rest.get_numrest()
    restdur=rest.get_restdur() #- duration of the rest 

    seq=[]
    dur=[]
    vel=[]

    prelmul=[]
    for ibeat in range(0,nbeat):
        prelmul.append(gcp.pcel2prelative(pcel,teff*pstab[ibeat]))                

    #test of end stab
    prelmul.append(gcp.pcel2prelative(pcel,teff_estab))                
    velstab=velstab+[15]

#-------- initialize ---------
    iseq=np.digitize([tcur],ttime)[0]  #-
    mnow=mnow_start
    counter=0
    ibeat=0    
    mnow,counter=gate_start(mnow,counter,tseq[iseq],tkseq[iseq],noct,prelmul[ibeat],finger,timer_start_width,timer_start_c,force=True)

    endcounter=max(0,int(np.random.logistic(timer_stop_c,timer_stop_width))) #logistic distribution
#------------------------
    
    for counter in range(0,len(mRNA)-1):
        y=mRNA[counter+1][1:finger+1]
        dy=(mRNA[counter+1][1:finger+1]-mRNA[counter][1:finger+1])
                #mRNA[counter]                
                #--------ura-haku---------
        iseqcand=np.digitize([tcur,tcur+240],ttime)
        prob=[0.5,0.5]
        iseq=np.random.choice(iseqcand,p=prob)
                 #x------------------------
#                print "iseq=",iseq,"/",lseq
        if iseq<lseq:
            deltat=np.mod(tcur,blen)   
            ibeat=np.argmin(np.abs(bpos-deltat))
            if ibeat==nbeat: ibeat=0
            #test endstab
            if  counter >= endcounter - len_estab: ibeat = nbeat
            phg=cp.get_pchord(prelmul[ibeat],tseq[iseq],tkseq[iseq],noct)
            phg=phg/np.sum(phg)/J*noct
#                    dy=dy+np.array([0.0,0.1,0.2,0.3])[0:finger]
        if disp:
            mnow=bbselect_chord(y, dy, phg, mnow,tseq[iseq],tkseq[iseq]) 
        else:
            mnow=bbselect_chord(y, dy, phg, mnow)                    
#            print ibeat,"/",nbeat,mnow,  np.argmax(phg), np.max(phg)

        counter=counter+1
        if counter > endcounter: 
#            print counter
            counter=-1
        
#        mnow,counter=gt.gate_stop(mnow,counter,finger,timer_stop_width,timer_stop_c)            
        if counter>0:
            if rhythm_pattern == "rhythmgen":
                durlist=rg.rythmgen(counter,tcur,blen,rhyarr,beatentry,allow,timeweight)
            elif rhythm_pattern == "4beat":
                durlist=[480]
            elif rhythm_pattern == "2beat":
                durlist=[960]
            elif  rhythm_pattern == "test":
                durlist=rg.test_random_rythm2()
            else:
                durlist=[240]

            for tmpdur in durlist:
                if tmpdur > 0:
                    seq.append(mnow)
                    dur.append(tmpdur)
                    tcur=tcur+tmpdur
                    vel.append(velstab[ibeat])
                elif tmpdur < 0:
                    seq.append(numrest*np.ones(finger,dtype=int))
                    dur.append(-tmpdur)
                    tcur=tcur-tmpdur
                    vel.append(velstab[ibeat])

#        print "generating",counter,"/",len(mRNA)-1,mnow

        if counter < 0:
            break

    if disp==True:
        plt.show()            

    mn=mt.midinote.seq2mn(np.array(seq),oct)
    if velarr is not None:
        vel=np.array(vel)+vg.velapply(mn,velarr)
    else:
        vel=np.array(vel)+80
    
    mask=(vel>127)
    vel[mask]=127
    mask=(vel<0)
    vel[mask]=0

    if finger > 1:
        velorg=np.copy(vel)
        for ifinger in range(0,finger-1):
            vel=np.vstack([vel,velorg])
        vel=vel.transpose()

    return np.array(mn), np.array(dur), np.array(vel)
    


def All_RNAtransfer(tseq,tdur,tkseq,nsamp,noct,plistmulti,hlist,jlist,bpos,blen,finger,dna=[],tdna=[],master=0.0):
    #ndov=8 : 8 buonpu
    global axp
    global timer_start_width
    global timer_start_c

    numrest=rest.get_numrest()
    restdur=rest.get_restdur() #- duration of the rest 
    ttime=np.cumsum(tdur) #- time for tkseq and tseq
    nbeat=len(bpos)            

    if len(tkseq) != len(tseq):
        print("len(tkseq)=",len(tkseq),"len(tseq)=",len(tseq))
        sys.exit("Inconsistent lengths for tonic and chord sequences.")
    else:
        lseq=len(tseq)

    mnow=0
    seq=[]
    dur=[]
    counter=0
    iseq=-1
    iphrase=0
    tcur=0 #- current time
    ibeat=0    
    mnow,counter=gate_start(0,counter,tseq[iseq],tkseq[iseq],noct,plistmulti[0][ibeat],finger,timer_start_width,timer_start_c,force=True)
    print("start=",mnow)
    while True:

        if counter<0:
            iseq=np.digitize([tcur],ttime)[0]  #-
            if iseq<lseq:
                ibeat=0
                mnow,counter=gate_start(mnow,counter,tseq[iseq],tkseq[iseq],noct,plistmulti[0][ibeat],finger,timer_start_width,timer_start_c)
                ## caution this mnow is not appended in mseq. just for computing next mnow

            seq.append(numrest*np.ones(finger,dtype=int))
            dur.append(restdur) #-
            tcur=tcur+restdur #-
        else:
            ##### generate mRNA #####
            imod=np.mod(iphrase,len(hlist))
            H=hlist[imod] 
            beta=2.0**(2.0*H)
            x0=0.0
            y0=0.0
            x1=1.0
            y1=0.0
            mRNAsingle=[]
            bb.brownianbridge_mRNA(x0,y0,x1,y1,var, beta, mRNAsingle)
            mRNA=np.array(mRNAsingle).transpose()[0]
            shiftarray=np.array([0.0,0.1,-0.1,0.2,-0.2,0.3,-0.3,0.4,-0.4,0.5,-0.5])*10.0
            
            #test
            gaus=gp.simple_gp()[0:len(mRNA)]
            print("sig gp =",np.std(gaus), end=' ')
            print("sig brown =",np.std(np.array(mRNAsingle).transpose()[1]))

            for ifinger in range(0,finger):       
                mRNA=np.vstack((mRNA,np.array(mRNAsingle).transpose()[1]+gaus+shiftarray[ifinger]))             
            mRNA=mRNA.transpose()
            #### transfer ####
            print("Transfer RNA iphrase=", iphrase, "H=",H, end=' ')
 
            if disp==True:
                ixp=0
                disptr.disp_start()
                print("DISPLAY START")
#                pylab.title("#"+str(iphrase)+", H="+str(H))

            for counter in range(0,len(mRNA)-1):
                y=mRNA[counter+1][1:finger+1]
                dy=(mRNA[counter+1][1:finger+1]-mRNA[counter][1:finger+1])
                if master > 0.0 and master < 1.0 and tcur < tdna[-1]:
                    it=np.digitize([tcur],tdna)[0]
                    dy=(1.0-master)*dy + master*dna[it]
                    y=y-master*dy + master*dna[it]
                #mRNA[counter]                
                #--------ura-haku---------
#                iseq=np.digitize([tcur],ttime)[0]  
                iseqcand=np.digitize([tcur,tcur+240],ttime)
                prob=[0.5,0.5]
                iseq=np.random.choice(iseqcand,p=prob)
                 #------------------------
                if master==1.0:
                    tdna.append(tcur)
                    dna.append(dy[0])
#                print "iseq=",iseq,"/",lseq
                if iseq<lseq:
                    deltat=np.mod(tcur,blen)   
                    ibeat=np.argmin(np.abs(bpos-deltat))
                    if ibeat==nbeat: ibeat=0
                    phg=cp.get_pchord(prelmul[ibeat],tseq[iseq],tkseq[iseq],noct)
                    phg=phg/np.sum(phg)/J*noct
#                    dy=dy+np.array([0.0,0.1,0.2,0.3])[0:finger]
                    if disp:
                        mnow=bbselect_chord(y, dy, phg, mnow,tseq[iseq],tkseq[iseq]) 
                    else:
                        mnow=bbselect_chord(y, dy, phg, mnow)                    

                    mnow,counter=gt.gate_stop(mnow,counter,finger,timer_stop_width,timer_stop_c)            
                    if rhythm_pattern == "bop":
                        durlist=rg.rythmgen(counter,tcur,blen)
                    elif rhythm_pattern == "4beat":
                        durlist=[480]
                    elif rhythm_pattern == "2beat":
                        durlist=[960]
                    elif  rhythm_pattern == "test":
                        durlist=rg.test_random_rythm2()
                    else:
                        durlist=[240]

                    for tmpdur in durlist:
                        if tmpdur > 0:
                            seq.append(mnow)
                            dur.append(tmpdur)
                            tcur=tcur+tmpdur
                        elif tmpdur < 0:
                            seq.append(numrest*np.ones(finger,dtype=int))
                            dur.append(-tmpdur)
                            tcur=tcur-tmpdur

                endmask=(mnow<0) 
                if np.prod(endmask)==1: # all elements of mnow < 0
                    break

            if disp==True:
                plt.show()            

            iphrase=iphrase+1



        iseq=np.digitize([tcur],ttime)[0]  #-

        if iseq >= lseq:
            return np.array(seq), np.array(dur), iphrase, np.array(dna), np.array(tdna)

#    return mseq

