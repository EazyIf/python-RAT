import pygame
import os

path = os.path.join(os.getenv("APPDATA"), "WindowsDefender")
filename = "rickroll.mp3"
file_path = os.path.join(path, filename)
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(file_path)  # music file
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(1)

while True:
    ...
