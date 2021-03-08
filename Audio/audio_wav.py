#!/usr/bin/env python
#-*- coding: utf-8 -*-

# http://izeunetit.fr/ICN1ere/correction/correction_son_5.html

# script audio.py (version modifié et allégée pour les besoins en module CAI)
# (C) Fabrice Sincère ; Jean-Claude Meilland et moi...
# RESTRICTIONS : PCM mono 16 bits signés ( -32 767 -> + 32 767 )

# http://blog.acipo.com/wave-generation-in-python/
# https://www.tutorialspoint.com/read-and-write-wav-files-using-python-wave
# https://www.programcreek.com/python/example/82393/wave.open

import wave
import struct
import binascii
import math
import random
import subprocess


def open_wav(filename):
    """
      (data,framerate) = open_wav(filename):
      rôle :
        lecture d'un fichier WAV 16 bits mono
      entrées :
        filename = nom du fichier au format WAV
      sorties :
        data = liste des échantillons
        framerate = fréquence d'échantillonage
        return 
    """
    data=[]                                      # liste des échantillons, vide si fichier pas mono ou pas sur 16 bits
    file=wave.open(filename,'rb')                # ouverture du fichier en lecture
    framerate = file.getframerate()           # fréquence d'échantillonnage
##    if (file.getnchannels() != 1):               # test Mono
##        print('Le fichier son doit être mono.')
##    elif (file.getsampwidth() != 2):             # test profondeur encodage 16 bits
##        print('Le fichier son doit être encodé sur 16 bits. (Ici: '+str(8*file.getsampwidth())+' bits.)')         
##    else :
    for i in range(file.getnframes()):            # parcours de la suite des échantillons ( getnframes() = nombre total d'échantillons )
        value = file.readframes(1)                # lecture d'un échantillon et passage au suivant
        data.append(struct.unpack("=h",value)[0]) # formule auto-magique pour le décodage...         
    file.close()
    return data,framerate

def save_wav(filename,data,framerate):
    '''
      rôle :
        écriture d'un fichier WAV 16 bits mono
      entrées :
        name = nom du fichier au format WAV
        data = liste des échantillons entiers sur 16 bits non-signés (valeurs < - 32 767 et valeurs > + 32 767 ramenées à leurs limites respectives)
        sampling = fréquence d'échantillonnage : 8000, 11025, 22050, 41 000, 44100 et éventuellement 48000 et 96000
    '''
    to_save = wave.open(filename,'w')
    # création en-tête
    channels = 1                                                            # mono
    n_bytes = 2                                                             # taille d'un échantillon : 2 octets = 16 bits
    samples = len(data)                                                     # nombre total d'échantillon
    params = (channels,n_bytes,framerate,samples,'NONE','not compressed')   # tuple
    to_save.setparams(params)                                                  # création de l'en-tête (44 octets)
    # écriture des données
    print('Please wait ...')
    for i in range(0,samples):
        data[i] = int(data[i]) # au cas où une valeur non entière traînerait...
        # écrétage si valeur en dehors de l'intervalle [-32767,+32767]
        if data[i]<-32767 : data[i]=-32767
        elif data[i]>32767: data[i]=32767                   
        to_save.writeframes(wave.struct.pack('h',data[i])) # codage et écriture échantillon 16 bits signés
    print("saving WAV file : '"+filename+"' done !")
    to_save.close()
    return filename

def save_note_wav(filename,left_frequency,right_frequency,duration=1) :
    # if type(degree) != str :
    #     degree=str(degree)
    # filename= name+degree+".wav"
    to_save=wave.open(filename,'w') 
    nb_channels = 2    # stéreo
    nb_bytes = 1       # taille d'un échantillon : 1 octet = 8 bits
    sampling = 44100   # fréquence d'échantillonnage
    left_level = 1     # niveau canal de gauche (0 à 1) ? '))
    right_level= 0.5    # niveau canal de droite (0 à 1) ? '))
    #duration = 1
    nb_samples = int(duration*sampling)
    params = (nb_channels,nb_bytes,sampling,nb_samples,'NONE','not compressed')
    to_save.setparams(params)    # création de l'en-tête (44 octets)

    # niveau max dans l'onde positive : +1 -> 255 (0xFF)
    # niveau max dans l'onde négative : -1 ->   0 (0x00)
    # niveau sonore nul :                0 -> 127.5 (0x80 en valeur arrondi)

    left_magnitude = 127.5*left_level 
    right_magnitude= 127.5*right_level

    for i in range(0,nb_samples):
        # canal gauche
        # 127.5 + 0.5 pour arrondir à l'entier le plus proche
        left_value = wave.struct.pack('B',int(128.0 + left_magnitude*math.sin(2.0*math.pi*left_frequency*i/sampling)))
        # canal droit
        right_value = wave.struct.pack('B',int(128.0 + right_magnitude*math.sin(2.0*math.pi*right_frequency*i/sampling)))
        to_save.writeframes(left_value + right_value) # écriture frame
    to_save.close()


def sinus_wav(filename='sinus.wav',f=440,framerate=8000,duration=2):   
    '''
      rôle :
        crée un fichier WAV d'onde sinusoïdale
      entrées :
        filename = nom du fichier au format WAV
        f = fréquence du son (440 Hz par défaut)
        framerate = fréquence d'échantillonnage : 11025, 22050, 44100 et éventuellement 48000 et 96000 (8000 Hz par défaut)
        duration = durée du son en secondes ( 2 secondes par défaut)
      sorties :
        data = liste des échantillons
    '''
    data =[int(30000*math.cos(2*math.pi*f*i/framerate)) for i in range(int(framerate*duration))] # framerate*duration = nombre total d'échantillons
    save_wav(filename,data,framerate)
    return data

if  __name__ == "__main__" :
    wav_sinus('A2.wav',220,8000,1)
    wav_sinus('A3.wav',440,8000,1)
    subprocess.call(["aplay", "A2.wav"])
    subprocess.call(["aplay", "A3.wav"])
    data,framerate=open_wav("A2.wav")
    print(framerate,data[0],data[1])

