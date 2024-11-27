from gpiozero import MotionSensor
# from picamera import PiCamera
import time
import socket

# Konfiguration
PIR_PIN = 4  # GPIO-pin til PIR-sensor
UDP_IP = "server_ip_adresse"  # Serverens IP-adresse
UDP_PORT = 5005              # Serverens UDP-port
IMAGE_PATH = "/home/pi/captured_image.jpg"

# Initialiser kamera og PIR-sensor
pir = MotionSensor(PIR_PIN)
camera = PiCamera()

def capture_image(file_path):
    """Tager et billede og gemmer det på filstien."""
    camera.start_preview()
    time.sleep(2)  # Giver kameraet tid til at justere
    camera.capture(file_path)
    camera.stop_preview()

def send_image_udp(file_path, udp_ip, udp_port):
    """Sender billedet som UDP-pakker."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with open(file_path, "rb") as f:
        data = f.read()
        sock.sendto(data, (udp_ip, udp_port))
        print("Billede sendt som UDP-pakker.")

try:
    print("Systemet overvåger bevægelse...")
    while True:
        pir.wait_for_motion()  # Blokerer, indtil bevægelse registreres
        print("Bevægelse registreret!")
        capture_image(IMAGE_PATH)
        send_image_udp(IMAGE_PATH, UDP_IP, UDP_PORT)
        print("Venter på ny bevægelse...")
        time.sleep(10)  # Undgå gentagne uploads i kort tid
except KeyboardInterrupt:
    print("Afslutter program...")
