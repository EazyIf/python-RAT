import PySimpleGUI as sg

from cli import *

print("[+] Building GUI")

sg.theme("default1")


def main():
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
                s = connect(get_host(), get_port())
                if not s:
                    continue
                send_file(s, path)
                s.close()
            elif event == "run_file":
                filename = values["file_name"]
                send_runner_code(filename)
        elif event == "ip" or event == "port":
            set_host(values["ip"])
            if values["port"].isdigit():
                set_port(values["port"])


if __name__ == "__main__":
    main()
