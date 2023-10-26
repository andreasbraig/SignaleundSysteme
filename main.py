import numpy as np
from matplotlib import pyplot as plt

t = np.arange(0,1,0.002)
f = np.array([1,5,5.3,100,200,300])

def PlotCos(t,f):
    fig = plt.figure("Verlauf Kosinus")
    fig.clf()

    for i,freq in enumerate(f):
        z = np.cos(2*np.pi*freq*t)
        ax = fig.add_subplot(len(f),1,i+1)
        ax.plot(t,z,'r')
        ax.grid()
        ax.set_title("Frequenz "+str(freq)+"Hz")

def PlotSin(t,f):
    fig = plt.figure("Verlauf Sinus")
    fig.clf()

    for i,freq in enumerate(f):
        z = np.sin(2*np.pi*freq*t)
        ax = fig.add_subplot(len(f),1,i+1)
        ax.plot(t,z,'b')
        ax.grid()
        ax.set_title("Frequenz "+str(freq)+"Hz")

PlotCos(t,f)
PlotSin(t,f)

#print(h)

plt.show()






