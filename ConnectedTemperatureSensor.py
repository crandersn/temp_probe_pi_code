from threading import Timer
import pyrebase
from TempReader import TempReader
from datetime import datetime
import RPi.GPIO as GPIO
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import time
import datetime
import boto3
import os

class ConnectedTempSensor:
    
    def __init__(self):
        # set up LCD
        self.lcd_columns = 16
        self.lcd_rows = 2

        self.lcd_rs = digitalio.DigitalInOut(board.D22)
        self.lcd_en = digitalio.DigitalInOut(board.D17)
        self.lcd_d4 = digitalio.DigitalInOut(board.D25)
        self.lcd_d5 = digitalio.DigitalInOut(board.D24)
        self.lcd_d6 = digitalio.DigitalInOut(board.D23)
        self.lcd_d7 = digitalio.DigitalInOut(board.D18)
        self.backlight_d8 = digitalio.DigitalInOut(board.D8)

        self.lcd = characterlcd.Character_LCD_Mono(self.lcd_rs, self.lcd_en, self.lcd_d4, self.lcd_d5, self.lcd_d6, self.lcd_d7, self.lcd_columns, self.lcd_rows, self.backlight_d8)

        #set up button and switch
        self.button = 16
        self.powerSwitch = 26
        GPIO.setup(self.button, GPIO.IN,pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.powerSwitch, GPIO.IN,pull_up_down=GPIO.PUD_UP)

        # set up firebase
        self.firebaseConfig = { 
          "apiKey": "AIzaSyA1XkaqnfFO8pm-yuTK5ggZpAsY27eOwn8", 
          "authDomain": "connected-temp-sensor.firebaseapp.com", 
          "databaseURL": "https://connected-temp-sensor-default-rtdb.firebaseio.com", 
          "projectId": "connected-temp-sensor", 
          "storageBucket": "connected-temp-sensor.appspot.com", 
          "messagingSenderId": "363436241273", 
          "appId": "1:363436241273:web:3404021c99f76d3ed2bfa8", 
          "measurementId": "G-CD08HW864M" 
        }                     

        #instantiate variables to keep track of program
        self.firebaseDatabase = pyrebase.initialize_app(self.firebaseConfig).database()
        self.last300 = []
        self.virtualButtonPressed = False
        self.lastTempReading = None

        self.firebaseDatabase.child("virtual_button_pressed").stream(self.virtualButton)

        self.lcd.backlight = True
        self.lcd.message = "Powering on :)"
        time.sleep(5.0)

    def updateTempReading(self):
        
        temp = ""
        
        if (self.powerSwitchState == False):
            temp = "DNA"
        else:
            temp = TempReader.getTemp()
        
        self.lastTempReading = temp
        
        if (len(self.last300) < 300):
            self.last300.append(self.lastTempReading)
        else:
            self.last300.pop(0)
            self.last300.append(self.lastTempReading)
        
        self.firebaseDatabase.update({"last_300_seconds" : self.last300})
        print("last T reading = " + temp)
        
        if (self.lastTempReading == "US"):
            time.sleep(0.8)
        elif (self.lastTempReading == "DNA"):
            time.sleep(0.9)
        
        self.t = Timer(0.1, self.updateTempReading)
        self.t.start()


    #firebase listener function
    def virtualButton(self, event):
        self.virtualButtonPressed = event["data"]
        print(event["data"])

    # main controll loop
    def run(self):
        
        # begin reading t values
        self.t = Timer(0.1, self.updateTempReading)
        self.t.start()
        
        while (True):
            
            self.buttonState = GPIO.input(self.button)
            self.powerSwitchState = GPIO.input(self.powerSwitch)
            
            if (self.powerSwitchState != False):
                
                if (self.buttonState == False or self.virtualButtonPressed == "True"):

                    self.lcd.backlight = True
                    
                    if (self.lastTempReading != "US"):
                    
                        self.lcd.message = TempReader.convertToDisplayFormat(self.lastTempReading)
                    else:
                        self.lcd.message = "Sensor Unplugged"
                
                else:
                    self.lcd.backlight = False
                    self.lcd.clear()
                    self.updatedSinceLastTempReading = True
                
                time.sleep(0.05)
            
            else:
                
                
                self.lcd.backlight = True
                self.lcd.message = "Powering off :("
                time.sleep(2)
                self.lcd.backlight = False
                self.lcd.clear()
                
                while (self.powerSwitchState == False):
                    
                    time.sleep(2)
                    self.powerSwitchState = GPIO.input(self.powerSwitch)
                
                self.lcd.backlight = True
                self.lcd.message = "Powering on :)"
                time.sleep(2.5)
                self.lcd.clear()
                self.lcd.backlight = False
            
        
        
        



        
        

