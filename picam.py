import socket
import time
from picamera2 import Picamera2, Preview

# Konfiguration af UDP
UDP_IP = "192.168.1.53"  # Erstat med serverens IP-adresse
UDP_PORT = 5005  # Porten, serveren lytter på
CHUNK_SIZE = 4096  # Maksimal størrelse for hver UDP-pakke (4 KB)

# Initialiser kameraet
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)})
picam2.configure(camera_config)

# Start kameraet
picam2.start()
time.sleep(2)  # Vent for at sikre, at kameraet er klar

# Tag et billede som JPEG
image_bytes = picam2.capture_file("temp_image.jpg")
with open("temp_image.jpg", "rb") as f:
    image_bytes = f.read()

# Opret en socketforbindelse
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send billedet i mindre pakker med indeksering
print("Sender billedet i mindre pakker...")
for i in range(0, len(image_bytes), CHUNK_SIZE):
    # Opdel billedet i chunks
    chunk = image_bytes[i:i + CHUNK_SIZE]
    packet_index = i // CHUNK_SIZE  # Beregn pakkeindekset
    packet = packet_index.to_bytes(4, "big") + chunk  # Tilføj indekset som de første 4 bytes
    sock.sendto(packet, (UDP_IP, UDP_PORT))
    print(f"Sendte pakke {packet_index} ({len(chunk)} bytes)")

# Send "END"-pakke for at markere afslutningen
sock.sendto(b"END", (UDP_IP, UDP_PORT))
print("Transmission afsluttet.")

# Stop kameraet
picam2.stop()