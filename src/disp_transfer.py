import sound_definition as sd
import matplotlib
import matplotlib.pyplot as plt
import pylab 
import numpy as np

def disp_start():
    col=["#E60012","#F39800","#FFF100","#8FC31F","#009944","#009E96","#00A0E9","#0068B7","#1D2088","#920783","#E4007F","#E5004F"]
    global axp
    figp=plt.figure()
    axp=figp.add_subplot(111)
    pylab.xlabel("i")
    pylab.ylabel("x")
    sg=sd.getsg()
    for i in range(0,12):
        rect = pylab.Rectangle((-1.5, -0.6+0.1*i), 1, 0.1, facecolor=col[i], alpha=0.3)
        pylab.gca().add_patch(rect)
        axp.annotate(sg[i], xy=(-1.0, -0.6+0.1*i+0.05), xycoords='data', fontsize=12,horizontalalignment="center",verticalalignment="center",color="black")
        

def disp_scales(ixp,ifinger,y,dy,mnote,chg,choff,tseqiseq,tkseqiseq):
    global axp
    sg=sd.getsg()
    col=["#E60012","#F39800","#FFF100","#8FC31F","#009944","#009E96","#00A0E9","#0068B7","#1D2088","#920783","#E4007F","#E5004F"]
#    axp.plot([float(ixp)],[y[ifinger]],"o",color=col[np.mod(mnote[ifinger],12)])
    axp.plot([float(ixp)],[y[ifinger]],"o",color="black")
#    axp.plot([float(ixp)],[y[ifinger]-dy[ifinger]],"s",color="gray")
    axp.annotate(sg[np.mod(mnote[ifinger],12)], xy=(ixp,y[ifinger]-dy[ifinger]-choff[ifinger]-0.05), xycoords='data', fontsize=12,horizontalalignment="center",verticalalignment="center",color="black")
    axp.annotate(sg[np.mod(tseqiseq[0],12)]+tkseqiseq, xy=(ixp,y[ifinger]-dy[ifinger]+chg[-1]-choff[ifinger]+0.1), xycoords='data', fontsize=9,horizontalalignment="center",verticalalignment="center",color="black")

    for i in range(0,len(chg)):
        axp.plot([float(ixp)-0.5,float(ixp)+0.5],[y[ifinger]-dy[ifinger]+chg[i]-choff[ifinger],y[ifinger]-dy[ifinger]+chg[i]-choff[ifinger]],color="gray")
                
        if i > 0:
            rect = pylab.Rectangle((float(ixp)-0.5, y[ifinger]-dy[ifinger]+chg[i-1]-choff[ifinger]), 1, chg[i]-chg[i-1], facecolor=col[np.mod(i,12)], alpha=0.3)
        else:
            rect = pylab.Rectangle((float(ixp)-0.5, y[ifinger]-dy[ifinger]+0.0-choff[ifinger]), 1, chg[i], facecolor=col[np.mod(i,12)], alpha=0.3)
        pylab.gca().add_patch(rect)

