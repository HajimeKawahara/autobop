#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import argparse
import scale

def read_cel_list(file):
    data=np.loadtxt(file,dtype={'names': ('tag','p'), 'formats': ('S8','S512')}, delimiter=':')
    pcel=[]
    label=[]
    for i in range(0,len(data)):        
        label.append(data["tag"][i].replace('"',''))
        pcel.append(list(map(float,data["p"][i].split(","))))

    return pcel, label

def cel_plot(el,label=[],root=0):
	keyboard=np.array(['white','black','white','black','white','white','black','white','black','white','black','white'])

	keyboard=scale.invert(keyboard,root)
	
	x=np.arange(12)
	c=np.linspace(0,1,len(el))
	while len(el)>len(label):
		label.append('')
	
	for (pel,plabel,i) in zip(el,label,c):
		y=scale.invert(pel, root)
		plt.scatter(x,y,s=100,c=cm.rainbow_r(i),label=plabel)

	plt.xlim(-1,12)
	plt.ylim(-1, 11)
	plt.bar(x[(keyboard=='white')]-0.4, np.ones(7)*10,facecolor='white', edgecolor='black' ,alpha=0.3)
	plt.bar(x[(keyboard=='black')]-0.4, np.ones(5)*10, facecolor='black',edgecolor='black',alpha=0.3)
	
	plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="", borderaxespad=0.)

	plt.show()
	
	return 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot CEL List')
    parser.add_argument('-f', nargs=1, required=True, help='chord probability list',type=str)

    args = parser.parse_args()    
    file=args.f[0]
    pcel, label=read_cel_list(file)

    cel_plot(pcel,label)
