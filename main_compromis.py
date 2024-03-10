import IPython.display as ipd
import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

set_1 = {i+1: chr(ord('a') + i) for i in range(26)}
set_1[0] = ' '
x, Fe = sf.read('../sounds/mess_difficile.wav')
y, Fe = sf.read('../sounds/mess.wav')
w, Fe = sf.read('../sounds/mess_ssespace.wav')



def decode_padding(x,Fe):
    seuil = 15
    Nfft = 24000
    x = x*np.hanning(len(x))
    u = np.fft.fft(x,Nfft)
    #show_TF(u)
    taille_echantillon = len(u)
    index = np.argmax(abs(u[int(501*Nfft//Fe):int(527*Nfft//Fe)])) + 501*Nfft//Fe
    frequence_estimee = index * Fe / taille_echantillon
    #print(f"frequence estimee: {frequence_estimee}")
    #print(abs(u[index]))
    if abs(u[index]) >seuil:
        return frequence_estimee
    return 500
    

def show_TF(u):
    Nfft = 24000
    locs = np.linspace(0,26,num=26*Nfft//Fe,endpoint=True)
    plt.stem(locs, abs(u[(501* Nfft)//Fe:(527* Nfft)//Fe]))
    plt.show()

def show(x,Fe):
    t = np.linspace(0, x.shape[0]/Fe, x.shape[0])
    plt.plot(t, x, label="Signal échantillonné")
    plt.grid()
    plt.xlabel(r"$t$ (s)")
    plt.ylabel(r"Amplitude")
    plt.title(r"Signal sonore")
    plt.show()



def decode_letter(x,Fe):
    key = round(decode_padding(x,Fe) - 500)
    #print(key)
    keys = set_1.keys()
    if key not in keys:
        #print('space')
        return ' '
    else:
        #print(set_1[key])
        return set_1[key]



def decode(x,Fe = 8000):
    set = []
    set.append(x[0:2000])
    n = len(x)
    nb_car = int(n//2500)
    if nb_car == 0:
        return decode_letter(x,Fe)
    for k in range(1,nb_car):
        set.append(x[k*2500-200:k*2500+2500])
    m = len(set)
    str = ''
    for i in range(m):
        str = str + decode_letter(set[i],Fe)
    return str

phrase_1 = decode(x)
phrase_2 = decode(y)

print(phrase_1)
print(phrase_2)
#print(decode(w,Fe))
#print(decode_letter(w,Fe))
#filter(x,Fe)
