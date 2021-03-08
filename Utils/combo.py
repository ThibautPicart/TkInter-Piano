import sys
major=sys.version_info.major
minor=sys.version_info.minor
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
elif major==3 and minor==6 :
    import tkinter as tk
    from tkinter import filedialog
else :
    # print("Your python version is : ",major,minor)
    # print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog 


root = tk.Tk() 
root.geometry('300x200')

labelChoix = tk.Label(root, text = "Veuillez faire un choix !")
labelChoix.pack()

# 2) - créer la liste Python contenant les éléments de la liste Combobox
listeProduits=["Laptop", "Imprimante","Tablette","SmartPhone"]

# 3) - Création de la Combobox via la méthode ttk.Combobox()
listeCombo = ttk.Combobox(root, values=listeProduits)
 
# 4) - Choisir l'élément qui s'affiche par défaut
listeCombo.current(0)

listeCombo.pack()
root.mainloop()