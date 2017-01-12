from breezycreate2 import Robot
import time

bot = Robot()
bot.playNote('A1', 100)

print "Going Forward"
bumps = 0

while True:
	bot.robot.digit_led_ascii(str(bumps).zfill(4))

	wallSensor = bot.getWallSensors()
	frontWall= wallSensor[3]
	leftWall =  wallSensor[5]
	rightWall =  wallSensor[0]
	rightFrontWall = wallSensor[1]


	if leftWall > 15 and frontWall < 20:
		print "Adjusting right"
		bot.setTurnSpeed(200)
		time.sleep(0.05)
		bot.setTurnSpeed(0)

	if rightWall > 200 or (frontWall < 15 and rightFrontWall > 20 and rightWall < 10):
		print "Adjusting left"
		bot.setTurnSpeed(-200)
		time.sleep(0.05)
		bot.setTurnSpeed(0)

	print "left: ", leftWall, "front: ", frontWall, "right: ", rightWall, rightFrontWall
	bot.setForwardSpeed(200)
	
	if frontWall > 150:
		bot.setForwardSpeed(0)
		if rightWall > 5:
			print "Turning left"
			bot.setTurnSpeed(-200)
			time.sleep(1)
			bot.setTurnSpeed(0)
		elif leftWall > 20:
			print "Turning right"
			bot.setTurnSpeed(200)
			time.sleep(1)
			bot.setTurnSpeed(0)
		else:
			"OOOPS"

	bumpers = bot.getBumpers()

	if bumpers[0] or bumpers[1]:
		bumps += 1
		if bumpers[0]:
			bot.setTurnSpeed(200)
			time.sleep(0.05)
			bot.setTurnSpeed(0)
		if bumpers[1]:
			bot.setTurnSpeed(-200)
			time.sleep(0.05)
			bot.setTurnSpeed(0)
