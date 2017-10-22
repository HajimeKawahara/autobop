### STORY SHEET ###

#general:inst:melody,piano
general:inst:melody,piano,bass,secondmel
#general:inst:melody,bass
general:n:10
general:bpm:380

#-- MELODY --#
melody:master:1.0
melody:finger:1
melody:oct:0
melody:teff:0.4,0.2,0.7,0.5,0.6,0.2,0.6,0.2
melody:H:0.4,0.2,0.6,0.5,0.6,0.3,0.2
melody:J:2.0,2.1,2.2,1.9
melody:gauss-farey:melody.farey
melody:teff_estab:0.2
melody:len_estab:4
melody:stab:0.5,1.0
melody:beat:0,240
melody:blen:480
melody:velstab:10,0
melody:velocgen:out.vel

melody:celfile:cel.list
melody:rhythm_pattern:rhythmgen
melody:rhyfile:test.rhy

melody:noct:2

melody:timer_stop_width:10.0
melody:timer_stop_c:55.0
melody:timer_start_width:3.0
melody:timer_start_c:15.0

#-- SECONDMEL --#
secondmel:master:1.0
secondmel:finger:1
secondmel:oct:0
secondmel:teff:0.3,0.5,0.4,0.7,1.3,1.5,2.5
secondmel:H:0.6,0.7,0.4,0.5,0.3,0.5,0.7,0.6
secondmel:J:3.0,2.5,3.0,2.5
secondmel:off:-1,61440
secondmel:gauss-farey:secondmel.farey
secondmel:teff_estab:0.2
secondmel:len_estab:4
secondmel:stab:0.7,1.0
secondmel:beat:0,240
secondmel:blen:480

secondmel:celfile:cel.list
secondmel:rhythm_pattern:rhythmgen
secondmel:rhyfile:test.rhy
secondmel:noct:2
secondmel:velstab:10,0

secondmel:timer_stop_width:7.0
secondmel:timer_stop_c:55.0
secondmel:timer_start_width:5.0
secondmel:timer_start_c:18.0
secondmel:velocgen:out.vel



#-- BASS --#
bass:master:0.99
bass:finger:1
bass:oct:-2
bass:teff:0.025
bass:H:0.6
bass:J:2.0
bass:off:153600,184320
#
bass:stab:0.7,1.0
bass:beat:0,240
bass:blen:480
bass:velstab:10,0

#
bass:celfile:celb.list
bass:rhythm_pattern:4beat
bass:noct:3
bass:velocgen:out.vel

bass:timer_stop_width:5.0
bass:timer_stop_c:50.0
bass:timer_start_width:1.0
bass:timer_start_c:0.0
bass:teff_estab:0.2
bass:len_estab:0

#-- PIANO --#
piano:master:0.99
piano:finger:5
piano:oct:-1
piano:teff:0.1,0.1,0.1
piano:H:0.8,0.9,0.7
piano:J:2.0,2.0,2.0

piano:teff_estab:0.2
piano:len_estab:0
piano:stab:0.7,1.0
piano:beat:0,240
piano:blen:480
piano:velstab:10,0

#
piano:celfile:cel.list
piano:rhythm_pattern:test
piano:noct:3

piano:timer_stop_width:5.0
piano:timer_stop_c:40.0
piano:timer_start_width:0.01
piano:timer_start_c:0.0
