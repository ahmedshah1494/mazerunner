from breezycreate2 import Robot


bot = Robot()
if not bot.isConnected():
	exit()
bot.playNote('A1', 100)
bot.setForwardSpeed(-200)
bot.turnLeft()
bot.turnRight()

#bot.close()