import socket
import time
from picamera2 import Picamera2

# Konfiguration
UDP_IP = "192.168.1.53"
UDP_PORT = 5005
CHUNK_SIZE = 4096

# Initialiser kamera
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)})
picam2.configure(camera_config)

picam2.start()
time.sleep(2)

# Tag et billede som JPEG
picam2.capture_file("temp_image.jpg")
with open("temp_image.jpg", "rb") as f:
    image_bytes = f.read()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send billedet i pakker
print("Sender billedet...")
for i in range(0, len(image_bytes), CHUNK_SIZE):
    chunk = image_bytes[i:i + CHUNK_SIZE]
    packet_index = i // CHUNK_SIZE
    packet = packet_index.to_bytes(4, "big") + chunk
    sock.sendto(packet, (UDP_IP, UDP_PORT))
    print(f"Sendte pakke {packet_index} ({len(chunk)} bytes)")
    time.sleep(0.01)  # Kort pause

sock.sendto(b"END", (UDP_IP, UDP_PORT))
print("Transmission afsluttet.")

picam2.stop()
