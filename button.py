import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
import os
import time
import sys

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
 

os.environ['TZ'] = 'Europe/Amsterdam'
now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
db = "false"
go = "true"


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN)  # om te zorgen dat het induwen is
GPIO.setup(LED_PIN, GPIO.OUT) 


# deurbel indrukken
def DoorbellPressed(channel):
    global now
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print(now)
    print("Button Pressed")

    GPIO.output(LED_PIN, GPIO.HIGH)  # zet led aan
    time.sleep(3)  # houd led aan voor 3 seconden
    GPIO.output(LED_PIN, GPIO.LOW)

    writeTodatabase() # sla op in database dat er aangebeld is



# opslaan in database
def writeTodatabase():
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
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

# haal laatste twee timestamps op uit de database
def getLastTwoEntries():
    try:
        con = mdb.connect(host='localhost', user=login, password=ww, database=database)
        with con:
            cur = con.cursor()
            cur.execute("SELECT tijd FROM deurbel ORDER BY tijd DESC LIMIT 2")
            rows = cur.fetchall()  # haal laatste twee rijen
            cur.close()
            return [str(row[0]) for row in rows] if rows else ["No Data", "Check DB"]
    except Exception as e:
        print("Database Error:", e)
        return ["No Data", "Check DB"]
    

# update lcd met laatste twee timestamps
def updateLcd():
    records = getLastTwoEntries()
    lcd.clear()
    lcd.message("{}\n{}".format(records[0], records[1]))  # laat laatste twee entries zien




# main loop
print("Program started.")
print("Control-C om te stoppen")

GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=DoorbellPressed, bouncetime=200)

try:
    while True:
	updateLcd()
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping program.")
    lcd.clear()
    GPIO.cleanup()