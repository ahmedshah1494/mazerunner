from breezycreate2 import Robot


bot = Robot()
if not bot.isConnected():
	exit()
bot.playNote('A1', 100)
#bot.turnLeft()
#bot.turnRight()

bot.setForwardDistanceSmart(1)

#bot.close()