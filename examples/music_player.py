from playsound import playsound
import os

path = os.path.join(os.getenv("APPDATA"), "RAT")
filename = "rickroll.mp3"
file_path = os.path.join(path, filename)
playsound(file_path)
