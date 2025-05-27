import socket
import threading
import os
from colorama import Fore, init
from client_handler import handle_client
from heartbeat import start_heartbeat_monitor
from interface import server_interface

init(autoreset=True)

def logo():
    print(f"{Fore.GREEN}" + r"""   _____ _           _       _ _   _ 
  |  ___(_)         | |     (_) \ | |
  | |__  _ _ __  ___| |_ ___ _|  \| |
  |  __|| | '_ \/ __| __/ _ \ | . ` |
  | |___| | | | \__ \ ||  __/ | |\  |
  \____/|_|_| |_|___/\__\___|_\_| \_/""" + f"{Fore.RESET}")

def accept_clients(server):
    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

def start_server(host="0.0.0.0", port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[!!!] Servidor escutando em {host}:{port}")

    threading.Thread(target=accept_clients, args=(server,), daemon=True).start()
    start_heartbeat_monitor()

    os.system("cls" if os.name == "nt" else "clear")
    logo()
    print("[...] Esperando conexão...")

    server_interface()

if __name__ == "__main__":
    start_server()
    # start_server("    