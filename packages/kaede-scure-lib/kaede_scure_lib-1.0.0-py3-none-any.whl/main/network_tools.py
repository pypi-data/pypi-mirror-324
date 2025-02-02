import socket

def scan_ports(ip: str):
    """ポートスキャンを実行"""
    for port in range(1, 1025):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if not s.connect_ex((ip, port)):
                print(f"Port {port} is open")
