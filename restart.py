import os
import threading
import time

def startprgm(command, delay=0):
    try:
        time.sleep(delay)
        os.system(command)
    except:
        print("Restart exception")

print('Stop: Clock and Messenger')

try:
    t = threading.Thread(target=startprgm("sudo kill -9 $(ps ax | grep 'startup.py' | fgrep -v grep | awk '{ print $1 }')"))
    t.start()
except:
    print('Failed: kill startup.py')

try:
    t = threading.Thread(target=startprgm("sudo kill -9 $(ps ax | grep 'LED_clock.py' | fgrep -v grep | awk '{ print $1 }')"))
    t.start()
except:
    print('Failed: kill Clock')

try:
    t = threading.Thread(target=startprgm("sudo kill -9 $(ps ax | grep 'messenger.py' | fgrep -v grep | awk '{ print $1 }')"))
    t.start()
except:
    print('Failed: kill messenger')

try:
    t = threading.Thread(target=startprgm("sudo kill -9 $(ps ax | grep 'watchdog.py' | fgrep -v grep | awk '{ print $1 }')"))
    t.start()
except:
    print('Failed: kill watchdog')

print('Start: Clock and Messenger')
t = threading.Thread(target=startprgm("sudo -H nohup python3 /home/pi/startup.py >/dev/null &"))
t.start()


try:
    t = threading.Thread(target=startprgm("sudo kill -9 $(ps ax | grep 'restart.py' | fgrep -v grep | awk '{ print $1 }')", 10))
    t.start()

except:
    print('Failed: kill restart.py')
