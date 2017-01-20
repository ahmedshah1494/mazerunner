f = os.popen('ifconfig  wlan0 | grep "inet addr:"| grep -v "127.0.0.1" | cut -d: -f2 | awk \'{ print $1}\'')
myIP = f.read().strip()


robot.robot.full()
for i in range(20):

	ip = myIP
	for i in range(2):
		robot.robot.digit_led_ascii(str("Addr").zfill(4))
		time.sleep(0.5)
		robot.robot.digit_led_ascii(str("    ").zfill(4))
		time.sleep(0.5)
	
	while len(ip) >= 4:
		robot.robot.digit_led_ascii(str(ip[:4]).zfill(4))
		ip = ip[1:]
		time.sleep(0.4)
		
	time.sleep(1)

pi_name = os.environ['RESIN_DEVICE_NAME_AT_INIT']
robot.robot.digit_led_ascii(str(pi_name).zfill(4))
robot.robot.safe()
