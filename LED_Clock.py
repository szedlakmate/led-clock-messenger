# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import sys
import time
import datetime
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

#import adafruit.adafruitgfx as adafruitgfx

from Adafruit_LED_Backpack import Matrix8x8

from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select, update, asc, desc

# Create an engine to the census database
engine = create_engine('mysql://root@localhost/messenger')
 #result = connection.execute(____).first()
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/messenger'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suggested by SQLAlchemy
#db = SQLAlchemy(app)

"""
# Calendar types model
class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(80), unique=True, nullable=False)
    shown = db.Column(db.Boolean, unique=False, nullable=False, default = False)
    sent = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, message):
        self.message = message
        self.shown = False
        #self.sent = datetime.datetime.utcnow

    def __repr__(self):
        return self.message

"""
# Create display instance on default I2C address (0x70) and bus number.
display = Matrix8x8.Matrix8x8()

# Alternatively, create a display with a specific I2C address and/or bus.
# display = Matrix8x8.Matrix8x8(address=0x74, busnum=1)

# Initialize the display. Must be called once before using the display.
display.begin()

igits = [
    [],
    []]

"""
# Run through each pixel individually and turn it on.
for x in range(8):
	for y in range(8):
		# Clear the display buffer.
		display.clear()
		# Set pixel at position i, j to on.  To turn off a pixel set
		# the last parameter to 0.
		display.set_pixel(x, y, 1)
		# Write the display buffer to the hardware.  This must be called to
		# update the actual display LEDs.
		display.write_display()
		# Delay for half a second.
		time.sleep(0.5)

# Draw some shapes using the Python Imaging Library.

# Clear the display buffer.
display.clear()

# First create an 8x8 1 bit color image.
image = Image.new('1', (8, 8))

# Then create a draw instance.
draw = ImageDraw.Draw(image)

# Draw a rectangle with colored outline
draw.rectangle((0,0,7,7), outline=255, fill=0)

# Draw an X with two lines.
draw.line((1,1,6,6), fill=255)
draw.line((1,6,6,1), fill=255)

# Draw the image on the display buffer.
display.set_image(image)

# Draw the buffer to the display hardware.
display.write_display()
"""

#parent_conn,child_conn = Pipe()
#p = Process(target=send, args=(child_conn,))
#p.start()
#print(parent_conn.recv())   # prints "Hello"

#font = ImageFont.load_default()
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
            print(msg)
        else:
            msg = ""
            
        if type(msg) != type(""):
            print(type(msg))
            msg = ""
        return msg
    except:
        #print("Unexpected error:", sys.exc_info()[0])
        return ""

while True:
    now = datetime.datetime.now()
    
    message = get_message()
    
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
    #display.set_image(image)
    #display.write_display()
    display.animate(display.horizontal_scroll(image), 0.12)
  		
    #time.sleep(0.1)

# See the SSD1306 library for more examples of using the Python Imaging Library
# such as drawing text: https://github.com/adafruit/Adafruit_Python_SSD1306
