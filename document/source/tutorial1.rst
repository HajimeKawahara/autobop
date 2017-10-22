=======================
Tutorial 1 (console)
=======================

Simple use
-----------------------

In your console, type 

::

 autobop.py -band brown.band -sheet giant.abs -o giant.takt

This makes a takt file (giant.takt) in the current directory. Start up your MIDI environment and set instruments. Then, use takt to connect MIDI.

::

 takt giant.takt

Changing the chord
----------------------------------

The abs file describes the chord progression. For instance, giant.abs contains::

 | BMaj7 D7 | GMaj7 Bb7 | EbMaj7 EbMaj7 | Am7 D7 |
 | GMaj7 Bb7 | EbMaj7 F#7 | BMaj7 BMaj7 | Fm7 Bb7 |
 | EbMaj7 EbMaj7 | Am7 D7 | GMaj7 GMaj7 | Dbm7 Gb7 |
 |BMaj7 BMaj7 | Fm7 Bb7 | EbMaj7 EbMaj7 | Dbm7 Gb7 || 

The preset chord symbols are here.

====== ======
symbol same
====== ======
Maj    
M      Maj
Maj7   
7      7
7alt   7
7cd    7
7(B)   7
7(A)   7
m 
m7 
mb5 
dim 
sus4 
Maj7b5 
mM7
====== ======

See sound_definition.py in detail.

Changing the band members
----------------------------------

The band file specifies the characteristics of the band. For instance, brown.band has

::

 john:brownbop:melody,test.ss
 tommy:brownbop:piano,test.ss
 paul:brownbop:bass,test.ss
 art:rhythmmachine:swing

In this case, there are four members and john, tommy, and paul use "brownbop" and art "rhythmmachine" as the improvization module. If you want to change the improvisation module, edit these. the third column corresponds to the option of the impovisation module. See the descriptions of each module for this option. Here, we show an example for the brownbop module.

In test.ss, you find the lines such as:: 

 melody:teff:0.4,0.2,0.7,0.5,0.6,0.2,0.6,0.2
 melody:H:0.4,0.2,0.6,0.5,0.6,0.3,0.2

These lines specifies the effective temperature and the Hurst exponent for "melody". 
If you change these sequence, you will hear different taste of the improvisation. Try it. 


 

