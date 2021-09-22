from threading import Timer
import pyrebase
from TempReader import TempReader
from AwsTimeStream import TimeStream
from datetime import datetime
import RPi.GPIO as GPIO
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import time
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
    

def printTemp():
    print(TempReader.getTemp())
    t = Timer(5.0, printTemp)
    t.start()


'''
i = 0
lcd.backlight = True
lcd.clear()
while (1):
    #i = i + 1
    #lcd.message = convertToDisplayFormat(get_temp())
    
    buttonState = GPIO.input(button)
    
    if (buttonState == False):

        lcd.message = convertToDisplayFormat(get_temp())
        time.sleep(2)
        lcd.clear()
    
    time.sleep(.01)'''


# code to write to the timeseries database
lcd.backlight = False

#firebase listener function
def virtualButton(event):
    print(event["data"])
  
  
timeStreamDB = TimeStream('past_temperatures', 'last_300_seconds', 'us-east-2')
timeStreamDB.write(TempReader.getTemp())

firebaseDatabase = pyrebase.initialize_app(firebaseConfig).database()
firebaseDatabase.child("notify").stream(virtualButton)

t = Timer(5.0, printTemp)
t.start()

while (True):
    
    print("looping")
    time.sleep(2)
    
    
    



    
    

