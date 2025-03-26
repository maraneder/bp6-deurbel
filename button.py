import RPi.GPIO as GPIO
import MySQLdb as mdb
import sys
import os
import glob
import time
import smbus
import smtplib
import urllib
from itertools import cycle
from time import sleep

login = "login" #gebruikersnaam hier invullen
ww = "ww" #wachtwoord hier invullen
database = "deurbel"

#pins van de LED en button
LED_PIN = 4
BUTTON_PIN = 17
LCD_BUTTON = 5

#pins van het LCD scherm
LCD_RS = 27
LCD_EN = 22
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18

LCD_WIDTH = 16  
LCD_CHR = True  
LCD_CMD = False 
E_PULSE = 0.0005
E_DELAY = 0.0005

# GPIO Setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


GPIO.setup(LCD_EN, GPIO.OUT)
GPIO.setup(LCD_RS, GPIO.OUT)
GPIO.setup(LCD_D4, GPIO.OUT)
GPIO.setup(LCD_D5, GPIO.OUT)
GPIO.setup(LCD_D6, GPIO.OUT)
GPIO.setup(LCD_D7, GPIO.OUT)

last_pressed_time = None

def lcd_init():
    lcd_command(0x33)  
    lcd_command(0x32) 
    lcd_command(0x28)  
    lcd_command(0x0C)  
    lcd_command(0x06)  
    lcd_command(0x01)  
    time.sleep(E_DELAY)
 

os.environ['TZ'] = 'Europe/Amsterdam'
now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
db = "false"
go = "true"


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)  # om te zorgen dat het induwen is
GPIO.setup(LED_PIN, GPIO.OUT) 
GPIO.setup(LCD_BUTTON, GPIO.IN, GPIO.PUD_UP)


# deurbel indrukken
def doorbellPressed(channel):
    global now
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print(now)
    print("Button Pressed")

    GPIO.output(LED_PIN, GPIO.HIGH)  # led aan
    lcd_display("Doorbell Pressed", 1)
    lcd_display(now, 2) 

    time.sleep(3)  # led aanhouden voor 3 seconden
    GPIO.output(LED_PIN, GPIO.LOW)

    # leeg line 1 en 2
    lcd_display("                ", 1)  
    lcd_display("                ", 2)  


    writeTodatabase()


# opslaan in database
def writeTodatabase():
    # zorg dat de button niet dubbel doorgeeft
    # dus maar een keer per minuut opslaan
    global last_pressed_time
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    current_minute = now[:16]

    if last_pressed_time is None or current_minute != last_pressed_time:
        try:
            con = mdb.connect(host='localhost', user=login, password=ww, database=database)
            db="true"
            with con:
                cur = con.cursor()
                cur.execute("INSERT INTO deurbel(tijd) VALUES (%s)", (now,))
	        con.commit()
                print("Data weggeschreven in database ")
	        cur.close()
        except:
            print('Er is geen verbinding met de database')
            print("Unexpected error:", sys.exc_info()[0])
            db="false"
    else: 
        print("Button pressed within same minute, skipping database write")



# send command
def lcd_command(bits):
    GPIO.output(LCD_RS, LCD_CMD)
    lcd_write(bits)

# send data
def lcd_data(bits):
    GPIO.output(LCD_RS, LCD_CHR)
    lcd_write(bits)

# write functie
def lcd_write(bits):
    GPIO.output(LCD_D4, bool(bits & 0x10))
    GPIO.output(LCD_D5, bool(bits & 0x20))
    GPIO.output(LCD_D6, bool(bits & 0x40))
    GPIO.output(LCD_D7, bool(bits & 0x80))
    lcd_toggle_enable()
    
    GPIO.output(LCD_D4, bool(bits & 0x01))
    GPIO.output(LCD_D5, bool(bits & 0x02))
    GPIO.output(LCD_D6, bool(bits & 0x04))
    GPIO.output(LCD_D7, bool(bits & 0x08))
    lcd_toggle_enable()

# toggle enable pin
def lcd_toggle_enable():
    time.sleep(E_DELAY)
    GPIO.output(LCD_EN, True)
    time.sleep(E_PULSE)
    GPIO.output(LCD_EN, False)
    time.sleep(E_DELAY)

# toon text
def lcd_display(message, line):
    if line == 1:
        lcd_command(0x80)  # Line 1
    elif line == 2:
        lcd_command(0xC0)  # Line 2

    message = message.ljust(LCD_WIDTH, " ")
    for char in message:
        lcd_data(ord(char))





# haal laatste twee timestamps op uit de database
def getLastTwoEntries():
    try:
        # connect met de mysql database
        con = mdb.connect(host='localhost', user=login, password=ww, database=database)
        with con:
            cur = con.cursor()
            cur.execute("SELECT tijd FROM deurbel ORDER BY tijd DESC LIMIT 2")  # haal laatste twee timestamps op
            timestamps = cur.fetchall()  
            return timestamps
    except mdb.Error as e:
        print("Error: Unable to fetch data from database", e)
        return []

    

def historyPressed(channel):
    timestamps = getLastTwoEntries()

    if len(timestamps) == 2:
        # toon op display
        lcd_display("{}".format(timestamps[0][0]), 1)
        lcd_display("{}".format(timestamps[1][0]), 2)
    else:
        # als er een of minder zijn
        lcd_display("No timestamps found", 1)
        lcd_display("or only one press", 2)



lcd_init()
lcd_display("Doorbell System", 1)
lcd_display("Press Button", 2)




# main loop
print(time.strftime('%d-%m-%Y %H:%M:%S', time.localtime()))
print("Program started.")
print("Control-C om te stoppen")

GPIO.add_event_detect(LCD_BUTTON, GPIO.RISING, callback=historyPressed, bouncetime=1000)
GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=doorbellPressed, bouncetime=1000)


try:
    while True:
        time.sleep(1)  
except KeyboardInterrupt:
    print("Stopping program.")
    lcd_command(0x01)
    GPIO.cleanup()
