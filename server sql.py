import socket
import pyodbc
from collections import defaultdict

# Konfiguration af serveren
UDP_IP = "192.168.1.53"  # Erstat med din server IP
UDP_PORT = 5005
BUFFER_SIZE = 4100  # CHUNK_SIZE (4096) + 4 bytes til pakkeindeks

# Opret en socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Server lytter på {UDP_IP}:{UDP_PORT}...")

# Forbindelse til SQL Server-databasen
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=mssql4.unoeuro.com;"  # Serverens IP eller hostname
    "DATABASE=silasstilling_dk_db_gproser;"  # Databasens navn
    "UID=silasstilling_dk;"  # Dit brugernavn
    "PWD=cxenHybp2DFGf9Rtz6aw;"  # Din adgangskode
    "Persist Security Info=True;"  # Gemmer loginoplysninger
)


# Opret forbindelse til SQL Server
connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

# Modtage loop
image_data = defaultdict(bytes)  # Dictionary til at gemme pakker baseret på deres indeks
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
        image_data[packet_index] += packet_content  # Brug += for at tilføje data
        print(f"Modtog pakke {packet_index} ({len(packet_content)} bytes) fra {addr}")

    except KeyboardInterrupt:
        print("Serveren blev stoppet.")
        break

# Rekonstruér billeddata i korrekt rækkefølge
sorted_data = [image_data[i] for i in sorted(image_data)]
full_image_data = b"".join(sorted_data)

# Gem billedet i databasen
try:
    query = "INSERT INTO images (image_data) VALUES (?)"
    cursor.execute(query, (full_image_data,))
    connection.commit()
    print("Billedet er blevet gemt i databasen.")
except pyodbc.Error as err:
    print(f"Fejl ved indsættelse af billede i database: {err}")

# Luk forbindelsen til SQL Server
cursor.close()
connection.close()

# Luk socket
sock.close()
