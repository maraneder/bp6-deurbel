import time
from libhueble import Lamp
import asyncio

async def main():
    # Creeer een lamp objext van het bluetooth MAC adress van de lamp 
    l = Lamp('EA:A4:D2:58:9D:4B')
    await l.connect()
    await l.set_power(False)
    await l.set_color_rgb(1,1,1)
    await l.set_brightness(1.0)

    for i in range(5):
        await l.set_power(False)
        time.sleep(2)
        await l.set_power(True)
        time.sleep(2)

    await l.set_power(False)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())