import os
from breezycreate2 import Robot
import time

f = os.popen('ifconfig  wlan0 | grep "inet addr:"| grep -v "127.0.0.1" | cut -d: -f2')
myIP = f.read()

bot = Robot()

while True:

	ip = myIP
	for i in range(2):
		bot.robot.digit_led_ascii(str(" ip ").zfill(4))
		time.sleep(0.5)
		bot.robot.digit_led_ascii(str("    ").zfill(4))
		time.sleep(0.5)
	
	while len(ip) >= 4:
		bot.robot.digit_led_ascii(str(ip[:4]).zfill(4))
		time.sleep(0.4)
		ip = ip[1:]
	time.sleep(1)
	