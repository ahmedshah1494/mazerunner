for i in range(0,3):
	moveDistanceSmart(4)
	time.sleep(3)
	img = capture()
	d = getDirectionFromImage(img)
	c = getCommandFromImage(img)
	t = getTagFromImage(img)
	if d == 'left':
		rotate(-90)
	else:
		rotate(90)
	print d
	print c
	print t

