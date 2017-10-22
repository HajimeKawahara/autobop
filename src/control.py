#!/usr/bin/python
import argparse
import numpy as np
import sys
import matplotlib
import matplotlib.pyplot as plt
import pylab 

def extract_control(dict,tag):
    q=[]
    for x in list(dict.keys()):
        if tag in dict[x]:
            q.append(dict[x][tag])
    return q
