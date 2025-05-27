import time
import threading
from client_handler import clients, last_ping

def monitor_clients():
    while True:
        now = time.time()
        for addr in list(last_ping.keys()):
            if now - last_ping[addr] > 60:
                print(f"[!] Cliente {addr[0]} desconectado por timeout.")
                try:
                    clients[addr].close()
                except:
                    pass
                if addr in clients:
                    del clients[addr]
                if addr in last_ping:
                    del last_ping[addr]
        time.sleep(10)

def start_heartbeat_monitor():
    threading.Thread(target=monitor_clients, daemon=True).start()
    print("[*] Monitor de heartbeat iniciado.")