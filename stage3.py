from breezycreate2 import Robot

import time

robot = Robot()
robot.playNote('A1', 100)

# while rain and car is on...


def solve():
    while True:
        robot.moveForward()
        leftBump, rightBump = robot.getBumpers()
        if leftBump and rightBump:
            robot.moveDistance(-0.05)    
            if robot.bumpedFrontRecently(3):
                robot.rotate(180)
            else:
                robot.rotate(-90)
              
        elif leftBump:
                robot.rotate(1)
        elif rightBump:
                robot.rotate(-1)

def solve2():
    while True:
        robot.moveForward()
        robot.updateBumpers()
        if robot.leftBump and robot.rightBump:
            robot.moveDistance(-0.05)    
            if robot.bumpedFrontRecently(3):
                robot.rotate(180)
            else:
                robot.rotate(-90)
              
        elif robot.leftBump:
                robot.rotate(10)
        elif robot.rightBump:
                robot.rotate(-10)

solve2()