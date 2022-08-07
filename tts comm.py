from gtts import gTTS
from playsound import playsound
# ask for text to speak
from pygame import mixer
import pygame

text = "you got hacked"
# generate tts
pygame.init()
pygame.mixer.init()
output = gTTS(text=text, lang="en", tld="co.in")
output.save(f"tts.mp3")



mixer.music.load("tts.mp3")#music file 
mixer.music.play()
pygame.mixer.music.set_volume(1)

while pygame.mixer.music.get_busy():
   ...