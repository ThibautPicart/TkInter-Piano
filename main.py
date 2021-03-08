# -*- coding: utf-8 -*-

import sys
#print("Your platform is : " ,sys.platform)
major=sys.version_info.major
minor=sys.version_info.minor
#print("Your python version is : ",major,minor)
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
elif major==3 and minor==6 :
    import tkinter as tk
    from tkinter import filedialog
else :
    # print("with your python version : ",major,minor)
    # print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog 

from math import pi,sin
import collections
import subprocess
import sqlite3

from observer import *
from piano import *
import wave_generator as generator
import wave_visualizer as visualizer
import keyboard



mw = tk.Tk()
mw.geometry("1200x600")
mw.title("Leçon de Piano")

#Menubar
menubar=generator.Menubar(mw)


#Piano
frame_piano=tk.Frame(mw,borderwidth=5,width=360,height=300)
octaves=4

#Pas la meilleure méthode, mais c'est la seule avec laquelle j'arrive à visualiser la note jouée
#Avec cette méthode, j'attache manuellement tous les keyboards à la vue (plus bas dans le code après création de la view_signal)
model_piano=[]
control_piano=[]
view_piano=[]
for i in range(octaves):
	model_piano.append(i)
	control_piano.append(i)
	view_piano.append(i)
for octave in range(octaves) :
	model_piano[octave]=keyboard.Octave(octave+1)
	control_piano[octave]=keyboard.Keyboard(frame_piano, model_piano[octave])
	view_piano[octave]=keyboard.Screen(frame_piano)
	model_piano[octave].attach(view_piano[octave])
	control_piano[octave].get_keyboard().grid(column=octave,row=0)
	view_piano[octave].get_screen().grid(column=octave,row=1)



#Wave visualizer
visuModel=visualizer.Generator()
frame_signal=tk.Frame(mw,borderwidth=5,width=360,height=300)
view_signal=visualizer.View(frame_signal,mod=visuModel)
view_signal.grid(4)
view_signal.packing()

for octave in range(octaves):
	model_piano[octave].attach(view_signal)


visuModel.attach(view_signal)
frame_piano.pack()
frame_signal.pack(side="left") 

#Générateur
model_generator=generator.Model()
frame_generator=tk.Frame(mw,borderwidth=5,width=360,height=700)
view_generator=generator.View(frame_generator)
model_generator.attach(view_generator)
control_generator=generator.Controller(frame_generator, model_generator, view_generator)
control_generator.packing()
frame_generator.pack()




mw.mainloop()





