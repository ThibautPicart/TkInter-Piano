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
from keyboard import *

class Piano :
    def __init__(self,parent,octaves) :
        self.parent=parent
        self.octaves=[]
        frame=tk.Frame(self.parent,bg="yellow")
        for octave in range(octaves) :
            self.create_octave(frame,octave+2)
        frame.pack(fill="x")

    def create_octave(self,parent,degree=3) :
        model=Octave(degree)
        control=Keyboard(parent,model)
        view=Screen(parent)
        model.attach(view)
        control.get_keyboard().grid(column=degree,row=0)
        view.get_screen().grid(column=degree,row=1)
        self.octaves.append(model)

if __name__ == "__main__" :
    mw = tk.Tk()
    mw.geometry("360x300")
    octaves=2
    mw.title("La leçon de piano à " + str(octaves) + " octaves")
    piano=Piano(mw,octaves)
    mw.mainloop()
