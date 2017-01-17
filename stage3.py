from breezycreate2 import Robot

import time

bot = Robot()
bot.playNote('A1', 100)

# while rain and car is on...


def solve():
    while True:
        bot.moveForward()
        leftBump, rightBump = bot.getBumpers()
        if leftBump and rightBump:
          #  bot.moveDistance(-0.05)    
            if bot.bumpedRecently(3):
                bot.rotate(180)
            else:
                bot.rotate(-90)
              
        elif leftBump:
                bot.rotate(10)
        elif rightBump:
                bot.rotate(-10)

def solve2():
    while True:
        bot.moveForward()
        bot.updateBumpers()
        if bot.leftBump and bot.rightBump:
          #  bot.moveDistance(-0.05)    
            if bot.bumpedRecently(3):
                bot.rotate(180)
            else:
                bot.rotate(-90)
              
        elif bot.leftBump:
                bot.rotate(10)
        elif bot.rightBump:
                bot.rotate(-10)

solve2()