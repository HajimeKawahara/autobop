import rest

def getsg():
    sg={0:"C",1:"Db",2:"D",3:"Eb",4:"E",5:"F",6:"Gb",7:"G",8:"Ab",9:"A",10:"Bb",11:"B"} 
    return sg

def getng():
    ng={"B#":0,"C":0, "C#":1,"Db":1, "D":2, "D#":3,"Eb":3, "E":4,"Fb":4, "E#":5,"F":5, "F#":6,"Gb":6, "G":7, "G#":8,"Ab":8, "A":9, "A#":10,"Bb":10, "B":11,"Cb":11}
    return ng

def gethg():
    numrest=rest.get_numrest()
    hg={"":[0,4,7,numrest],"Maj":[0,4,7,numrest],"M":[0,4,7,numrest],"Maj7":[0,4,7,11],"Maj7b5":[0,4,7,11],"7":[0,4,7,10],"7alt":[0,4,7,10],"7cd":[0,4,7,10],"7(B)":[0,4,7,10],"7(A)":[0,4,7,10],"m":[0,3,7,numrest],"m7":[0,3,7,10],"mM7":[0,3,7,11],"mb5":[0,3,6,10],"dim":[0,3,6,9], "sus4":[0,5,7,10]}
    return hg

def get_chord_regexp():
    regexp = r"([A-G]|[A-G]b|[A-G]#|%)(Maj |M |Maj7 |7 |7alt |7cd |7\(B\) |7\(A\) |m |m7 |mb5 |dim |sus4 |Maj7b5 |mM7 | )"
    return regexp

def get_drumkit():
    dr={'Kick':36, 'Rim':37, 'Snare':38, 'F-Tom':41, 'C-HH':42, 'P-HH':44, 'M-Tom':45, 'O-HH':46, 'H-Tom':48, 'Crash':49, 'Ride':51}
    return dr
