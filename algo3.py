import multiprocessing as multiproc
import numpy as np
import soundfile as sf
import pyaudio
import matplotlib.pyplot as plt



def run(value,value2,fileName,fig,saveValue=None):

    value = ((value / 100) * 66) +1
    value2 = ((value2/10))-5
    N = 500
    Ts = 1/N
    t = np.arange(0,1,Ts)
    sin = np.sin(2*np.pi*value*t)
    y=((np.random.rand(N)-0.5)*2)*value2

    n=N*9
    N2=N+n
    nuller=np.zeros(n)
    add = y + sin
    data = np.hstack((add,nuller))


    fdata = np.fft.fftshift(np.abs(np.fft.fft(data)))
    pos =np.argmax(fdata) 

    fig.clf()
    t = np.linspace(0, data.size/N-Ts,data.size)
    ax = fig.add_subplot(2, 1, 2)
    ax.plot(t, data)
    ax = fig.add_subplot(2, 1, 1)
    f= np.arange(-N/2, N/2,N/N2)

    title = "Eingabefrequenz: " + str(round(value,2)) + ",Rauschen: " + str(round(value2,2)) + " Position des Maximums: " + str(abs(round(f[pos],2)))

    fig.suptitle(title, fontsize=20)

    ax.plot(f,fdata)
    fig.canvas.draw()

    multiproc.Process(target=playAudio,args=(data,N)).start()

def playAudio(data,samplerate):
    stream = pyaudio.PyAudio().open(format = pyaudio.paFloat32,channels = 1,rate = samplerate,output = True)
    stream.write(data.astype(np.float32).tobytes())
    stream.close()

if __name__ == '__main__':
    run(10,0,"LadiesGentleman.ogg",plt.figure())
    plt.show()