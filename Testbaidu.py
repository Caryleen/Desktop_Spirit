import os
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

def led_blue_on():
    Pin= 22
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Pin,GPIO.OUT)
    GPIO.output(Pin,GPIO.HIGH)
def led_blue_off():
    Pin= 22
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Pin,GPIO.OUT)
    GPIO.output(Pin,GPIO.LOW)
    
def rec():
    
    print("recording...")
    led_blue_on()
    os.system('sudo arecord -D "plughw:0" -f S16_LE -r 16000 -d 4 /home/pi/jiqiren/voice.wav')
    led_blue_off()
    print("finish")

