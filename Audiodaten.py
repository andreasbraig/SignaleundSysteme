import numpy as np
import soundfile as sf  #Importieren des soundfile Pakets als "sf"
import pyaudio #Importieren des pyaudio Pakets
import multiprocessing as multiproc

data, samplerate = sf.read('california.mp3') #Liest die Audio Datei test.ogg und speichert die Daten in das numpy Array data ab sowie die Abtastrate in samplerate
sf.write('new.mp3', data, samplerate) #Abspeichern von Daten in eine mp3 Datei

stream = pyaudio.PyAudio().open(format = pyaudio.paFloat32,channels = 1,rate = 2 * samplerate,output = True) #Datenstrom vorbereiten
stream.write(data.astype(np.float32).tobytes()) #Datenarray umwandeln und als Datenstrom abspielen
stream.close() #Schließen des Datenstroms




