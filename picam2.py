import sys
import time
import picamera
import select
import socket
from gpiozero import PIRSensor

from picamera2 import Picamera2, Preview

request = "none"

while True:
    picam2 = Picamera2()
    picam2.start_preview(Preview.QTGL)

    preview_config = picam2.create_previewconfiguration()
    picam2.configure(preview_config)

    picam2.start()
    picam2.configure(preview_config)
