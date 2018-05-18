"""
This program was written by Máté Szedlák (C) 2018 (szedlakmate@gmail.com). All rights reserved.

Source:
https://github.com/szedlakmate/led-clock-messenger/
"""


import datetime
import time
import sys
#from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
# import adafruit.adafruitgfx as adafruitgfx
from Adafruit_LED_Backpack import Matrix8x8
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select, update, asc, desc
from weather import Weather, Unit


def weather_api_request(loc_identifier, unit):
    if unit.capitalize() == 'F':
        weather = Weather(unit='f')
    else:
        weather = Weather(unit=Unit.CELSIUS)
    if type(loc_identifier) == type('budapest'):
        location = weather.lookup_by_location(loc_identifier)
    elif type(loc_identifier) == type([47.4801247, 19.2519299]):
        location = weather.lookup_by_latlng(loc_identifier[0], loc_identifier[1])

    return location.condition


def get_message(engine):
        try:
            meta = MetaData(engine)
            messages = Table('messages', meta, autoload=True)
            sel = select([messages.c.message, messages.c.id]).where(messages.c.shown == 0).order_by(
                asc(messages.c.sent)).limit(1)
            item = engine.execute(sel).first()
            if item is not None and type(item[0]) == type('A'):
                engine.execute("UPDATE messages SET shown=True WHERE ID =" + str(item[1]))
                msg = item[0]
                print(msg)
            else:
                msg = ""

            if type(msg) != type(""):
                print(type(msg))
                msg = ""
            return msg
        except:
            print("Unexpected error:", sys.exc_info())
            return ""


class Clock(object):
    def __init__(self):
        self.displays = [Matrix8x8.Matrix8x8(address=0x74), Matrix8x8.Matrix8x8(address=0x72), Matrix8x8.Matrix8x8(address=0x70)]
        self.prev_api_req_time = datetime.datetime.now() - datetime.timedelta(minutes=60)
        self.condition = weather_api_request([47.4794433, 19.2530735], 'c')
        self.engine = create_engine('mysql+pymysql://messenger:demopassword@localhost/messenger')

    def weather(self, location, unit='c', refresh_interval=20):
        current_api_req_time = datetime.datetime.now()
        if current_api_req_time - self.prev_api_req_time >= datetime.timedelta(minutes=refresh_interval):
            self.prev_api_req_time = current_api_req_time
            try:
                self.condition = weather_api_request(location, unit)
                print('Weather updated')
            except:
                print('Weather update API error: ', sys.exc_info())
                return ''

        report = self.condition.temp + '°C'
        return report

    def set_auto_brightness(self):
        if (datetime.datetime.now().hour > 7) and (datetime.datetime.now().hour < 20):
            BRIGHTNESS = 15
        else:
            BRIGHTNESS = 1
        for i in range(3):
            self.displays[i].set_brightness(BRIGHTNESS)

    def multi_draw(self, images):
        for i in range(3):
            self.displays[i].set_image(images[i*8+8].rotate(270))
            # Draw the buffer to the display hardware
            self.displays[i].write_display()

    def multi_animate(self, images, delay=.25):
        """Displays each of the input images in order, pausing for "delay"
        seconds after each image.

        Keyword arguments:
        image -- An iterable collection of Image objects.
        delay -- How many seconds to wait after displaying an image before
            displaying the next one. (Default = .25)
        """
        canvas = [Image.new('1', (8, 8))] * 16

        for image in images:
            canvas.append(image)

        for i in range(16):
            canvas.append(Image.new('1', (8, 8)))

        for i in range(len(canvas) - 16):
            # Draw the image on the display buffer.
            multi_image = [canvas[i], canvas[i + 8], canvas[i + 8 * 2]]
            for i in range(3):
                self.displays[i].set_image(multi_image[i].rotate(270))
                # Draw the buffer to the display hardware.
                self.displays[i].write_display()
            time.sleep(delay)

    def write_loop(self):
        # Infinite loop to drive the clock
        while True:
            #try:
                self.set_auto_brightness()
                now = datetime.datetime.now()

                message = get_message(self.engine)
                """
                if  now.second < -3:
                    self.display.clear()
                    image = Image.new('1', (8, 8))
                    draw = ImageDraw.Draw(image)
                    draw.text((0,0), str(now.hour), fill=255)
                    self.display.set_image(image)
                    self.display.write_display()
                    time.sleep(3)
                    #show_hour_skipthisloop--
                #else:
                    #show_hour_skipthisloop = 3
                """
                if now.second < 8:
                    image = Image.new('1', (30, 8))
                    draw = ImageDraw.Draw(image)
                    draw.text((0, -2), self.weather([47.4801247, 19.2519299]), fill=255)
                    self.multi_animate(self.displays[0].horizontal_scroll(image), 0.12)

                if now.minute % 5 == 0 and now.second < 14:
                    image = Image.new('1', (54, 8))
                    draw = ImageDraw.Draw(image)
                    draw.text((0, -2), 'Szeretlek', fill=255)
                    self.multi_animate(self.displays[0].horizontal_scroll(image), 0.12)

                if len(message) > 0:
                    image = Image.new('1', (len(message) * 6 + 2, 8))
                    draw = ImageDraw.Draw(image)
                    draw.text((0, -2), message, fill=255)
                    self.multi_animate(self.displays[0].horizontal_scroll(image), 0.12)


                minute_to_show = str(now.minute) if now.minute >= 10 else '0' + str(now.minute)
                time_to_show = str(now.hour) + minute_to_show
                # self.multi_clear()
                image = Image.new('1', (30, 8))
                draw = ImageDraw.Draw(image)
                draw.text((0, -2), time_to_show, fill=255)
                self.multi_draw(self.displays[0].horizontal_scroll(image))
                time.sleep(0.5)
                # See the SSD1306 library for more examples of using the Python Imaging Library
                # such as drawing text: https://github.com/adafruit/Adafruit_Python_SSD1306
            #except Exception:
                pass
                #print(str(time.time()) + 'Error: Print failure')

    def start(self):
        # Create display instance on default I2C address (0x70) and bus number.

        # Alternatively, create a display with a specific I2C address and/or bus.
        # display = Matrix8x8.Matrix8x8(address=0x74, busnum=1)

        # Initialize the display. Must be called once before using the display.
        for i in range(3):
            self.displays[i].begin()

        digits = [
            [],
            []]
        self.write_loop()

CLOCK = Clock()
CLOCK.start()
