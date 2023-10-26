import numpy as np
from matplotlib import pyplot as plt
ts=0.002
fs= 1/ts
t = np.arange(0,1,ts)
xf = np.arange(-fs/2,fs/2,1)
f = np.array([1,5,5.3,100,200,300])
fm= np.array([0,0.02,0.05,0.1,0.3,0.45,0.5,0.6])*fs

for j, mfreq in enumerate(fm):
    cos = np.cos(2*np.pi*mfreq*t)
    fig = plt.figure("Verlauf Mult "+str(mfreq)+"Hz")
    fig.clf()

    for i,freq in enumerate(f):
        z = np.cos(2*np.pi*freq*t)
        d = cos*z
        b= np.fft.fft(d)
        c= np.abs(b)
        res=np.fft.fftshift(c)  # umwandlung mit fourier
        ax = fig.add_subplot(len(f),2,2*i+1+1) #rechter plot
        ax.plot(xf,res,'m')
        ax.grid()
        ax.set_title("Frequenz "+str(freq)+"Hz")
        ax = fig.add_subplot(len(f),2,2*i+1) #linker plot
        ax.plot(t,d,'c')
        ax.grid()
        ax.set_title("Frequenz "+str(freq)+"Hz")


plt.show()






