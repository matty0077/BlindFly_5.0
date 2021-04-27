#!/usr/bin/env python
import sys, time
import grovepi
import threading
import subprocess
import math
# set I2C to use the hardware bus
#grovepi.set_bus("RPI_1")

ultrasonic_ranger = 7#D7 Slot
buzzer = 4#D4 Slot
grovepi.pinMode(buzzer,"OUTPUT")
potentiometer = 1
grovepi.pinMode(potentiometer,"INPUT")
 
#////////////////////////////////soundfx
def soundplay(folder, fx, vol):
    import pygame
    FXPATH="/home/pi/Desktop/GROVE_2.0/BlindFly_3.0/FX/"
    pygame.mixer.init()
    pygame.mixer.music.set_volume(vol)#put above?
    pygame.mixer.music.load(FXPATH + folder +'/' + fx + ".wav")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy==True:
        continue
#soundplay("ranger","far",.1)

#//////////////////////threader
def Threader(action):
    THREAD=threading.Thread(target=action)
    #Thread.daemon=True
    THREAD.start()
    THREAD.join()#optional?
    
######################SHUTDOWN MACHINE
def ShutDown():
    import os
    time.sleep(1)
    os.system("sudo shutdown now -P")

############################customizable alert system. tempo=time in between beeps, rounds is the total number of beeps    
def Beeper(tempo,rounds):
    try:
        while True:
            if rounds>0:
                grovepi.digitalWrite(buzzer,1)
                time.sleep(tempo)
                grovepi.digitalWrite(buzzer,0)
                time.sleep(tempo)
                rounds-=1
                time.sleep(tempo)
                #print(rounds)   
            else:
                grovepi.digitalWrite(buzzer,0)
                break
            
    except KeyboardInterrupt:
        grovepi.digitalWrite(buzzer,0)
        print ("Exit Program...")
        sys.exit()
    except IOError:
        grovepi.digitalWrite(buzzer,0)
        print ("Error")
        sys.exit()
        
##########################READ DISTANCE
def Distancer():
    try:
        sonic=grovepi.ultrasonicRead(ultrasonic_ranger)#ultrasonic ranger reading
        ROTT=grovepi.analogRead(potentiometer)#rotary angle reading
        TEMPO=ROTT*.001#turns angle of sensor into decimal to control response time
                            
        if sonic<=1000 and sonic>750:
            time.sleep(2+TEMPO)
            
        elif sonic<=750 and sonic>500:
            time.sleep(1.75+TEMPO)

        elif sonic<=500 and sonic>350:
            time.sleep(1.25+TEMPO)
            
        elif sonic<=350 and sonic>250:
            time.sleep(1+TEMPO)
            
        elif sonic<=250 and sonic>150:
            time.sleep(.75+TEMPO)

        elif sonic<=150 and sonic>75:
            time.sleep(.5+TEMPO)
            
        elif sonic<=75 and sonic>5:
            time.sleep(.25+TEMPO)

        elif grovepi.ultrasonicRead(ultrasonic_ranger)<=5:
            Beeper(.05,5)
            ShutDown()
            
        #print('{} cm'.format(sonic))
        #print(TEMPO)
        Threader(Beeper(.1,1))

    except KeyboardInterrupt:
        print("Pogram Exit")
        Beeper(.05,3)
        grovepi.digitalWrite(buzzer,0)
        sys.exit()
    except IOError:
        Beeper(.025,10)
        grovepi.digitalWrite(buzzer,0)
        print ("Error")
        sys.exit()
                             
############RUN PROGRAM
while True:
    Distancer()
####################
#soundplay("misc","upgrade",1.0)
#Threader(action)
#ShutDown()
#Beeper(.025,5)
                
