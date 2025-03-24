import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
import os
import time

login = "login" #gebruikersnaam hier invullen
ww = "ww" #wachtwoord hier invullen
database = "deurbel"

#pins van de LED en button
LED_PIN = 4
BUTTON_PIN = 17

#pins van het LCD scherm
LCD_RS = 27
LCD_E = 22
LCD_D4 = 25
LCD_D5 = 24 
LCD_D6 = 23
LCD_D7 = 18
LCD_BUTTON = 5
LCD_COLUMNS = 16
LCD_ROWS = 2
LCD_BACKLIGHT = 0


lcd = LCD.Adafruit_CharLCD(LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7, LCD_COLUMNS, LCD_ROWS, LCD_BACKLIGHT)
 

version="/home/pi/deurbel/deurbel.py"
os.environ['TZ'] = 'Europe/Amsterdam'
now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
db = "false"
go = "true"


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)  # om te zorgen dat het induwen is
GPIO.setup(LED_PIN, GPIO.OUT) 