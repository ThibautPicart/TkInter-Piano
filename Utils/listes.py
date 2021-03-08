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

class Selection(tk.Frame) :
    def __init__(self,parent,data=[]):
        tk.Frame.__init__(self,parent)
        self.parent=parent
        self.list=tk.Listbox(self)
        self.list.configure(height=7)
        self.list.configure(width=10)
        self.__data=data
        for d in data : 
            self.list.insert("end", d)
    def insert(self,data):
        if data not in self.__data :
            self.__data.append(data)
            self.list.insert("end",data)
    def packing(self) :
        self.list.pack()
        self.pack()

class ListMenu(tk.Frame) :
    def __init__(self,parent=None,name="Notes",elements=[],selection=None):
        tk.Frame.__init__(self,parent)
        self.variable = tk.StringVar(self)
        self.variable.set("A") # default value
        self.menu = tk.OptionMenu(self, self.variable, *elements,command=self.cb_selection)
        self.label=tk.Label(self, text=name, relief="flat", bd=4)
        self.selection=selection
    def cb_selection(self,event) :
        print("variable", self.variable.get()) 
        print("event",event)
        self.selection.insert(self.variable.get())

    def get_note(self):
        return self.variable.get()
    def packing(self) :
        self.label.grid(row=1,column=0)
        self.menu.grid(row=1,column=1)
        self.pack()

if __name__ == "__main__" :
    mw = tk.Tk()
    mw.geometry("360x300")
    notes=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
    selection= Selection(mw)
    menu=ListMenu(mw,"notes",notes,selection)
    menu.packing()
    print(menu.get_note())
    selection.packing()
    mw.mainloop()
