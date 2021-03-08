import os.path
import logging, sys
# logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

def is_directory(path) :
    exists=False
    if os.path.exists(path) :
        exists=True
    return exists

def is_file(path=".",name="README.md") :
    exists=False
    if is_directory(path) :
        message="Le dossier  : ",directory," existe bien"
        print(message)
        print("Le dossier  : ",directory," existe bien")
        # logging.debug(message)
        path_to_file=path+'/'+name
        if os.path.isfile(path_to_file):
            message="Fichier : ",name," trouvé sous le dossier :",path
            print(message)
            print("Fichier : ",name," trouvé sous le dossier :",path)
           # logging.debug(message)
            exists=True
        else:
            message="Fichier : ",name," non trouvé sous le dossier :",path
            print(message)
            print("Fichier : ",name," non trouvé sous le dossier :",path)
            # logging.debug(message)
            exists=False
    else:
        message="Le dossier  :",path," n'existe pas"
        print(message)
         # logging.debug(message)
        exists=False
    return exists

if __name__ == "__main__" :
    directory='../Sounds'
    print(os.path.isdir(directory))
    filename=directory+'A2.wav'
    print(os.path.isfile(filename))