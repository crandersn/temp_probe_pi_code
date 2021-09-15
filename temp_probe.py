from datetime import datetime
import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import time
import os
import glob

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
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

        
def get_temp(): #Fundtion to read the value of Temperature
    file = open(device_file, 'r') #opent the file
    lines = file.readlines() #read the lines in the file
    file.close() #close the file
             
    trimmed_data = lines[1].find('t=') #find the "t=" in the line
               
    if trimmed_data != -1:
        temp_string = lines[1][trimmed_data+2:] #trim the strig only to the temoerature value        
        return temp_string
    else: 
        return "empty"

def convertToDisplayFormat(inputTemp):
    
    return inputTemp[:2] + "." + inputTemp[2:].strip() + " Celcius"
    


'''lcd.clear()
lcd.backlight = True
lcd.message = get_temp()
time.sleep(4)
lcd.clear()
lcd.backlight = False'''


i = 0
lcd.backlight = True
while (i < 3):
    i = i + 1
    lcd.message = convertToDisplayFormat(get_temp())
    time.sleep(2)
    
    

