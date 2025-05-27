def authenticate(client, password="TutuLindo"):
    client.send(password.encode())
    response = client.recv(1024).decode()
    if response != "OK":
        print("[!] Autenticação falhou. Fechando cliente.")
        client.close()
        return False
    return True
# def authenticate(client, password="minha_senha123"):