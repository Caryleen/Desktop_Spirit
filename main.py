import os
import time
import faceD
import Testbaidu
import threading
import RPi.GPIO as GPIO
import jianghaodongbaiduyy2


#GPIO.setwarings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
prev_input_set = 0

print ('按键进行录音对话')

while True:
    #faceD.face()
    
    a=GPIO.input(15)
    if((not prev_input_set) and a):
        Testbaidu.rec()
        try:
            jianghaodongbaiduyy2.yy()
        except:
            print('error')
    prev_input_set = a
    time.sleep(0.05)
       


