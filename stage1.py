from breezycreate2 import Robot

robot = Robot()
robot.rotate(360)



def solve1():
	robot.moveDistanceSmart(0.175 + 0.125)
	robot.rotate(90)
	robot.moveDistanceSmart(1.2)
	robot.rotate(-90)
	robot.moveDistanceSmart(3.6 - 2*(0.27 + 0.075))
	robot.rotate(90)
	robot.moveDistanceSmart(3 - 2*(0.27 + 0.075))
	robot.rotate(-90)
	robot.moveDistanceSmart(1.2 + 0.27)
	robot.rotate(90)
	robot.moveDistanceSmart(0.45)

def solve2():
	robot.moveDistanceSmart(0.175 + 0.125)
	robot.rotate(-90)
	robot.moveDistanceSmart(1.2)
	robot.rotate(90)
	robot.moveDistanceSmart(1.2 - 2*(0.175 + 0.125))
	robot.rotate(-90)
	robot.moveDistanceSmart(1.2)
	robot.rotate(-90)
	robot.moveDistanceSmart(1.2 - 2*(0.175 + 0.125))
	robot.rotate(-90)
	robot.moveDistanceSmart(1.2)	
	robot.rotate(90)
	robot.moveDistanceSmart(0.6 + 0.27)
