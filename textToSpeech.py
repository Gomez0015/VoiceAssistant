from gtts import gTTS 
import os

def text2Speech(usertext):
    language = 'en'
    myobj = gTTS(text=usertext, lang=language, slow=False) 
    myobj.save("tts.mp3") 

    dir_path = os.path.dirname(os.path.realpath(__file__))

    os.system("afplay tts.mp3")
    
    os.remove("tts.mp3")

