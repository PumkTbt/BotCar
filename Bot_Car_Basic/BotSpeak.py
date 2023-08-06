from gtts import gTTS
import os
from playsound import playsound

def play(textvoice):
    tts = gTTS(text=textvoice, lang='vi')
    file_name = "voice.mp3"
    tts.save(file_name)
    playsound(file_name)
    os.remove(file_name)

