import socket
import pyodbc
from collections import defaultdict

# Server konfiguration
UDP_IP = "192.168.1.53"
UDP_PORT = 5005
BUFFER_SIZE = 4100  # CHUNK_SIZE (4096) + 4 bytes til pakkeindeks

# Forbindelse til SQL Server-databasen
connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=mssql4.unoeuro.com;"
    "DATABASE=silasstilling_dk_db_gproser;"
    "UID=silasstilling_dk;"
    "PWD=cxenHybp2DFGf9Rtz6aw;"
    "Persist Security Info=True;"
)

# Buffer til pakker
image_data = defaultdict(bytes)

def save_image_to_database(image_data):
    """Gem billedet i databasen."""
    sorted_data = [image_data[i] for i in sorted(image_data)]
    full_image_data = b"".join(sorted_data)

    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        query = "INSERT INTO images (image_data) VALUES (?)"
        cursor.execute(query, (full_image_data,))
        connection.commit()
        print("Billedet er blevet gemt i databasen.")
    except pyodbc.Error as err:
        print(f"Fejl ved indsættelse af billede i database: {err}")
    finally:
        cursor.close()
        connection.close()

# Start serveren
server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((UDP_IP, UDP_PORT))

print(f"Server lytter på {UDP_IP}:{UDP_PORT}...")

try:
    while True:
        data, addr = server_sock.recvfrom(BUFFER_SIZE)

        # Tjek om transmissionen er slut
        if data == b"END":
            print("Transmission afsluttet. Gemmer billedet...")
            save_image_to_database(image_data)
            image_data.clear()  # Ryd bufferen for næste transmission
            continue

        # Håndter billedpakker
        packet_index = int.from_bytes(data[:4], "big")
        packet_content = data[4:]  # Resten er billeddata
        image_data[packet_index] += packet_content  # Saml billeddata

        print(f"Modtog pakke {packet_index} ({len(packet_content)} bytes) fra {addr}")
except KeyboardInterrupt:
    print("Serveren blev stoppet.")
finally:
    server_sock.close()
