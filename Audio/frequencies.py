# https://fr.wikipedia.org/wiki/Note_de_musique

import sqlite3
connect = sqlite3.connect("frequencies.db")
cursor = connect.cursor()
cursor.execute("DROP TABLE IF EXISTS frequencies")
cursor.execute("CREATE TABLE frequencies ( \
                    octave INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
                    C float,CSharp float,\
                    D float,DSharp float,\
                    E float,\
                    F float,FSharp float,\
                    G float,GSharp float,\
                    A float,ASharp float,\
                    B float );"
              )

f0=440.0
level=-5  # Octave 4 : A 440 Hz 
f=f0*2**level

gammes=[]
for i in range(-1,10) :
    octave=[]
    octave.append(i)
    for j in range (-9,3) :
        frequency=f*2**(j/12)
        octave.append(frequency)
        frequency=frequency*2
    f=2*f
    gammes.append(octave)
cursor.executemany("INSERT INTO frequencies VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);", gammes)
key="F"
result=cursor.execute("SELECT "+str(key) +" FROM frequencies WHERE octave=3;")
print("Octave 4 : "+str(key)+" ",result.fetchone()[0],'Hz')
connect.commit()
