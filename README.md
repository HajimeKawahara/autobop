# autobop 

Melody Generation Based on Stochastic Processes for Jazz Chord Progressions.

Jazz improvisations are usually based on chord progressions. Autobop automatically generates phrases based on stochastic processes and an analog of quantum energy levels (QEL) of electrons. The algorithm converts general stochastic processes to melody lines under strong constraints on chord changes. This conversion enables the generated melody to exhibit monotonically increasing, decreasing, jaggy, and periodical features. The QEL model controls affinity of horizontal sounds of melody for chord changes. Several non-Markov processes including the Brownian bridges with the Hurst parameter and the quasi-periodic random Gaussian process are currently available.

See Wiki for the details: https://github.com/HajimeKawahara/autobop/wiki

Note: Our purpose of autobop is NOT to generate good music, but to explore what kind of principle generates new feeling of melody. This concept makes melodies with a mixture of good and bad sounds. But, I do not care much about that, because I am quite sure that real music is NOT an algorithm. I just hope that one find new sounds of improvisation from autobop.


The purpose of autobop is NOT to generate good improvisation as real musicians play, BUT to explore what kind of improvisation is generated by a various combination of principles. This concept should make melodies with a mixture of good and bad sounds. But, I do not care much about that, because I am quite sure that real music is NOT an algorithm. I just hope that one find new sounds of improvisation from autobop.      


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
