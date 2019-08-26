'''
Haar Cascade Face detection with OpenCV  
    Based on tutorial by pythonprogramming.net
    Visit original post: https://pythonprogramming.net/haar-cascade-face-eye-detection-python-opencv-tutorial/  
Adapted by Marcelo Rovai - MJRoBot.org @ 7Feb2018 
'''
import pygame
import os
import numpy as np
import cv2
import time
import RPi.GPIO as GPIO
import threading

def face():
    #GPIO.setwarings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    prev_input_set = 0                #set
    GPIO.setup(12,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    prev_input_light = 0                 #light
    GPIO.setup(13,GPIO.IN,pull_up_down = GPIO.PUD_DOWN)
    prev_input_res = 0

    x1=0
    x2=800
    y1=800
    w1=800
    # multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
    faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)
    cap.set(3,640) # set Width
    cap.set(4,480) # set Height

    def led_green_on():
        redPin= 7
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(redPin,GPIO.OUT)
        GPIO.output(redPin,GPIO.HIGH)
    def led_green_off():
        redPin= 7
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(redPin,GPIO.OUT)
        GPIO.output(redPin,GPIO.LOW)
    """
    def autolight():    
        time.sleep(1)
        Pin= 40
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(Pin,GPIO.OUT)
        GPIO.output(Pin,GPIO.HIGH)
    Pin= 40
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Pin,GPIO.OUT)
    GPIO.output(Pin,GPIO.LOW)   """
       
        

        #----------------------------------------

    light = GPIO.input(12)
    if((not prev_input_set) and light ):
        print("dark!----please turn on the light")
        
        pygame.mixer.init()
        if not pygame.mixer.music.get_busy():
            track = pygame.mixer.music.load("works/gxtal.mp3")  
            pygame.mixer.music.play()
        #autolight()
         
    ret, img = cap.read()
    img = cv2.flip(img, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(100, 100) )
    if(not len(faces)):
        led_green_off()
        


    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]     #play rectangle
        
        setinput = GPIO.input(11)
        reset = GPIO.input(13)
        if (480-h-y > 100):
            led_green_on()
        else:
            led_green_off()
        
        if((not prev_input_set) and setinput ):
        #"button pressed"
            w1=w+30
            y1=y+35
            x1=x-30
            x2=x+30
            print("Standard : ")
            print(faces)
        prev_input_set = setinput
        time.sleep(0.05)
        
        # judge positions and play attentions
        if w > w1:   
            print("Too CLOSE")
            #os.system('mplayer works/ktjl.mp3')
            led_green_off()
            pygame.mixer.init()
            if not pygame.mixer.music.get_busy():
                track = pygame.mixer.music.load("works/ktjl.mp3")  
                pygame.mixer.music.play()
                
            
        elif y > y1:
            print(" Too LOW ")
            led_green_off()
            pygame.mixer.init()
            if not pygame.mixer.music.get_busy():
                track = pygame.mixer.music.load("works/ttdl.mp3")  
                pygame.mixer.music.play()
       
            
        elif x > x2 and w < w1 :
            print(" LEFT")
            led_green_off()
            pygame.mixer.init()
            if not pygame.mixer.music.get_busy():
                track = pygame.mixer.music.load("works/tpz.mp3")  
                pygame.mixer.music.play()
          
            
        elif x < x1 and w < w1 :
            print(" RIGHT")
            led_green_off()
            pygame.mixer.init()
            if not pygame.mixer.music.get_busy():
                track = pygame.mixer.music.load("works/tpy.mp3")  
                pygame.mixer.music.play()
           
            
        else :
            print("Normal")
        
            
        if((not prev_input_res ) and reset ):#another solution: if cv2.waitKey(1000 // 12) & 0xff == ord("r"):
            x1=0
            x2=800
            y1=800
            w1=800
            print("RESET")
        prev_input_res = reset
        time.sleep(0.05)
         
    cv2.imshow('video',img)
        # press 'ESC' to quit
    k = cv2.waitKey(100) & 0xff
    if k == 27:
        cap.release()
        cv2.destroyAllWindows()
           





