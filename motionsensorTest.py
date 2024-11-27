from gpiozero import MotionSensor
import socket

# Konfigurer PIR-sensoren
pir = MotionSensor(12)  # GPIO-pin 12 (juster hvis din sensor er tilsluttet en anden pin)

# Opsæt UDP-socket
UDP_IP = "192.168.103.45"  # IP-adressen på den enhed, der skal modtage beskeden
UDP_PORT = 5005   # Port
MESSAGE = "Bevægelse registreret!".encode('utf-8')  # Konverteret til bytes med UTF-8

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("PIR-sensor initialiseret. Afventer bevægelse...")

try:
    while True:
        pir.wait_for_motion()
        print("Bevægelse registreret!")
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))  # Send besked som bytes
        pir.wait_for_no_motion()
except KeyboardInterrupt:
    print("\nAfslutter program.")
finally:
    sock.close()
