#!/usr/bin/python
import numpy as np
import rest
from collections import deque
from classAutobop import track

def convert_value( value ):
    if value.lower() in ['true', 'false']:
        return value.lower()=='true'
    elif value.isdigit():
        return int(value)
    else:
        return value

def read_arrange(file):
    data=np.loadtxt(file,dtype={'names': ('position','part','control','value'), 'formats': ('int','S32','S32','S32')}, delimiter=':')

    events=deque([])
    for datum in data:
        events.append( {'position':datum['position'], 'part': datum['part'], 'control': datum['control'], 'value': convert_value(datum['value'])} )

    return events

def initialize( option ):
    opt = option.split(',')

    eachcontrol={}
    eachcontrol["onoff"]=True
    eachcontrol["resolution"] = int(opt[0])
    eachcontrol["events"]=read_arrange( opt[1] )

    return eachcontrol

def improvise( tseq, tkseq, ttime, part, control ):
    trk = track()
    trk.extend( [rest.get_numrest()], [control[part]['resolution']] )
    tcur = control['tcur'][part]

    events = control[part]['events']
   
    while len(events) and events[0]['position'] <= tcur :
        event = events.popleft()
        control[event['part']][event['control']] = event['value']

    return trk, control
    
if __name__ == '__main__':
    control={}
    control['tcur'] = {'conductor': 0}
    control['conductor'] = initialize('480,test.arr')

    while control['tcur']['conductor'] < 3000:
        mn, dur, control = improvise( 0, 0, 0, 'conductor', control)
        

    
