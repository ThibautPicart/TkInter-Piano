from audio_wav import open_wav,save_wav
import sys
import shutil
import subprocess

sys.path.append('../Sounds')
sys.path.append('../Chords')

''' ouverture des fichiers des trois notes, et récupération de leur liste d'échantillons
Remarque : les trois sons doivent bien entendu avoir été créé avec la même fréquence d'échantillonnage... '''

data1,framerate1 = open_wav('../Sounds/C4.wav')
data2,framerate2 = open_wav('../Sounds/E4.wav')
data3,framerate3 = open_wav('../Sounds/G4.wav')

data = [] # liste des échantillons de l'accord

for i in range(len(data1)):
    data.append((1/3.0)*(data1[i]+data2[i]+data3[i])) # calcul de la moyenne de chacun des échantillons de même index issus des trois listes   

filename='C4Major.wav'
save_wav(filename,data,framerate1)
subprocess.call(["aplay", filename])
shutil.move(filename,'../Chords/'+filename)