from asyncio import events
import PySimpleGUI as sg

sg.theme('default1')

def open_window3():
    layout = [[sg.Text('Enter the file name: '), sg.InputText()],
             [sg.Button("Open File")]]
             
    window = sg.Window("Second Window", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        # if event == "Open File":

    window.close()

def open_window2():
    layout = [[sg.Text('Enter the file directory: '), sg.InputText()],
             [sg.Button("Send File")]]
             
    window = sg.Window("Second Window", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        # if event == "Send File":
    
    window.close()

def open_window():
    layout = [[sg.Text('Wirte your text here: '), sg.InputText()],
             [sg.Button("Send TTS")]]
             
    window = sg.Window("Second Window", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        # if event == "Send TTS":
    
    window.close()

def open_window1():
    layout = [[sg.Text('enter file name'), sg.InputText()],
             [sg.Button("send")]]
             
    window = sg.Window("run mp3 files", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        # if event == "send":            
    
    window.close()


def main():
    layout = [[sg.Button("send tts massege"), sg.Button("open mp3 files"), [sg.Button("send files")], sg.Button("open other files")]]

    window = sg.Window("Main Window", layout)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "send tts massege":
            open_window()
        if event == "open mp3 files":
            open_window1()
        if event == "send files":
            open_window2()
        if event == "open other files":
            open_window3()
    window.close()
if __name__ == "__main__":
    main()