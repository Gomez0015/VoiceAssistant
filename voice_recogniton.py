import speech_recognition as sr
import string
from pynput import keyboard

COMBINATION = {keyboard.Key.cmd, keyboard.KeyCode.from_char('`')}

r = sr.Recognizer()

text = ""

def startListening():
    with sr.Microphone() as source:
        print("Listening...")

        audio = r.listen(source)

        try:
            text = r.recognize_google(audio)
            return(text)
        except:
            return("nothing detected")

# The currently active modifiers
current = set()

number = 0

def on_press(key):
    if key in COMBINATION:
        current.add(key)
        if all(k in current for k in COMBINATION):
            print("Keys pressed")
            exec(open("chat.py").read())



def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass

if __name__ == "__main__":
   with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

def reset():
    import voice_recogniton




