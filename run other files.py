import os
path = os.path.join(os.getenv('APPDATA'), "WindowsDefender")
filename = "rick-roll.mp3"
file_path = os.path.join(path, filename)
os.startfile(file_path)