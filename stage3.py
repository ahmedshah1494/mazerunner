from breezycreate2 import Robot

import time


robot = Robot()

def solve():
    while True:
        leftBump, rightBump = robot.getBumpers()
        if leftBump == rightBump == False:
            robot.moveForward()
        if leftBump and rightBump:
            robot.moveDistance(-0.05)    
            if robot.bumpedFrontRecently(3):
                robot.rotate(180)
            else:
                robot.rotate(-90)
              
        elif leftBump:
                robot.rotate(2)
        elif rightBump:
                robot.rotate(-2)



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
                robot.rotate(2)
        elif robot.rightBump:
                robot.rotate(-2)

solve()