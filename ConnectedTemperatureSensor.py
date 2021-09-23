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

# set up LCD
lcd_columns = 16
lcd_rows = 2

lcd_rs = digitalio.DigitalInOut(board.D22)
lcd_en = digitalio.DigitalInOut(board.D17)
lcd_d4 = digitalio.DigitalInOut(board.D25)
lcd_d5 = digitalio.DigitalInOut(board.D24)
lcd_d6 = digitalio.DigitalInOut(board.D23)
lcd_d7 = digitalio.DigitalInOut(board.D18)
backlight_d8 = digitalio.DigitalInOut(board.D8)

lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, backlight_d8)


# configure system to read temperature probe
os.system('modprobe w1-gpio') 
os.system('modprobe w1-therm')

#set up button
button = 16
GPIO.setup(button, GPIO.IN,pull_up_down=GPIO.PUD_UP)

# set up switch


# set up firebase
firebaseConfig = { 
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
firebaseDatabase = pyrebase.initialize_app(firebaseConfig).database()
last300 = []
virtualButtonPressed = False
lastTempReading = None

def updateTempReading():
    
    temp = TempReader.getTemp()
    global lastTempReading
    lastTempReading = temp
    
    global last300
    
    if (len(last300) < 10):
        last300.append(lastTempReading)
    else:
        last300.pop(0)
        last300.append(lastTempReading)
    
    firebaseDatabase.update({"last_300_seconds" : last300})
    print("last T reading = " + temp)
    t = Timer(1.0, updateTempReading)
    t.start()


#firebase listener function
def virtualButton(event):
    global virtualButtonPressed
    virtualButtonPressed = event["data"]
    print(event["data"])

firebaseDatabase.child("virtual_button_pressed").stream(virtualButton)

# begin reading t values
t = Timer(1.0, updateTempReading)
t.start()

lcd.backlight = True
lcd.message = "Powering on :)"
time.sleep(5.0)

# main controll loop
while (True):
    
    buttonState = GPIO.input(button)
    
    if (buttonState == False or virtualButtonPressed == "True"):

        lcd.backlight = True
        
        if (lastTempReading != "US"):
        
            lcd.message = TempReader.convertToDisplayFormat(lastTempReading)
        else:
            lcd.message = "Sensor Unplugged"
    
    else:
        lcd.backlight = False
        lcd.clear()
        updatedSinceLastTempReading = True
    
    time.sleep(0.05)
    
    
    
    



    
    

