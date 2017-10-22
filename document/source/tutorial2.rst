==================================
Tutorial 2 (using Jupyter)
==================================

To understand what autobop is doing, Jupyter (or ipython notobook) is very useful. Perform samples/tutorial2.ipynb.

.. code:: python

    %matplotlib inline
    import matplotlib
    import matplotlib.pyplot as plt
    import pylab 
    
    from classAutobop import track
    import autobop
    import sheet
    import numpy as np
    import brownbop
    import sound_definition
    import debugraphic

setting
~~~~~~~

.. code:: python

    # read a band file
    band=autobop.read_personnel("brown.band")

.. code:: python

    # your band members are john (melody: MIDI ch1), paul (bass: MIDI ch3), 
    # tommy (piano: MIDI ch2), and art (drum: MIDI ch4). 
    band




.. parsed-literal::

    {'art': {'ch': 4,
      'module': <module 'rhythmmachine' from 'rhythmmachine.pyc'>,
      'option': 'swing'},
     'john': {'ch': 1,
      'module': <module 'brownbop' from 'brownbop.pyc'>,
      'option': 'melody,test.ss'},
     'paul': {'ch': 3,
      'module': <module 'brownbop' from 'brownbop.pyc'>,
      'option': 'bass,test.ss'},
     'tommy': {'ch': 2,
      'module': <module 'brownbop' from 'brownbop.pyc'>,
      'option': 'piano,test.ss'}}



.. code:: python

    # read a chord progression file
    tseq, tkseq = sheet.read("giant.abs")

.. code:: python

    # tseq describes a sequence of tonic sg notes (from 0 to 11), which is different from the MIDI note.
    # tseq[0:3] #-> array([[11],[ 2],[ 7]])
    # you can know the correspondance of values of notes to CDEF... using getsg().  
    sg=sound_definition.getsg()
    sg[3]




.. parsed-literal::

    'Eb'



.. code:: python

    # tkseq specifies a sequence of chord types
    # tkseq[0:3] #-> array(['Maj7', '7', 'Maj7'], dtype='|S4')

.. code:: python

    # of repititions
    nsamp=3
    tkseq = np.tile(tkseq, nsamp)
    tseq = np.tile(tseq, (nsamp,1))

.. code:: python

    # bpm
    bpm=320

.. code:: python

    # defining the duration of the tonic sequence (tonic duration; tdur)
    chordlength = 960
    tdur = np.full( len(tseq), chordlength, dtype=int )

.. code:: python

    # time of tdur
    ttime=np.cumsum(tdur)

initialize
~~~~~~~~~~

.. code:: python

    control={} #current atmosphere
    trkband={}
    eachtcur={}
    for part in band.keys():
        player = band[part]
        trkband[part]=track()
        #set control 
        eachtcur[part]=0
        control[part]=player['module'].initialize(str(player["option"],"utf-8"))
        
    control["tcur"]=eachtcur  # each current time of a player


.. parsed-literal::

    READ melody.farey
    n 5
    amplitude 30.0
    ['1/5' '1/4' '1/3' '2/5' '1/2' '3/5' '2/3' '3/4' '4/5']


.. code:: python

    print control['john']


.. parsed-literal::

    {'gauss-farey-n': 5, 'teff': 0.4, 'H': 0.4, 'J': 2.0, 'gauss': 'gauss-farey', 'velarr': array([[  84.,   83.,   83., ...,   59.,   59.,   59.],
           [  84.,   84.,   83., ...,   59.,   59.,   59.],
           [  85.,   84.,   84., ...,   59.,   59.,   59.],
           ..., 
           [ 104.,  104.,  104., ...,   91.,   90.,   88.],
           [ 104.,  104.,  104., ...,   92.,   91.,   90.],
           [ 104.,  104.,  104., ...,   93.,   92.,   91.]]), 'gauss-farey-amp': 30.0, 'inst': 'melody', 'iphrase': 0, 'storydict': {'melody': {'len_estab': [4.0], 'timer_start_width': [3.0], 'timer_stop_width': [10.0], 'teff': [0.4, 0.2, 0.7, 0.5, 0.6, 0.2, 0.6, 0.2], 'noct': [2.0], 'timer_stop_c': [55.0], 'timer_start_c': [15.0], 'blen': [480.0], 'gauss-farey': ['melody.farey'], 'master': [1.0], 'finger': [1.0], 'velocgen': ['out.vel'], 'oct': [0.0], 'teff_estab': [0.2], 'beat': [0.0, 240.0], 'H': [0.4, 0.2, 0.6, 0.5, 0.6, 0.3, 0.2], 'J': [2.0, 2.1, 2.2, 1.9], 'rhyfile': ['test.rhy'], 'stab': [0.5, 1.0], 'rhythm_pattern': ['rhythmgen'], 'velstab': [10.0, 0.0], 'celfile': ['cel.list']}, 'secondmel': {'len_estab': [4.0], 'timer_start_width': [5.0], 'timer_stop_width': [7.0], 'teff': [0.3, 0.5, 0.4, 0.7, 1.3, 1.5, 2.5], 'noct': [2.0], 'timer_stop_c': [55.0], 'timer_start_c': [18.0], 'blen': [480.0], 'gauss-farey': ['secondmel.farey'], 'master': [1.0], 'finger': [1.0], 'velocgen': ['out.vel'], 'oct': [0.0], 'teff_estab': [0.2], 'beat': [0.0, 240.0], 'H': [0.6, 0.7, 0.4, 0.5, 0.3, 0.5, 0.7, 0.6], 'J': [3.0, 2.5, 3.0, 2.5], 'rhyfile': ['test.rhy'], 'stab': [0.7, 1.0], 'rhythm_pattern': ['rhythmgen'], 'velstab': [10.0, 0.0], 'celfile': ['cel.list'], 'off': ['-1', '61440']}, 'piano': {'len_estab': [0.0], 'rhythm_pattern': ['test'], 'timer_stop_width': [5.0], 'teff': [0.1, 0.1, 0.1], 'beat': [0.0, 240.0], 'H': [0.8, 0.9, 0.7], 'noct': [3.0], 'J': [2.0, 2.0, 2.0], 'timer_start_width': [0.01], 'celfile': ['cel.list'], 'master': [0.99], 'finger': [5.0], 'timer_start_c': [0.0], 'timer_stop_c': [40.0], 'stab': [0.7, 1.0], 'velstab': [10.0, 0.0], 'blen': [480.0], 'oct': ['-1'], 'teff_estab': [0.2]}, 'bass': {'len_estab': [0.0], 'timer_start_width': [1.0], 'timer_stop_width': [5.0], 'off': [153600.0, 184320.0], 'teff': [0.025], 'beat': [0.0, 240.0], 'H': [0.6], 'noct': [3.0], 'J': [2.0], 'timer_start_c': [0.0], 'celfile': ['celb.list'], 'teff_estab': [0.2], 'master': [0.99], 'finger': [1.0], 'velocgen': ['out.vel'], 'timer_stop_c': [50.0], 'stab': [0.7, 1.0], 'velstab': [10.0, 0.0], 'blen': [480.0], 'oct': ['-2'], 'rhythm_pattern': ['4beat']}, 'general': {'bpm': [380.0], 'inst': ['melody', 'piano', 'bass', 'secondmel'], 'n': [10.0]}}, 'gauss-farey-weight': array([ 0.07462687,  0.22388062,  0.37313437,  0.38059705,  0.75373137,
            0.76865673,  0.91791046,  0.99253732,  1.        ], dtype=float32), 'onoff': True}


