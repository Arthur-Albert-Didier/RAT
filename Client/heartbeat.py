import threading
import time

def send_heartbeat(client):
    while True:
        try:
            client.send("ping".encode())
            time.sleep(30)
        except:
            break

def start_heartbeat(client):
    threading.Thread(target=send_heartbeat, args=(client,), daemon=True).start()
    