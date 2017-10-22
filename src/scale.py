#!/usr/bin/python
import numpy as np

def invert(scale, root):
	inv=np.r_[scale[root::],scale[:root:]]
	
	return inv
	
def transpose(scale, root):
    trans=np.r_[scale[-root::],scale[:-root:]]

    return trans