main loop
~~~~~~~~~

.. code:: python

    while min( control['tcur'].values() ) < ttime[-1]:
        part = min( control['tcur'].items(), key=lambda x:x[1])[0]
        player=band[part]       
        trk, control = player['module'].improvise(tseq, tkseq, ttime, part, control)
        trkband[part].join(trk)
        control['tcur'][part] = np.sum(trkband[part].dur)


.. parsed-literal::

    paul H= 0.6 J= 2.0 teff 0.025
    john H= 0.4 J= 2.0 teff 0.4
    Farey = 2 / 3
    rhythmgen
    test.rhy
    tommy H= 0.8 J= 2.0 teff 0.1
    john H= 0.2 J= 2.1 teff 0.2
    Farey = 2 / 3
    rhythmgen
    test.rhy
    tommy H= 0.9 J= 2.0 teff 0.1
    paul H= 0.6 J= 2.0 teff 0.025
    john H= 0.6 J= 2.2 teff 0.7
    Farey = 1 / 2
    rhythmgen
    test.rhy
    tommy H= 0.7 J= 2.0 teff 0.1
    paul H= 0.6 J= 2.0 teff 0.025
    john H= 0.5 J= 1.9 teff 0.5
    Farey = 1 / 3
    rhythmgen
    test.rhy
    john H= 0.6 J= 2.0 teff 0.6
    Farey = 1 / 4
    rhythmgen
    test.rhy
    paul H= 0.6 J= 2.0 teff 0.025
    john H= 0.3 J= 2.1 teff 0.2
    Farey = 1 / 4
    rhythmgen
    test.rhy
    tommy H= 0.8 J= 2.0 teff 0.1
    paul H= 0.6 J= 2.0 teff 0.025


.. code:: python

    # triming 
    for part in trkband:
            trkband[part].truncate( ttime[-1] )

results
~~~~~~~

.. code:: python

    trkband




.. parsed-literal::

    {'art': <classAutobop.track instance at 0x106a08ea8>,
     'john': <classAutobop.track instance at 0x106a07518>,
     'paul': <classAutobop.track instance at 0x10a029d88>,
     'tommy': <classAutobop.track instance at 0x106a08f38>}



There are three fundamental methods in track class: duration, MIDI note, and velocity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    # duration
    trkband[b'john'].dur[0:5]




.. parsed-literal::

    array([  1, 239, 240, 480, 240])



.. code:: python

    # MIDI notes  
    trkband[b'john'].note[0:5]




.. parsed-literal::

    array([[-64],
           [ 82],
           [-64],
           [ 78],
           [-64]])



.. code:: python

    # display MIDI notes of john
    fig = plt.figure()
    ax=fig.add_subplot(211)
    debugraphic.plot_midiseq(ax,trkband[b'john'].note[0:100], trkband[b'john'].dur[0:100]) 
    ax=fig.add_subplot(212)
    debugraphic.plot_midiseq(ax,trkband[b'john'].note[100:200], trkband[b'john'].dur[100:200]) 
    plt.show()



.. image:: output_23_0.png


.. code:: python

    # velocity
    trkband[b'john'].vel[0:5]




.. parsed-literal::

    array([[10],
           [87],
           [10],
           [86],
           [10]])


