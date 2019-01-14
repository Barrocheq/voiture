# -*- coding: utf-8 -*-
import io
import picamera
import hashlib
import zbar
import RPi.GPIO as GPIO

from PIL import Image
from time import sleep

#Demmarage de la camera

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT)
GPIO.output(17, 1)

#with picamera.PiCamera() as camera:
picamera.PiCamera().exposure_mode = 'auto'
picamera.PiCamera().preview_fullscreen = False
picamera.PiCamera().preview_window = (300, 200, 640, 480)
picamera.PiCamera().start_preview()
stream = io.BytesIO()
sleep(0.7)

while 1:
    sleep(0.7)
    picamera.PiCamera().capture(stream, format='jpeg')

    stream.seek(0)
    pil = Image.open(stream)

    scanner = zbar.ImageScanner()
    scanner.parse_config('enable')

    pil = pil.convert('L')
    width, height = pil.size
    raw = pil.tobytes()

    image = zbar.Image(width, height, 'Y800', raw)
    scanner.scan(image)

    classement =[]
    for symbol in image:
        print symbol.data
        if len(symbo.data) != 0:
        classement.append(symbol.data)
        else:
            print 'QRCODE vide'
    print classement

    del(image)
