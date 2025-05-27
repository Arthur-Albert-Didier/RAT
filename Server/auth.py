def authenticate(client_socket, addr, password_expected="TutuLindo"):
    try:
        password = client_socket.recv(1024).decode()
        if password != password_expected:
            client_socket.send("NOK".encode())
            client_socket.close()
            print(f"[!] Cliente {addr[0]} tentou conectar com senha errada.")
            return False
        else:
            client_socket.send("OK".encode())
            return True
    except Exception as e:
        print(f"[!] Erro na autenticação do cliente {addr}: {e}")
        client_socket.close()
        return False
