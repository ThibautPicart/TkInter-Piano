# -*- coding: utf-8 -*-

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
    # print("with this version ... I guess it will work ! ")
    import tkinter as tk
    from tkinter import filedialog 

sys.path.append("Audio")
sys.path.append("Chords")
from audio_wav import save_note_wav, open_wav, save_wav
import sqlite3
from Utils.listes import *
from observer import *
import collections
import subprocess
import shutil


class Menubar(tk.Frame):
    def __init__(self,parent=None):
        tk.Frame.__init__(self, borderwidth=2)
        if parent :
            menu = tk.Menu(parent)
            parent.config(menu=menu)
            fileMenu = tk.Menu(menu)
            fileMenu.add_command(label="Save",command=self.save)
            menu.add_cascade(label="File", menu=fileMenu)

    def save(self):
        formats=[('Texte','*.py'),('Portable Network Graphics','*.png'),('Audio','*.WAV')]
        filename=filedialog.asksaveasfilename(parent=self,filetypes=formats,title="Save...")
        if len(filename) > 0:
            print("Sauvegarde en cours dans %s" % filename)



class Model(Subject):
    def __init__(self):
        Subject.__init__(self)
        self.duration=1 #durée du son 
        self.notes=["C","D","E","F","G","A","B","C#","D#","F#","G#","A#"] #liste des notes
        self.octaves=[1,2,3,4] #liste des octaves
        self.key="" #note selectionnée
        self.octave=1#octave selectionné
        self.gamme="" 
        self.noteliste=[] #liste des notes sélectionnées pour créer accord
        self.chordFilename=""
        self.chordsliste=[]#liste des accords créés

    #gets
    def get_duration(self):
        return self.duration

    def get_notes(self):
        return self.notes

    def get_octaves(self):
        return self.octaves

    def get_key(self):
        return self.key

    def get_octave(self):
        return self.octave

    def get_gamme(self) :
        return self.gamme

    def get_noteliste(self):
        return self.noteliste

    def get_chordsliste(self):
        return self.chordsliste

    #sets
    def set_duration(self, d):
        self.duration=d

    def set_key(self, key):
        self.key=key

    def set_octave(self, octave):
        self.octave=octave

    #play
    def play(self):
        if __debug__:
            if self.key not in self.gamme.keys() :
                raise AssertionError
        subprocess.call(["aplay",self.gamme[self.key]])

    def playChord(self):
        self.notify("accord")



    #insert
    def insert(self):
        self.noteliste.append(self.key+str(self.octave))
        self.notify("addNote")

    def delete(self):
        self.noteliste=[]
        print(self.noteliste)
        self.notify("clear")

    #notify
    def notify(self, action) :
        for obs in self.observers:
            obs.update(self, action)

    #on modifie la gamme en fonction de l'octave choisi
    def set_sounds_to_gamme(self) :
        folder="Sounds"
        self.gamme=collections.OrderedDict()
        for key in self.notes :
            self.gamme[key]="Sounds/"+key+str(self.octave)+".wav"
        return self.gamme

    #generate
    def generate(self):
        print("generate")
        #on récupère les paramètres
        d=self.duration
        key=self.key
        octave=self.octave
        notes=["octave","C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        #on créé le fichier
        connect = sqlite3.connect("Audio/frequencies.db")
        cursor = connect.cursor()
        gammes=cursor.execute("SELECT * FROM frequencies")

        for gamme in gammes :       # toutes les gammes 
            if (octave-1) < gamme[0] < (octave+1)  :  # Gamme de degre 4 de reference, La (A) 440 Hz )
                for i in range(1,len(gamme)) :
                    if notes[i]==key :
                        filename= notes[i]+str(gamme[0])+".wav"
                        print(filename)
                        save_note_wav(filename,gamme[i],2*gamme[i],d)
                        shutil.move(filename,'Sounds')


    def createChord(self):
        datas = [0]*len(self.noteliste)
        framerate=[0]*len(self.noteliste)
        for i in range(len(self.noteliste)) :
            datas[i],framerate[i]=open_wav('Sounds/'+self.noteliste[i]+".wav")

        data=[]
        somme=0
        for i in range(len(datas[0])) :
            for j in range(len(self.noteliste)):
                somme=somme+datas[j][i]
            data.append((1/3.0)*somme)
            somme=0
        filename=""
        for i in range(len(self.noteliste)):
            filename=filename+self.noteliste[i]
        filename=filename+".wav"
        save_wav(filename,data,framerate[0])
        #subprocess.call(["aplay", filename])
        shutil.move(filename,'Chords/'+filename)

        #Puis on l'ajoute à la liste des accords créés
        self.chordsliste.append(filename)
        self.notify("addChord")



class View(Observer):
    def __init__(self,parent):
        Observer.__init__(self)
        self.parent=parent
        self.frameAccord=tk.LabelFrame(parent,text="Générateur d'accords")
        self.noteList=tk.Listbox(self.frameAccord)
        self.noteList.configure(height=4)
        self.noteList.pack()

        self.frameAvailableChords=tk.LabelFrame(parent, text="Accords créés")
        self.chordsList=tk.Listbox(self.frameAvailableChords)
        self.chordsList.configure(height=4)
        self.chordsList.pack()


    def update(self, model=None, action=None):
        if(action=="addNote"):
            self.noteList.insert("end", model.get_noteliste()[-1])
            # self.noteList.delete(0, "end")
            # for note in model.get_noteliste():
            #     self.noteList.insert("end", note)
        elif(action=="clear"):
            #on efface tout
            self.noteList.delete(0, "end")
        elif(action=="addChord"):
            self.chordsList.insert("end", model.get_chordsliste()[-1])
        elif(action=="accord"):
          subprocess.call(["aplay","Chords/"+model.get_chordsliste()[self.chordsList.curselection()[0]]])

       



class Controller :
    def __init__(self,parent,model,view):
        self.model=model
        self.view=view
        self.create_controls(parent)

    def create_controls(self, parent):
        #frame du générateur de note
        self.frameNote=tk.LabelFrame(parent, text="Générateur de notes")

        #duration 
        self.duration=tk.IntVar()
        self.duration.set(1)
        self.scaleDuration=tk.Scale(self.frameNote, variable=self.duration,
                                    label="Durée de la note (s)",
                                    orient="horizontal", length=200,
                                    from_=1, to=5, tickinterval=1)
        self.scaleDuration.bind("<ButtonRelease>", self.update_duration)

        #Choix de la note
        self.key=tk.StringVar()
        self.key.set("Note")
        self.keyList=tk.OptionMenu(self.frameNote, self.key,
                                    *self.model.get_notes())
        self.key.trace("w", self.update_key)

        #Choix de l'octave
        self.octave=tk.IntVar()
        self.octaveList=tk.OptionMenu(self.frameNote, self.octave,
                                    *self.model.get_octaves())
        self.octave.trace("w", self.update_octave)

        #bouton de création de la note
        self.generateBtn=tk.Button(self.frameNote, text="Générer la note")   
        self.generateBtn.bind("<Button-1>", self.generate)

        #bouton pour jouer la note
        self.playBtn=tk.Button(self.frameNote, text="Jouer la note")
        self.playBtn.bind("<Button-1>", self.play)

        #bouton pour ajouter à l'accord
        self.addBtn=tk.Button(self.frameNote, text="Ajouter à l'accord")
        self.addBtn.bind("<Button-1>", self.addNote)

        #bouton pour créér l'accord
        self.createChordBtn=tk.Button(self.view.frameAccord, text="Générer l'accord")
        self.createChordBtn.bind("<Button-1>", self.createChord)

        #bouton pour vider la liste des notes selectionnees
        self.clearListBtn=tk.Button(self.view.frameAccord, text="Vider la liste des notes sélectionnées")
        self.clearListBtn.bind("<Button-1>", self.clearList)

        #bouton pour jouer un accord
        self.playChordBtn=tk.Button(self.view.frameAvailableChords, text="Jouer l'accord sélectionné")
        self.playChordBtn.bind("<Button-1>", self.playChord)

        #choix de la durée de la note
    def update_duration(self, event):
        self.model.set_duration(self.duration.get())

        # choix de la note
    def update_key(self, *args):
        self.model.set_key(self.key.get())

        #choix de l'octave
    def update_octave(self, *args):
        self.model.set_octave(self.octave.get())
        self.model.set_sounds_to_gamme()

    def generate(self, event):
        self.model.generate()

    def play(self, event):
        self.model.play()

    def addNote(self, event):
        self.model.insert()

    def clearList(self, event):
        self.model.delete()

    def createChord(self, event):
        self.model.createChord()

    def playChord(self, event):
        self.model.playChord()


    def packing(self):
        self.frameNote.pack()
        self.scaleDuration.pack(side="top")
        self.keyList.pack(side="left")
        self.octaveList.pack(side="left")
        self.generateBtn.pack(side="bottom")
        self.playBtn.pack(side="bottom")
        self.addBtn.pack()
        self.view.frameAccord.pack(side="left")
        self.createChordBtn.pack()
        self.clearListBtn.pack()
        self.view.frameAvailableChords.pack()
        self.playChordBtn.pack()



if __name__ == "__main__" :
    
    mw=tk.Tk()
    mw.geometry("1200x300")
    mw.title("Generateur de fichier au format WAV")


    #initialisation du model
    model=Model()

    #création de la vue
    view=View(mw)


    #on attache la vue et le modele
    model.attach(view)

    #création du controller
    ctrl=Controller(mw, model, view)
    ctrl.packing()

    #mainloop
    mw.mainloop()





