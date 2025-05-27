from client_handler import clients

selected_client = None

def server_interface():
    global selected_client

    while True:
        cmd = input("Servidor> ").strip()

        if cmd == "list":
            if not clients:
                print("Nenhum cliente conectado.")
            for idx, addr in enumerate(clients.keys(), 1):
                print(f"{idx}. {addr[0]}:{addr[1]}")

        elif cmd.startswith("select"):
            try:
                num = int(cmd.split()[1]) - 1
                if 0 <= num < len(clients):
                    selected_client = list(clients.keys())[num]
                    print(f"Cliente {selected_client[0]} selecionado.")
                else:
                    print("Numero invalido.")
            except (IndexError, ValueError):
                print("Uso: select <numero>")

        elif cmd == "broadcast":
            command = input("Comando para broadcast: ")
            for client in clients.values():
                client.send(command.encode())

        elif cmd == "help":
            print("Comandos:\n list\n select <num>\n broadcast\n send <comando>\n exit")

        elif cmd.startswith("send"):
            if not selected_client:
                print("Nenhum cliente selecionado.")
                continue
            command = cmd[5:]
            clients[selected_client].send(command.encode())

        elif cmd == "exit":
            print("Saindo do servidor.")
            break

        else:
            print("Comando desconhecido. Use 'help' para ajuda.")
# if __name__ == "__main__":
#     server_interface()    