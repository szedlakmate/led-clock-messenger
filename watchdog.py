"""
This program was written by Máté Szedlák (C) 2018 (szedlakmate@gmail.com). All rights reserved.

Source:
https://github.com/szedlakmate/led-clock-messenger/
"""


import os
import threading
import time
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import select, update, asc, desc

engine = create_engine('mysql://root@localhost/messenger')


def startprgm(cmd, delay=0):
    try:
        time.sleep(delay)
        print("Executing" + cmd)
        os.system(cmd)
    except:
        print("Restart exception")


def get_command():
    try:
        meta = MetaData(engine)
        commands = Table('commands', meta, autoload=True)  
        sel = select([commands.c.command, commands.c.id]).where(commands.c.shown == False).order_by(asc(commands.c.sent)).limit(1)
        item = engine.execute(sel).first()
        if type(item[0]) == type('A'):
            engine.execute("UPDATE commands SET shown=True WHERE ID =" + str(item[1]))
            cmd = item[0]
        else:
            cmd = ""
        if type(cmd) != type(""):
            print(type(cmd))
            cmd = ""
        return cmd
    except:
        # print("Unexpected error:", sys.exc_info()[0])
        return ""


# Infinite loop to drive the watchdog
while True:
    command = get_command()
    if len(command) > 0:
        t = threading.Thread(target=startprgm(command, 3))
        t.start()
    time.sleep(3)
