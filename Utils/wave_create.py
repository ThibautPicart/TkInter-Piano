import sys
import shutil
sys.path.append('../Audio')
from  audio_wav import sinus_wav

sinus_wav('A2.wav',220,8000,1)
print(shutil.move('A2.wav','../Sounds/A2.wav'))