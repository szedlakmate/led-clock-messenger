import os
import threading
import time


print('Start: Clock')
t = threading.Thread(target=os.system("sudo -H nohup python3 /home/pi/Projects/led-clock-messenger/LED_clock.py >/dev/null &"))
t.start()

print('Start: Messenger')
t = threading.Thread(target=os.system("sudo -H nohup python3 /home/pi/Projects/led-clock-messenger/messenger.py >/dev/null &"))
t.start()
