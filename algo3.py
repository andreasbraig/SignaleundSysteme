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
    n=N*9
    N2=N+n
    t = np.arange(0,1,Ts)
    t2 = np.arange(0,10,Ts)
    sin = np.sin(2*np.pi*value*t)
    sin2 = np.sin(2*np.pi*value*t2)
    y=((np.random.rand(N)-0.5)*2)*value2
    y2=((np.random.rand(N2)-0.5)*2)*value2

    nuller=np.zeros(n)
    add = y + sin
    data = np.hstack((add,nuller))
    data2 = y2 + sin2


    fdata0 = np.fft.fftshift(np.abs(np.fft.fft(add)))
    fdata1 = np.fft.fftshift(np.abs(np.fft.fft(data)))
    fdata2 = np.fft.fftshift(np.abs(np.fft.fft(data2)))
    pos =np.argmax(fdata1) 

    fig.clf()
    fig.subplots_adjust(hspace = 0.5)
    plt.rc ('xtick', labelsize = 10) 
    plt.rc ('ytick', labelsize = 10)
    t = np.linspace(0, data.size/N-Ts,data.size)
    t0 = np.linspace(0, add.size/N-Ts,add.size)
    f= np.arange(-N/2, N/2,N/N2)
    f0= np.arange(-N/2, N/2,1)
    ax = fig.add_subplot(3, 2, 2)
    ax.set_title("Sinus im Zeitbereich", fontsize=10)
    ax.plot(t0, add,'g')
    ax = fig.add_subplot(3, 2, 4)
    ax.set_title("Sinus mit Nullern im Zeitbereich", fontsize=10)
    ax.plot(t, data,'g')
    ax = fig.add_subplot(3, 2, 6)
    ax.set_title("Sinus verlängerte Zeitachse im Zeitbereich", fontsize=10)
    ax.plot(t, data2, 'g')
    ax = fig.add_subplot(3, 2, 1)
    ax.set_title("Sinus im Frequenzbereich", fontsize=10)
    ax.plot(f0, fdata0, 'm')
    ax = fig.add_subplot(3, 2, 3)
    ax.set_title("Sinus mit Nullern im Frequenzbereich", fontsize=10)
    ax.plot(f,fdata1, 'm')
    ax = fig.add_subplot(3, 2, 5)
    ax.set_title("Sinus verlängerte Zeitachse im Frequenzbereich", fontsize=10)
    ax.plot(f,fdata2, 'm')

    title = "Eingabefrequenz: " + str(round(value,2)) + ",Rauschen: " + str(round(value2,2)) + " Position des Maximums: " + str(abs(round(f[pos],2)))

    fig.suptitle(title, fontsize=20)

    fig.canvas.draw()

    multiproc.Process(target=playAudio,args=(data,N)).start()

def playAudio(data,samplerate):
    stream = pyaudio.PyAudio().open(format = pyaudio.paFloat32,channels = 1,rate = samplerate,output = True)
    stream.write(data.astype(np.float32).tobytes())
    stream.close()

if __name__ == '__main__':
    run(10,0,"LadiesGentleman.ogg",plt.figure())
    plt.show()