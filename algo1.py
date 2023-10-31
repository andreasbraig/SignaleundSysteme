import multiprocessing as multiproc
import numpy as np
import soundfile as sf
import pyaudio
import matplotlib.pyplot as plt

def run(value,value2,fileName,fig,saveValue=None):
    data, samplerate = sf.read(fileName)

    value = value / 100 * 0.6

    l = len(data)
    ts = 1/samplerate
    tmult = np.arange(0,l*ts,ts)
    cos = np.cos(2*np.pi*(value * samplerate)*tmult)

    fig.clf()

    fig = plt.figure("Verlauf Skaliert mit "+str(value) + " mal fs")
    data2=data*cos
    t = np.linspace(0, data2.size/samplerate,data2.size)
    ax = fig.add_subplot(2, 1, 2)
    ax.plot(t, data2)
    ax = fig.add_subplot(2, 1, 1)
    f= np.linspace(-samplerate/2, samplerate/2,data2.size)
    ax.plot(f,np.fft.fftshift(np.abs(np.fft.fft(data2))))

    fig.canvas.draw()

    multiproc.Process(target=playAudio,args=(data2,samplerate)).start()

def playAudio(data,samplerate):
    stream = pyaudio.PyAudio().open(format = pyaudio.paFloat32,channels = 1,rate = samplerate,output = True)
    stream.write(data.astype(np.float32).tobytes())
    stream.close()

if __name__ == '__main__':
    run(10,0,"LadiesGentleman.ogg",plt.figure())
    plt.show()