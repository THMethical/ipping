import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

target_ip = "192.168.0.1"
start_port = 1
end_port = 65535
timeout = 0.5
max_threads = 200  # Passe je nach System an

def ping_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            return port
    return None

def main():
    open_ports = []
    port_range = range(start_port, end_port + 1)

    print(f"[i] Starte Port-Ping für {target_ip} ({start_port}-{end_port}) mit {max_threads} Threads...\n")

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(ping_port, port): port for port in port_range}

        for future in tqdm(as_completed(futures), total=len(port_range), desc="Prüfe Ports", ncols=80):
            port = future.result()
            if port:
                print(f"[+] Offen: Port {port}")
                open_ports.append(port)

    print("\n[✓] Scan abgeschlossen.")
    if open_ports:
        print(f"[+] Offene Ports gefunden: {open_ports}")
    else:
        print("[-] Keine offenen Ports gefunden.")

if __name__ == "__main__":
    main()
