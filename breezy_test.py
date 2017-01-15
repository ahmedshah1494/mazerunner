from breezycreate2 import Robot
import time
import math

bot = Robot()
if not bot.isConnected():
	exit()
bot.playNote('A1', 100)
#bot.turnLeft()
#bot.turnRight()



bot.setTurnAngle(90)
bot.setTurnAngle(-90)
time.sleep(0.1)
bot.close()