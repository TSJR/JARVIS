import speech_recognition as sr 
import pyttsx3
from utils import *

# Local vars for commands
enabled = False

def validate_cmnd(text):
    text = text.lower()
    if "jarvis" in text:
        return text[text.index("jarvis") + 7:]
    else:
        return ""
    

# Hardcoded commands
def enable():
    global enabled
    if not enabled:
        enabled = True
        return "Welcome back sir"
        

def disable():
    global enabled
    if enabled:
        enabled = False
        return "Shutting off"
    
cmnds = {
    "enable": enable,
    "disable": disable,
    "disabled": disable
}

if __name__ == "__main__":
    rec = sr.Recognizer()

    run = True
    print("START")
    while run:
        try:
            with sr.Microphone() as source:
                rec.adjust_for_ambient_noise(source, duration=0.2)
                audio = rec.listen(source)
                raw_text = rec.recognize_google(audio)
                query = validate_cmnd(raw_text)
                if query:
                    if cmnds.get(query): # Hardcoded command
                        response = cmnds[query]()
                    elif enabled: # Don't do anything if JARVIS isn't enabled
                        response = fetch_response(query)
                    if response:
                        speak_text(response)
                
                
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            
        except sr.UnknownValueError:
            print("Nothing heard")