import socket

# Konfiguration af serveren
UDP_IP = "192.168.1.53"  # Serverens IP-adresse
UDP_PORT = 5005
BUFFER_SIZE = 4100  # CHUNK_SIZE (4096) + 4 bytes til pakkeindeks

# Opret en socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Server lytter på {UDP_IP}:{UDP_PORT}...")

# Modtage loop
image_data = {}  # Dictionary til at gemme pakker baseret på deres indeks
while True:
    try:
        # Modtag data fra klienten
        data, addr = sock.recvfrom(BUFFER_SIZE)

        # Check for afslutning
        if data == b"END":
            print("Transmission afsluttet.")
            break

        # Første 4 bytes indeholder pakkeindekset
        packet_index = int.from_bytes(data[:4], "big")
        packet_content = data[4:]  # Resterende bytes er billeddata

        # Gem pakken i buffer
        image_data[packet_index] = packet_content
        print(f"Modtog pakke {packet_index} ({len(packet_content)} bytes) fra {addr}")

    except KeyboardInterrupt:
        print("Serveren blev stoppet.")
        break

# Rekonstruér billeddata i korrekt rækkefølge
sorted_data = [image_data[i] for i in sorted(image_data)]
full_image_data = b"".join(sorted_data)

# Gem billedet til en fil
output_file = "received_image.jpg"
with open(output_file, "wb") as f:
    f.write(full_image_data)
    print(f"Billedet er gemt som '{output_file}'.")

# Luk socket
sock.close()
