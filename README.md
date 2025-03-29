# bp6-deurbel

## Handleiding

Om dit project te kunnen draaien, moeten de files op de Raspberry Pi staan, zorg dat de paden kloppen zoals te vinden in button.py. Voor lamp_blink moet een virtual env worden aangemaakt, omdat deze draait op python3 en button.py gebruikt python2.

Import vervolgens alles dat staat bij de imports, zowel in button.py als lamp_blink.py. Dit kan je doen door bijvoorbeeld het commando "pip install" met daarachter welke library je wil installeren te runnen in de terminal. Bij de from x import y, installeer dan x.

In dit project is er al verbonden met de Philips Hue bluetooth lamp die wij hebben en is het MAC adres al gevonden. Om de lamp te vinden, zet de lamp in pairing mode, bij een nieuwe lamp gebeurt dit automatisch bij het opstarten. Run dan "sudo bluetoothctl" in de terminal, en daarna "scan on". Dan moet je het MAC adres opschrijven en run je "pair" met daarachter het MAC adres en "trust" en daarachter het MAC adress. Dan ben je verbonden met de lamp, en kan je het MAC adress in dit project vervangen met het MAC adress van jouw lamp.

## Automatisch opstarten

De crontab is aangepast zodat start.sh word gerund op het moment dat de Pi aangaat, zodat het programma niet meer handmatig hoeft te worden opgestart.