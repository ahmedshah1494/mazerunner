from breezycreate2 import Robot

import time

bot = Robot()
bot.playNote('A1', 100)


def solve():
    lastBump = 0
    while True:
        bot.setForwardSpeed(200)
        bumpers = bot.getBumpers()
        if bumpers[0] and bumpers[1]:
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

        elif bumpers[0]:
                bot.setTurnSpeed(200)
                time.sleep(0.05)
                bot.setTurnSpeed(0)
        elif bumpers[1]:
                bot.setTurnSpeed(-200)
                time.sleep(0.05)
                moveTime += 0.05
                bot.setTurnSpeed(0)

solve()