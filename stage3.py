from breezycreate2 import Robot

import time


robot = Robot()

def solve():
    while True:
        leftBump, rightBump = robot.getBumpers()
        if leftBump == rightBump == False:
            robot.moveForward()
        if leftBump == rightBump == True:
            robot.moveDistance(-0.05)    
            if robot.bumpedFrontRecently(3):
                robot.rotate(90)
            else:
                robot.rotate(-180)
              
        elif leftBump:
                robot.rotate(1)
        elif rightBump:
                robot.rotate(-1)

solve()