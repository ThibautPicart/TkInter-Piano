# -*- coding: utf-8 -*-
# script wav_audio.py
#http://fsincere.free.fr/isn/python/cours_python_ch9.php
#http://izeunetit.fr/ICN1ere/son_audio.php
# (C) Fabrice Sincère ; Jean-Claude Meilland
import wave
import math
import shutil

import sqlite3
import subprocess
from audio_wav import save_note_wav

if  __name__ == "__main__" :
    connect = sqlite3.connect("frequencies.db")
    cursor = connect.cursor()
    gammes=cursor.execute("SELECT * FROM frequencies")

    notes=["octave","C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    for gamme in gammes :       # toutes les gammes 
        if 1 < gamme[0] < 3  :  # Gamme de degre 4 de reference, La (A) 440 Hz )
            for i in range(1,len(gamme)) :
                filename= notes[i]+str(gamme[0])+".wav"
                print(filename)
                save_note_wav(filename,gamme[i],2*gamme[i])
                # print(filename)
                subprocess.call(["aplay", filename])
                shutil.move(filename,'../Sounds')
