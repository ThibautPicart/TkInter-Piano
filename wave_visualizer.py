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

from math import pi,sin,cos
from observer import *
import sqlite3



class Generator(Subject) :
    def __init__(self,name="signal"):
        Subject.__init__(self)
        self.name=name
        self.signal=[]
        self.a,self.f,self.p=1.0,1.0,0.0
        self.harmonics=1

    def get_name(self) :
        return self.name
    def get_signal(self) :
        return self.signal
    def get_harmonics(self):
        return self.harmonics
    def get_frequency(self):
        return self.f

    def set_magnitude(self,a) :
        self.a=a
    def set_frequency(self,f) :
        self.f=f
    def set_phase(self, p) :
        self.p=p 
    def set_harmonics(self, harmonics=1):
        self.harmonics=harmonics
    def set_params(self,a=1.0,f=1.0,p=0.0):
        self.a, self.f, self.p = a,f,p

    def notify(self) :
        for obs in self.observers:
            obs.update(self)


    def vibration(self,t,harmoniques=1, impair=True):
        a,f,p=self.a,self.f,self.p
        harmonics=self.harmonics
        somme=0
        for h in range(1,harmonics+1) :
            somme=somme + (a*1.0/h)*sin(2*pi*(f*h)*t-p)
        return somme

    def generate_signal(self,period=1.0,samples=1000):
        del self.signal[0:]
        duration=range(samples)
        Te = period/samples
        for t in duration :
            self.signal.append([t*Te,self.vibration(t*Te)])
        self.notify()
        return self.signal 



class View(Observer) :
    def __init__(self,parent,bg="white",width=600,height=300, units=1,mod=None):
        Observer.__init__(self)
        self.canvas=tk.Canvas(parent,bg=bg,width=width,height=height)
        #self.a,self.f,self.p=10.0,2.0,0.0
        self.name="signal_visualizer"
        self.signals={}
        self.width,self.height=width,height
        self.units=units
        self.canvas.bind("<Configure>",self.resize)
        self.mainModel=mod
        


    def update(self, model=None, key=None):
        #print("View : update()")
        #si on a une nouvelle key, le clavier a joué et on exécute la partie ou name == "octave"
        if model.get_name() == "signal" :
            #print("testt signal")
            if model.get_name()  not in self.signals.keys() :
                self.signals[model.get_name()]= model.get_signal()
            else :
                print(model.get_name())
                self.canvas.delete(model.get_name())
            self.plot_signal(model.get_signal(),model.get_name())
        elif model.get_name() == "octave" :
            scaling=100.0
            connect = sqlite3.connect("Audio/frequencies.db")
            cursor=connect.cursor()
            request="SELECT " + str(key) + " FROM frequencies WHERE octave="+str(model.get_degree())+";"
            result=cursor.execute(request)
            frequence=result.fetchone()[0]
            print("Fréquence de la note jouée : " + str(frequence), "Hz")
            self.mainModel.set_frequency(frequence/scaling)
            self.mainModel.generate_signal()



    def plot_signal(self,signal,name,color="red"):
        w,h=self.width,self.height
        signal_id=None
        if signal and len(signal) > 1:
            plot = [(x*w,h/2.0*(1-y/(self.units/2.0))) for (x, y) in signal]
            signal_id=self.canvas.create_line(plot,fill=color,smooth=1,width=2,tags=name)
        return signal_id

    def grid(self,steps=8):
        self.units=steps
        tile_x=self.width/steps
        for t in range(1,steps+1):
            x =t*tile_x
            self.canvas.create_line(x,0,x,self.height,tags="grid")
            self.canvas.create_line(x,self.height/2-10,x,self.height/2+10,width=3,tags="grid")
        tile_y=self.height/steps
        for t in range(1,steps+1):
            y =t*tile_y
            self.canvas.create_line(0,y,self.width,y,tags="grid")
            self.canvas.create_line(self.width/2-10,y,self.width/2+10,y,width=3,tags="grid")
    
    def resize(self,event):
        if event:
            self.width,self.height=event.width,event.height
            self.canvas.delete("grid")
            for name in self.signals.keys():
                self.canvas.delete(name)
                self.plot_signal(self.signals[name],name)
            self.grid()
            
    
    def packing(self) :
        self.canvas.pack(expand=1,fill="both",padx=6)

class Controller :
    def __init__(self,parent,model,view):
        self.model=model
        self.view=view
        self.create_controls(parent)

    def create_controls(self,parent):
        self.frame=tk.LabelFrame(parent,text='Signal')
        self.amp=tk.IntVar()
        self.amp.set(1)
        self.scaleA=tk.Scale(self.frame,variable=self.amp,
                             label="Amplitude",
                             orient="horizontal",length=400,
                             from_=0,to=5,tickinterval=1)
        self.scaleA.bind("<ButtonRelease>",self.update_magnitude)

        self.frequence=tk.IntVar()
        self.frequence.set(1)
        self.scaleB=tk.Scale(self.frame,variable=self.frequence,
                             label="Fréquence (Hz)",
                             orient="horizontal",length=400,
                             from_=0,to=100,tickinterval=10)
        self.scaleB.bind("<ButtonRelease>",self.update_frequence)

        self.phase=tk.IntVar()
        self.phase.set(1)
        self.scaleC=tk.Scale(self.frame,variable=self.phase,
                             label="Phase",
                             orient="horizontal",length=400,
                             from_=0,to=2*pi,tickinterval=0.1)
        self.scaleC.bind("<ButtonRelease>",self.update_phase)

        self.harmonics=tk.IntVar()
        self.harmonics.set(1)
        self.scaleD=tk.Scale(self.frame,variable=self.harmonics,
                             label="Harmonics",
                             orient="horizontal",length=400,
                             from_=1,to=5,tickinterval=1)
        self.scaleD.bind("<ButtonRelease>",self.update_harmonics)


    def update_magnitude(self,event):
        self.model.set_magnitude(self.amp.get())
        self.model.generate_signal()

    def update_frequence(self,event):
        self.model.set_frequency(self.frequence.get())
        self.model.generate_signal()

    def update_phase(self,event):
        self.model.set_phase(self.phase.get())
        self.model.generate_signal()

    def update_harmonics(self,event):
        self.model.set_harmonics(self.harmonics.get())
        self.model.generate_signal()

    def packing(self) :
        self.frame.pack()
        self.scaleA.pack()
        self.scaleB.pack()
        self.scaleC.pack()
        self.scaleD.pack()

if __name__ == "__main__" :
    mw = tk.Tk()
    mw.title("Visualisation de signal sonore")
    frame=tk.LabelFrame(mw, text="Signal Visualizer",borderwidth=5,width=400,height=300,bg="yellow")
    #mw.geometry("360x300")
    # frame=tk.Frame(mw,borderwidth=5,width=360,height=300,bg="green")
    frame.pack()
    model=Generator()
    view=View(frame)
    view.grid()
    view.packing()
    model.attach(view)
    model.generate_signal()
    ctrl=Controller(mw,model,view)
    ctrl.packing()
    # view.update(model)
    mw.mainloop()
