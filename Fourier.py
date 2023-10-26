import numpy as np
from matplotlib import pyplot as plt

t = np.arange(0,1,0.002)
xf = np.arange(-250,250,1)
f = np.array([1,5,5.3,100,200,300])

fig = plt.figure("Verlauf Kosinus")
fig.clf()

for i,freq in enumerate(f):
    z = np.cos(2*np.pi*freq*t)
    b= np.fft.fft(z)
    c= np.abs(b)
    d=np.fft.fftshift(c)
    ax = fig.add_subplot(len(f),1,i+1)
    ax.plot(xf,d,'r')
    ax.grid()
    ax.set_title("Frequenz "+str(freq)+"Hz")




plt.show()






