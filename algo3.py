import multiprocessing as multiproc
import numpy as np
import soundfile as sf
import pyaudio
import matplotlib.pyplot as plt



def run(value,value2,fileName,fig,saveValue=None):

    value = ((value / 100) * 66) +1
    value2 = ((value2/100)*11)-5
    Ts = 0.002
    N = 500
    t = np.arange(0,1,Ts)
    sin = np.sin(2*np.pi*value*t)
    y=np.random.rand(N)*value2

    data = y + sin

    fig.clf()
    t = np.linspace(0, data.size/N,data.size)
    ax = fig.add_subplot(2, 1, 2)
    ax.plot(t, data)
    ax = fig.add_subplot(2, 1, 1)
    f= np.linspace(-N/2, N/2,data.size)
    ax.plot(f,np.fft.fftshift(np.abs(np.fft.fft(data))))
    fig.canvas.draw()

    multiproc.Process(target=playAudio,args=(data,N)).start()

def playAudio(data,samplerate):
    stream = pyaudio.PyAudio().open(format = pyaudio.paFloat32,channels = 1,rate = samplerate,output = True)
    stream.write(data.astype(np.float32).tobytes())
    stream.close()

if __name__ == '__main__':
    run(10,0,"LadiesGentleman.ogg",plt.figure())
    plt.show()