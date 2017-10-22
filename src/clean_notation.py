#!/usr/bin/python
import sys
import argparse
import numpy as np

def get_clean_dict():
    #note=["c","des","d","ees","e","f","ges","g","aes","a","bes","b"]
    alles= ["des","ees","ges","aes","bes"]
    gcdict={"CMaj":["des","ees","ges","aes"],"DMaj":alles,"EMaj":alles,"GMaj":["des","ees","ges","aes"],"AMaj":alles,"BMaj":alles, \
                "C":["des","ees","ges","aes"],"D":alles,"E":alles,"G":["des","ees","ges","aes"],"A":alles,"B":alles, \
            "C7":["des","ees","ges","aes"],"D7":alles,"E7":alles,"G7":["des","ees","ges","aes"],"A7":alles,"B7":alles, \
            "C7(A)":["des","ees","ges","aes"],"D7(A)":alles,"E7(A)":alles,"G7(A)":["des","ees","ges","aes"],"A7(A)":alles,"B7(A)":alles, \
            "C7(B)":["des","ees","ges","aes"],"D7(B)":alles,"E7(B)":alles,"G7(B)":["des","ees","ges","aes"],"A7(B)":alles,"B7(B)":alles, \
            "Em7":alles,"Gm7":["ges"],"Am7":alles,"Bm7":alles, \
            "Emb5":["des","ees","ges"],"Amb5":["des","ges","aes","bes"],"Bmb5":alles}



    return gcdict
