"""
This program was written by Máté Szedlák (C) 2018 (szedlakmate@gmail.com). All rights reserved.

Source:
https://github.com/szedlakmate/led-clock-messenger/
"""

# import sys
# import time
import datetime
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
# import adafruit.adafruitgfx as adafruitgfx
from Adafruit_LED_Backpack import Matrix8x8
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select, update, asc, desc

engine = create_engine('mysql://root@localhost/messenger')

# Create display instance on default I2C address (0x70) and bus number.
display = Matrix8x8.Matrix8x8()

# Alternatively, create a display with a specific I2C address and/or bus.
# display = Matrix8x8.Matrix8x8(address=0x74, busnum=1)

# Initialize the display. Must be called once before using the display.
display.begin()

digits = [
    [],
    []]

display.set_brightness(1)


def get_message():
    try:
        meta = MetaData(engine)
        messages = Table('messages', meta, autoload=True)  
        sel = select([messages.c.message, messages.c.id]).where(messages.c.shown == False).order_by(asc(messages.c.sent)).limit(1)
        item = engine.execute(sel).first()
        if type(item[0]) == type('A'):
            engine.execute("UPDATE messages SET shown=True WHERE ID =" + str(item[1]))
            msg = item[0]
            #print(msg)
        else:
            msg = ""
            
        if type(msg) != type(""):
            print(type(msg))
            msg = ""
        return msg
    except:
        # print("Unexpected error:", sys.exc_info()[0])
        return ""


# Infinite loop to drive the clock
while True:
    now = datetime.datetime.now()
    
    message = get_message()
    """
    if  now.second < -3:
        display.clear()
        image = Image.new('1', (8, 8))
        draw = ImageDraw.Draw(image)
        draw.text((0,0), str(now.hour), fill=255)
        display.set_image(image)
        display.write_display()
        time.sleep(3)
        #show_hour_skipthisloop--
    #else:
        #show_hour_skipthisloop = 3
    """
    if now.minute % 5 == 0 and now.second < 7:
        display.clear()
        image = Image.new('1', (54, 8))
        draw = ImageDraw.Draw(image)
        draw.text((0,-2),'Szeretlek', fill=255)
        display.animate(display.horizontal_scroll(image), 0.12)
        
    if len(message) > 0:
        display.clear()
        image = Image.new('1', (len(message)*6+2, 8))
        draw = ImageDraw.Draw(image)
        draw.text((0,-2), message, fill=255)
        display.animate(display.horizontal_scroll(image), 0.12)
    
    minute_to_show = str(now.minute) if now.minute >= 10 else '0' + str(now.minute)
    time_to_show = str(now.hour) + ':' + minute_to_show
    display.clear()
    image = Image.new('1', (30, 8))
    draw = ImageDraw.Draw(image)
    draw.text((0,-2), time_to_show, fill=255)
    display.animate(display.horizontal_scroll(image), 0.12)

    # time.sleep(0.1)

# See the SSD1306 library for more examples of using the Python Imaging Library
# such as drawing text: https://github.com/adafruit/Adafruit_Python_SSD1306
