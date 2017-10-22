#!/usr/bin/python
import numpy as np
import rest

def_vel = 80

def padding( seq1, seq2, value ):
      seq1=np.array(seq1)
      seq2=np.array(seq2)

      if seq1.shape[1] != seq2.shape[1]:
            delta = seq1.shape[1] - seq2.shape[1]
            if delta > 0:
                  pad = np.full( (len(seq2), abs(delta)), value, dtype=int)
                  seq2 = np.hstack([seq2, pad])
            elif delta < 0:
                  pad = np.full( (len(seq1), abs(delta)), value, dtype=int)
                  seq1 = np.hstack([seq1, pad])

      return seq1, seq2

class track:
      def __init__(self, oct=0):
            self.oct = oct
            self.note = np.zeros([0,1],dtype=int)
            self.dur = np.zeros(0,dtype=int)
            self.vel = np.zeros([0,1],dtype=int)

      def extend(self, ext_note, ext_dur, ext_vel=None):
            numrest = rest.get_numrest()
            ext_note = np.array(ext_note)
            ext_dur = np.array(ext_dur)
            ext_vel = np.array(ext_vel) if ext_vel is not None else np.full(len(ext_note), def_vel, dtype=int)
          
            #--- Error check ---#
            if ext_note.dtype != 'int64' or ext_note.ndim not in [1,2]:
                  print('Seq.extend: illegal note sequence. (dtype=%s, ndim=%d)' % (ext_note.dtype, ext_note.ndim))
                  return
            if ext_vel.dtype != 'int64' or ext_vel.ndim not in [1,2]:
                  print('Seq.extend: illegal vel sequence. (dtype=%s, ndim=%d)' % (ext_vel.dtype, ext_vel.ndim))
                  return
            if ext_dur.ndim != 1:
                  print('Seq.extend: illegal dur seauence. (ndim=%d)' % (ext_dur.ndim))
                  return
            if len(ext_note) != len(ext_dur) or len(ext_dur) != len(ext_vel):
                  print('Seq.extend: inconsistent length')
                  return

            #--- Transform ---#
            if ext_note.ndim==1: ext_note = ext_note.reshape(len(ext_note), 1)
            if ext_vel.ndim==1: ext_vel = ext_vel.reshape(len(ext_vel), 1)

            #--- Padding ---#
            self.note, ext_note = padding(self.note, ext_note, numrest)
            self.vel, ext_vel = padding(self.vel, ext_vel, -1)

            #--- Stack ---#
            self.note = np.vstack([self.note, ext_note])
            self.dur = np.append(self.dur, ext_dur)
            self.vel = np.vstack([self.vel, ext_vel])

            return

      def join(self, trk):
            self.oct = trk.oct
            self.extend( trk.note, trk.dur, trk.vel )

            return


      def toMidinote(self):
            numrest=rest.get_numrest()

            mn=self.note+60+12*self.oct
            mn[self.note<0]=numrest

            return mn

      def truncate(self, timecode):
            excess_idx = np.digitize( [timecode], np.cumsum(self.dur) )[0]
            self.note, self.dur, self.vel = self.note[0:excess_idx], self.dur[0:excess_idx], self.vel[0:excess_idx]

if __name__=='__main__':
      test=track()

      test.extend([[10,20],[30,30]],[480,480],[80,80])
      test.extend([60,70],[240,240])
      test.extend([40,50,60],[120,120,120],[[40,40],[40,40],[40,50,80]])

      print(test.note)
      print(test.dur)
      print(test.vel)
