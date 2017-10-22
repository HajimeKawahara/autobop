# autobop -- Melody Generation Based on Stochastic Processes for Jazz Chord Progressions

## Requirements

- Python 3 (numpy, matplotlib)
- takt http://takt.sourceforge.net
- MIDI software synthesizer (SampleTank, Kontakt, HaLion etc..)

## MIDI Setting for mac

Activate the IAC driver (Application -> Utilities -> Audio MIDI).


## Recording for mac

- Install Soundflower.
- Set output in a software synthesizer to soundflower 2ch.
- Use Audicity or Garage Band to record after setting its input to soundflower 2ch.

## tutorial

In your console, type

autobop.py -band brown.band -sheet giant.abs -o giant.takt

This makes a takt file (giant.takt) in the current directory. Start up your MIDI environment and set instruments. Then, use takt to connect MIDI.

takt giant.takt

## examples

https://soundcloud.com/user653030395/bass-steps
