# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/34522095/gui-button-hold-down-tkinter

import sys
# print("Your platform is : " ,sys.platform)
major=sys.version_info.major
minor=sys.version_info.minor
# print("Your python version is : ",major,minor)
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
from observer import *


class Octave(Subject) :
    """ Octave Model """
    def __init__(self,degree=3,name="octave") :
        Subject.__init__(self)
        self.degree=degree
        self.name=name
        self.set_sounds_to_gamme(degree)
    def get_name(self) :
        return self.name
    def get_gamme(self) :
        return self.gamme
    def set_gamme(self,gamme) :
        self.gamme=gamme
    def get_degree(self) :
        return self.degree
    def notify(self,key) :
        # on update les observers = les vues
        for obs in self.observers:
            obs.update(self,key)

    def set_sounds_to_gamme(self,degree=3) :
        self.degree=degree
        folder="Sounds"
        notes=["C","D","E","F","G","A","B","C#","D#","F#","G#","A#"]
        self.gamme=collections.OrderedDict()
        for key in notes :
            self.gamme[key]="Sounds/"+key+str(degree)+".wav"
        return self.gamme

class Screen(Observer):
    """ Octave View """
    def __init__(self,parent) :
        self.parent=parent
        self.create_screen()
    def create_screen(self) :
        self.screen=tk.Frame(self.parent,borderwidth=5,width=500,height=160,bg="pink")
        self.info=tk.Label(self.screen,text="Appuyez sur une touche clavier ",bg="pink",font=('Arial',10))
        self.info.pack()
    def get_screen(self) :
        return self.screen

    def update(self,model,key="C") :
        """Octave View update"""
        if __debug__:
            if key not in model.gamme.keys() :
                raise AssertionError
        subprocess.call(["aplay",model.get_gamme()[key]])
        if self.info :
            self.info.config(text="Vous avez joue la note: "+ key + str(model.get_degree()))
    

class Keyboard :
    """ Octave controller """
    def __init__(self,parent,model) :
        self.parent=parent
        self.model=model
        self.create_keyboard()
    def create_keyboard(self,key_w=40,key_h=150) :
        # key_w,key_h=40,150
        dx_white,dx_black=0,0
        self.keyboard=tk.Frame(self.parent,borderwidth=3, width=7.2*key_w,height=1.05*key_h,bg="red")
        for key in self.model.gamme.keys() :
            if key.startswith('#',1,len(key)) :
                delta_w,delta_h=3/4.,2/3.
                delta_x=3/5.
                button=tk.Button(self.keyboard,name=key.lower(),width=3,height=6,bg="black")
                button.bind("<Button-1>",lambda event,x=key : self.play_note(x))
                button.place(width=key_w*delta_w,height=key_h*delta_h,x=key_w*delta_x+key_w*dx_black,y=0)
                if key.startswith('D#',0,len(key) ) :
                    dx_black=dx_black+2
                else :
                    dx_black=dx_black+1
            else :
                button=tk.Button(self.keyboard,name=key.lower(),bg = "white")
                button.bind("<Button-1>",lambda event,x=key : self.play_note(x))
                button.place(width=key_w,height=key_h,x=key_w*dx_white,y=0)
                dx_white=dx_white+1

    def play_note(self,key) :
        """Octave Controller Action"""
        #key correspond à la note jouée
        self.model.notify(key)

    def get_keyboard(self) :
        return self.keyboard
    def get_degrees(self) :
        return self.degrees

if __name__ == "__main__" :
    mw = tk.Tk()
    mw.geometry("360x300")
    degree=4
    mw.title("Clavier pour octave de degré " + str(degree))
    model=Octave(degree) # on initialise le modele
    # arrivé là on a initialisé le modèle et été chercher les sons dans le dossier sounds
    control=Keyboard(mw,model) # on initialise le controller
    view=Screen(mw)
    model.attach(view)
    control.get_keyboard().grid(column=degree,row=0)
    view.get_screen().grid(column=degree,row=1)
    mw.mainloop()
