from breezycreate2 import Robot
import time

bot = Robot()
bot.playNote('A1', 100)

print "Going Forward"
bumps = 0
lastBump = 0
bot.setForwardSpeed(200)
while True:
	bot.robot.digit_led_ascii(str(bumps).zfill(4))

	bumpers = bot.getBumpers()

	if bumpers[0] or bumpers[1]:
		bot.setForwardSpeed(-200)
		time.sleep(0.25)
		bot.setForwardSpeed(0)
		bumpTime = time.time()
		if time.time() - lastBump > 3:
			print "Turning left"
			bot.setTurnSpeed(-200)
			time.sleep(1)
			bot.setTurnSpeed(0)
		else:
			print "Turning right"
			bot.setTurnSpeed(200)
			time.sleep(2)
			bot.setTurnSpeed(0)
		
		bot.setForwardSpeed(200)

		lastBump = bumpTime
