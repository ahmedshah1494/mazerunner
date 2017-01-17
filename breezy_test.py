from breezycreate2 import Robot
import time
import math

bot = Robot()
if not bot.isConnected():
	exit()
bot.playNote('A1', 100)
#bot.turnLeft()
#bot.turnRight()
