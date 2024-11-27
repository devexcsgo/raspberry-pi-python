import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 5005))  # Brug en anden port, fx 5005
print("Lytter efter UDP-beskeder...")

while True:
    data, addr = sock.recvfrom(1024)
    print(f"Besked modtaget fra {addr}: {data.decode()}")
