from breezycreate2 import Robot

import time

bot = Robot()
bot.playNote('A1', 100)


def solve():
    lastBump = 0
    while True:
        bot.moveForward()
        bumpers = bot.getBumpers()
        if bumpers[0] and bumpers[1]:
            bot.setForwardDistance(-0.05)
            bumpTime = time.time()
            if time.time() - lastBump > 3:
                bot.setTurnAngle(-90)
            else:
                bot.setTurnAngle(180)
            lastBump = bumpTime
            
        elif bumpers[0]:
                bot.setTurnAngle(10)
        elif bumpers[1]:
                bot.setTurnAngle(-10)

solve()