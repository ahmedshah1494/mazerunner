#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 27 May 2015

###########################################################################
# Copyright (c) 2015 iRobot Corporation
# http://www.irobot.com/
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#   Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
#   Neither the name of iRobot Corporation nor the names
#   of its contributors may be used to endorse or promote products
#   derived from this software without specific prior written
#   permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###########################################################################


from Tkinter import *
import tkMessageBox
import tkSimpleDialog
import time

import struct
import sys, glob # for listing serial ports

import math
import thread
import threading

try:
    import serial
except ImportError:
    #MHH:
    print('Import error', 'Please install pyserial.')
    raise

connection = None

TEXTWIDTH = 40 # window width, in characters
TEXTHEIGHT = 16 # window height, in lines

VELOCITYCHANGE = 200
ROTATIONCHANGE = 300

helpText = """\
Supported Keys:
P\tPassive
S\tSafe
F\tFull
C\tClean
D\tDock
R\tReset
Space\tBeep
Arrows\tMotion

If nothing happens after you connect, try pressing 'P' and then 'S' to get into safe mode.
"""

SENSORS = chr(142)  # + 1 byte
ACCUMULATED_DISTANCE = 0
DISTANCE_TRAVELED = 0

# the sensors
BUMPS_AND_WHEEL_DROPS = 7
WALL_IR_SENSOR = 8
CLIFF_LEFT = 9
CLIFF_FRONT_LEFT = 10
CLIFF_FRONT_RIGHT = 11
CLIFF_RIGHT = 12
VIRTUAL_WALL = 13
LSD_AND_OVERCURRENTS = 14
INFRARED_BYTE = 17
BUTTONS = 18
DISTANCE = 19
ANGLE = 20
CHARGING_STATE = 21
VOLTAGE = 22
CURRENT = 23
BATTERY_TEMP = 24
BATTERY_CHARGE = 25
BATTERY_CAPACITY = 26
WALL_SIGNAL = 27
CLIFF_LEFT_SIGNAL = 28
CLIFF_FRONT_LEFT_SIGNAL = 29
CLIFF_FRONT_RIGHT_SIGNAL = 30
CLIFF_RIGHT_SIGNAL = 31
CARGO_BAY_DIGITAL_INPUTS = 32
CARGO_BAY_ANALOG_SIGNAL = 33
CHARGING_SOURCES_AVAILABLE = 34
OI_MODE = 35
SONG_NUMBER = 36
SONG_PLAYING = 37
NUM_STREAM_PACKETS = 38
REQUESTED_VELOCITY = 39
REQUESTED_RADIUS = 40
REQUESTED_RIGHT_VELOCITY = 41
REQUESTED_LEFT_VELOCITY = 42
# others just for easy access to particular parts of the data
POSE = 100
LEFT_BUMP = 101
RIGHT_BUMP = 102
LEFT_WHEEL_DROP = 103
RIGHT_WHEEL_DROP = 104
CENTER_WHEEL_DROP = 105
LEFT_WHEEL_OVERCURRENT = 106
RIGHT_WHEEL_OVERCURRENT = 107
ADVANCE_BUTTON = 108
PLAY_BUTTON = 109

#                    0 1 2 3 4 5 6 7 8 9101112131415161718192021222324252627282930313233343536373839404142
SENSOR_DATA_WIDTH = [0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,2,2,1,2,2,2,2,2,2,2,1,2,1,1,1,1,1,2,2,2,2]


class iRobotInterface(Tk):
    # static variables for keyboard callback -- I know, this is icky
    callbackKeyUp = False
    callbackKeyDown = False
    callbackKeyLeft = False
    callbackKeyRight = False
    callbackKeyLastDriveCommand = ''

    def __init__(self):
        self.connect()
        if self.is_connected():
            self.setMode('P')
            self.setMode('F')


    # sendCommandASCII takes a string of whitespace-separated, ASCII-encoded base 10 values to send
    def sendCommandASCII(self, command):
        cmd = ""
        for v in command.split():
            cmd += chr(int(v))

        self.sendCommandRaw(cmd)

    # sendCommandRaw takes a string interpreted as a byte array
    def sendCommandRaw(self, command):
        global connection

        try:
            if connection is not None:
                connection.write(command)
            else:
                #MHH
                print "Not connected."
        except serial.SerialException:
            print "Lost connection"
            #MHH
            connection = None

        #print ' '.join([ str(ord(c)) for c in command ])
        #MHH
        #self.text.insert(END, ' '.join([ str(ord(c)) for c in command ]))
        #self.text.insert(END, '\n')
        #self.text.see(END)

    # getDecodedBytes returns a n-byte value decoded using a format string.
    # Whether it blocks is based on how the connection was set up.
    def getDecodedBytes(self, n, fmt):
        global connection

        try:
            return struct.unpack(fmt, connection.read(n))[0]
        except serial.SerialException:
            print "Lost connection"
            #MHH
            print 'Uh-oh-- Lost connection to the robot'
            connection = None
            return None
        except struct.error:
            print "Got unexpected data from serial port."
            return None

    # get8Unsigned returns an 8-bit unsigned value.
    def get8Unsigned(self):
        return getDecodedBytes(1, "B")

    # get8Signed returns an 8-bit signed value.
    def get8Signed(self):
        return getDecodedBytes(1, "b")

    # get16Unsigned returns a 16-bit unsigned value.
    def get16Unsigned(self):
        return getDecodedBytes(2, ">H")

    # get16Signed returns a 16-bit signed value.
    def get16Signed(self):
        return getDecodedBytes(2, ">h")


    # MHH
    def setMode(self, m):
            if m == 'P':   # Passive
                self.sendCommandASCII('128')
            elif m == 'S': # Safe
                self.sendCommandASCII('131')
                #print 'MHH-- Mode =', m
            elif m == 'F': # Full
                self.sendCommandASCII('132')
            elif m == 'C': # Clean
                self.sendCommandASCII('135')
            elif m == 'D': # Dock
                self.sendCommandASCII('143')
            elif m == 'SPACE': # Beep
                self.sendCommandASCII('140 3 1 64 16 141 3')
            elif m == 'R': # Reset
                self.sendCommandASCII('7')
            else:
                print repr(k), "not handled"

    #MHH
    def goForwardInTime(self, s, v = VELOCITYCHANGE):
        self.callbackKeyUp = True
        motionChange = True
        velocity = 0

        if v <= 0:
            print "You can only pass positive velocities for moving forward."
            motionChange = False
        elif v > 500:
            print "Maximum velocity is 500 mm/s. We set the velocity to the maximum."
            velocity = 500
        else:
            velocity = v

        if s <= 0:
            if s == 0:
               print "You cannot drive in no time!\nYou need to enter a positive time value."
            else:
               print "You cannot drive in time backward!\nYou need to enter a positive time value."

            motionChange = False


        if motionChange == True:
            rotation = 0

            #MHH
            self.callbackKeyUp = False

            # compute left and right wheel velocities
            vr = velocity + (rotation/2)
            vl = velocity - (rotation/2)

            # create drive command
            cmd = struct.pack(">Bhh", 145, vr, vl)
            if cmd != self.callbackKeyLastDriveCommand:
                self.sendCommandRaw(cmd)
                self.callbackKeyLastDriveCommand = cmd
                time.sleep(s)
                self.stopMoving()

    def goForward(self, d, v = VELOCITYCHANGE):
        velocity = 0
        motionChange = True

        if v <= 0:
            print "You can only pass positive velocities for moving forward."
            motionChange = False
        elif v > 500:
            print "Maximum velocity is 500 mm/s. We set the velocity to the maximum."
            velocity = 500
        else:
            velocity = v

        if motionChange:
            t = (d*100*10) / v
            self.goForwardInTime(t, v)

    def goForwardUntilBump(self, d, v = VELOCITYCHANGE):
        velocity = 0
        motionChange = True

        if v <= 0:
            print "You can only pass positive velocities for moving forward."
            motionChange = False
        elif v > 500:
            print "Maximum velocity is 500 mm/s. We set the velocity to the maximum."
            velocity = 500
        else:
            velocity = v

        if motionChange:
            t = (d*100*10) / v
            self.goFor(v)
            #print "going forward at " + str(v) + " for " + str(t)
            start_t = time.time()
            while True:
                cur_t = time.time()
                if (self.getBumpSensor() or cur_t - start_t >= t):
                    #print (cur_t - start_t)
                    break
                time.sleep(0.001)
            self.stopMoving()
            time_fraction = max(min((cur_t - start_t) / t, 1.0), 0.0)
            #print ("time fraction is" + str(time_fraction) + "\n")
            return time_fraction * d
        return 0

    #MHH: Be carefull, this will go forever if you do not stop it.
    def goFor(self, v = VELOCITYCHANGE):
        self.callbackKeyUp = True
        motionChange = True
        velocity = 0

        if v <= 0:
            print "You can only pass positive velocities for moving forward."
            motionChange = False
        elif v > 500:
            print "Maximum velocity is 500 mm/s. We set the velocity to the maximum."
            velocity = 500
        else:
            velocity = v


        if motionChange == True:
            rotation = 0

            self.callbackKeyUp = False

            # compute left and right wheel velocities
            vr = velocity + (rotation/2)
            vl = velocity - (rotation/2)

            # create drive command
            cmd = struct.pack(">Bhh", 145, vr, vl)
            if cmd != self.callbackKeyLastDriveCommand:
                self.sendCommandRaw(cmd)
                self.callbackKeyLastDriveCommand = cmd


    #MHH
    def stopMoving(self):
            # compute left and right wheel velocities
            vr = 0
            vl = 0

            # create drive command
            cmd = struct.pack(">Bhh", 145, vr, vl)
            if cmd != self.callbackKeyLastDriveCommand:
                self.sendCommandRaw(cmd)
                self.callbackKeyLastDriveCommand = cmd

    def goBackward(self, d, v = VELOCITYCHANGE):
        velocity = 0
        motionChange = True

        if v <= 0:
            print "You can only pass positive velocities for moving forward."
            motionChange = False
        elif v > 500:
            print "Maximum velocity is 500 mm/s. We set the velocity to the maximum."
            velocity = 500
        else:
            velocity = v

        if motionChange:
            t = (d*100*10) / v
            self.goBackwardInTime(t, v)
                
                
                
    #MHH
    def goBackwardInTime(self, s, v = VELOCITYCHANGE):
        self.callbackKeyDown = True
        motionChange = True
        velocity = 0

        if v <= 0:
            print "You can only pass positive velocities for moving backward."
            motionChange = False
        elif v > 500:
            print "Maximum velocity is 500 mm/s. We set the velocity to the maximum."
            velocity = -500
        else:
            velocity = -v


        if s <= 0:
            if s == 0:
               print "You cannot drive in no time!\nYou need to enter a positive time value."
            else:
               print "You cannot drive in time backward!\nYou need to enter a positive time value."

            motionChange = False


        if motionChange == True:
            rotation = 0

            self.callbackKeyDown = False

            # compute left and right wheel velocities
            vr = velocity + (rotation/2)
            vl = velocity - (rotation/2)

            # create drive command
            cmd = struct.pack(">Bhh", 145, vr, vl)
            if cmd != self.callbackKeyLastDriveCommand:
                self.sendCommandRaw(cmd)
                self.callbackKeyLastDriveCommand = cmd
                time.sleep(s)
                self.stopMoving()


    #MHH: Be carefull, this will go backward forever unless you stop it.
    def goBack(self, v = VELOCITYCHANGE):
        self.callbackKeyDown = True
        motionChange = True
        velocity = 0

        if v <= 0:
            print "You can only pass positive velocities for moving backward."
            motionChange = False
        elif v > 500:
            print "Maximum velocity is 500 mm/s. We set the velocity to the maximum."
            velocity = -500
        else:
            velocity = -v


        if motionChange == True:
            rotation = 0

            self.callbackKeyDown = False

            # compute left and right wheel velocities
            vr = velocity + (rotation/2)
            vl = velocity - (rotation/2)

            # create drive command
            cmd = struct.pack(">Bhh", 145, vr, vl)
            if cmd != self.callbackKeyLastDriveCommand:
                self.sendCommandRaw(cmd)
                self.callbackKeyLastDriveCommand = cmd

    #MHH
    def turnL(self, s, r = ROTATIONCHANGE):
        self.callbackKeyLeft = True
        motionChange = True

        if s <= 0:
            print "You can only rotate the iRobot in positive time; hence, enter a positive time value."
            motionChange = False

        if motionChange == True:
            velocity = 0
            rotation = r

            self.callbackKeyLeft = False

            # compute left and right wheel velocities
            vr = velocity + (rotation/2)
            vl = velocity - (rotation/2)

            # create drive command
            cmd = struct.pack(">Bhh", 145, vr, vl)
            if cmd != self.callbackKeyLastDriveCommand:
                self.sendCommandRaw(cmd)
                self.callbackKeyLastDriveCommand = cmd
                time.sleep(s)
                self.stopMoving()


    def turnLeft(self, deg, r = ROTATIONCHANGE):
        D = 255 # in mm
        arclen = 2 * math.pi * D
        arclen *= (deg / 360.0)
        t = arclen / (r)
        self.turnL(t, r)

    #MHH
    def turnR(self, s,radius, r = ROTATIONCHANGE):
        self.callbackKeyLeft = True
        motionChange = True

        if s <= 0:
            print "You can only rotate the iRobot in positive time; hence, enter a positive time value."
            motionChange = False

        if motionChange == True:
            velocity = 0
            rotation = -r

            self.callbackKeyLeft = False

            # compute left and right wheel velocities
            vr = velocity + (rotation/2)
            vl = velocity - (rotation/2)

            # create drive command
            cmd = struct.pack(">Bhh", 145, vr, vl)
            if cmd != self.callbackKeyLastDriveCommand:
                self.sendCommandRaw(cmd)
                self.callbackKeyLastDriveCommand = cmd
                time.sleep(s)
                self.stopMoving()
                

    def turnRight(self, deg, r = ROTATIONCHANGE):
        D = 255 # in mm
        arclen = 2 * math.pi * D
        arclen *= (deg / 360.0)
        t = arclen / (r)
        self.turnR(t, r)

    def read(self, bytes):
        global connection
        message = ""
        message = connection.read( bytes )
        #return str(message, encoding='Latin-1');
        return message;


    def getBumpSensor(self):
        '''Reads the value of the requested sensor from the robot and returns it.'''
        # Send the request for data to the Create:

        seq = [142, BUMPS_AND_WHEEL_DROPS]
        string = ""
        for s in seq:
            string += str(s) + " "
        self.sendCommandASCII(string)

        # Receive the reply:

        # MB: Added ability to retry in case a user is querying the sensors
        # while the robot is executing a wait command.
        msg = self.read(1)
        nRetries = 0
        while len(msg) < 1 and nRetries < 3:
            # Serial receive appears to block for 0.5 sec, so we don't
            # need to sleep
            msg = self.read(1)
            nRetries += 1

        #print nRetries, "retries needed"

        # Last resort: return None and force the user to deal with it,
        # rather than crashing.
        #if len(msg) < 2:
        #    raise CommunicationError("Improper sensor query response length: ")
            #self.close()
        #    return None
        msg_len = len(msg)
        if msg_len == 0:
            return False
        sensor_bytes = [ord(b) for b in msg[0:msg_len]]
        bRightBumper = sensor_bytes[0] & 0x1
        bLeftBumper = sensor_bytes[0] & 0x2
        return True if bRightBumper or bLeftBumper else False

    def _interpretSensor(self, sensorToRead, raw_data):
        '''interprets the raw binary data form a sensor into its appropriate form for use.  This function is for internal use - DO NOT CALL'''
        data = None
        #interpret = SENSORS[sensorToRead].interpret

        #if len(raw_data) < SENSORS[sensorToRead].size:
        #        return None

        #if interpret == "ONE_BYTE_SIGNED":
        #    data = self._getOneByteSigned(raw_data[0])
        #elif interpret == "ONE_BYTE_UNSIGNED":
        #    data = self._getOneByteUnsigned(raw_data[0])
        #elif interpret == "TWO_BYTE_SIGNED":
        data = self._getTwoBytesSigned(raw_data[0],raw_data[1])
        #elif interpret == "TWO_BYTE_UNSIGNED":
        #    data = self._getTwoBytesUnsigned(raw_data[0],raw_data[1])
        #elif interpret == "ONE_BYTE_UNPACK":
        #    if sensorToRead == "BUMPS_AND_WHEEL_DROPS":
        #        data = self._getLower5Bits(raw_data[0])
        #    elif sensorToRead == "BUTTONS":
        #        data = self._getButtonBits(raw_data[0])
        #    elif sensorToRead == "USER_DIGITAL_INPUTS":
        #        data = self._getLower5Bits(raw_data[0])
        #    if sensorToRead == "OVERCURRENTS":
        #        data = self._getLower5Bits(raw_data[0])
        #elif interpret == "NO_HANDLING":
        #    data = raw_data

        return data



    def _getTwoBytesSigned( self, r1, r2 ):
        """ r1, r2 are two bytes as a signed integer """
        return self.twosComplementInt2bytes( r1, r2 )


    def twosComplementInt2bytes( self, highByte, lowByte ):
        """ returns an int which has the same value
        as the twosComplement value stored in
        the two bytes passed in

        the output range should be -32768 to 32767

        chars or ints can be input, both will be
        truncated to 8 bits
        """
        # take everything except the top bit
        topbit = self.bitOfByte( 7, highByte )
        lowerbits = highByte & 127
        unsignedInt = lowerbits << 8 | (lowByte & 0xFF)
        if topbit == 1:
            # with sufficient thought, I've convinced
            # myself of this... we'll see, I suppose.
            return unsignedInt - (1 << 15)
        else:
            return unsignedInt

    def twosComplementInt2bytesV2( self, highByte, lowByte ):
        """ returns an int which has the same value
        as the twosComplement value stored in
        the two bytes passed in

        the output range should be -32768 to 32767

        chars or ints can be input, both will be
        truncated to 8 bits
        """
        # take everything except the top bit
        topbit = self.bitOfByte( 7, highByte )
        print 'Top Bit', topbit
        lowerbits = highByte & 127
        unsignedInt = lowerbits << 8 | (lowByte & 0xFF)
        if topbit == 1:
            # with sufficient thought, I've convinced
            # myself of this... we'll see, I suppose.
            return unsignedInt - (1 << 15)
        else:
            return unsignedInt

    def bitOfByte( self, bit, byte ):
        """ returns a 0 or 1: the value of the 'bit' of 'byte' """
        if bit < 0 or bit > 7:
           print 'Your bit of', bit, 'is out of range (0-7)'
           print 'returning 0'
           return 0
        return ((byte >> bit) & 0x01)


    # A handler for keyboard events. Feel free to add more!
    def callbackKey(self, event):
        k = event.keysym.upper()
        motionChange = False

        if event.type == '2': # KeyPress; need to figure out how to get constant
            if k == 'P':   # Passive
                self.sendCommandASCII('128')
            elif k == 'S': # Safe
                self.sendCommandASCII('131')
            elif k == 'F': # Full
                self.sendCommandASCII('132')
            elif k == 'C': # Clean
                self.sendCommandASCII('135')
            elif k == 'D': # Dock
                self.sendCommandASCII('143')
            elif k == 'SPACE': # Beep
                self.sendCommandASCII('140 3 1 64 16 141 3')
            elif k == 'R': # Reset
                self.sendCommandASCII('7')
            elif k == 'UP':
                self.callbackKeyUp = True
                motionChange = True
            elif k == 'DOWN':
                self.callbackKeyDown = True
                motionChange = True
            elif k == 'LEFT':
                self.callbackKeyLeft = True
                motionChange = True
            elif k == 'RIGHT':
                self.callbackKeyRight = True
                motionChange = True
            else:
                print repr(k), "not handled"
        elif event.type == '3': # KeyRelease; need to figure out how to get constant
            if k == 'UP':
                self.callbackKeyUp = False
                motionChange = True
            elif k == 'DOWN':
                self.callbackKeyDown = False
                motionChange = True
            elif k == 'LEFT':
                self.callbackKeyLeft = False
                motionChange = True
            elif k == 'RIGHT':
                self.callbackKeyRight = False
                motionChange = True

        if motionChange == True:
            velocity = 0
            velocity += VELOCITYCHANGE if self.callbackKeyUp is True else 0
            velocity -= VELOCITYCHANGE if self.callbackKeyDown is True else 0
            rotation = 0
            rotation += ROTATIONCHANGE if self.callbackKeyLeft is True else 0
            rotation -= ROTATIONCHANGE if self.callbackKeyRight is True else 0

            # compute left and right wheel velocities
            vr = velocity + (rotation/2)
            vl = velocity - (rotation/2)

            # create drive command
            cmd = struct.pack(">Bhh", 145, vr, vl)
            if cmd != self.callbackKeyLastDriveCommand:
                self.sendCommandRaw(cmd)
                self.callbackKeyLastDriveCommand = cmd

    #MHH
    def connect(self):
        global connection

        if connection is not None:
            print 'Oops', "You're already connected!"
            return

        try:
            #raise
            #ports = self.getSerialPorts()
            #MHH
            #port = tkSimpleDialog.askstring('Port?', 'Enter COM port to open.\nAvailable options:\n' + '\n'.join(ports))
            #print 'Available Options:\n' + '\n'.join(ports)
            #port = raw_input('Enter COM port to open.\n')
            port = "/dev/ttyUSB0"
        except EnvironmentError:
            port = "/dev/ttyUSB0"#raw_input('Enter COM port:\n')

        if port is not None:
            #print "Trying " + str(port) + "... "
            try:
                connection = serial.Serial(port, baudrate=115200, timeout=1)
                print "Connection Succeeded!"
            except:
                connection =  None
                #tkMessageBox.showinfo('Failed', "Sorry, couldn't connect to " + str(port))
    
    def is_connected(self):
        global connection
        return connection != None

    def onConnect(self):
        global connection

        if connection is not None:
            tkMessageBox.showinfo('Oops', "You're already connected!")
            return

        try:
            ports = self.getSerialPorts()
            port = tkSimpleDialog.askstring('Port?', 'Enter COM port to open.\nAvailable options:\n' + '\n'.join(ports))
            #port = raw_input('Port?', 'Enter COM port to open.\nAvailable options:\n' + '\n'.join(ports))
        except EnvironmentError:
            port = tkSimpleDialog.askstring('Port?', 'Enter COM port to open.')

        if port is not None:
            print "Trying " + str(port) + "... "
            try:
                connection = serial.Serial(port, baudrate=115200, timeout=1)
                print "Connected!"
                tkMessageBox.showinfo('Connected', "Connection succeeded!")
            except:
                print "Failed."
                tkMessageBox.showinfo('Failed', "Sorry, couldn't connect to " + str(port))


    def onHelp(self):
        tkMessageBox.showinfo('Help', helpText)

    def onQuit(self):
        if tkMessageBox.askyesno('Really?', 'Are you sure you want to quit?'):
            self.destroy()

    def stop(self):
         self.sendCommandASCII('173')


    def getSerialPorts(self):
        """Lists serial ports
        From http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of available serial ports
        """
        if sys.platform.startswith('win'):
            ports = ['COM' + str(i + 1) for i in range(256)]

        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this is to exclude your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')

        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')

        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def getDistanceSensor(self):
        global connection
        self.sendCommandASCII('19')
        r = connection.read(size=1)
        return r

    #MHH
    def getDistanceTraveled(self):
        global connection

        connection.write( SENSORS )
        connection.write( chr(2) )

        r = connection.read(size=6)

        r = [ ord(c) for c in r ]   # convert to ints

        print 'R = ', r

        distance = 0
        interpretedData = 0
        startofdata = 2
        interpretedData = self.twosComplementInt2bytesV2(r[startofdata], r[startofdata+1] )
        #print 'Distance = ', interpretedData

        if(interpretedData <= 0):
           interpretedData = interpretedData * -1

        return interpretedData

    #MHH
    def getAccumulatedDistance(self):
        global ACCUMULATED_DISTANCE
        ACCUMULATED_DISTANCE = self.getDistanceTraveled() + ACCUMULATED_DISTANCE
        return ACCUMULATED_DISTANCE

    #MHH
    def resetAccumulatedDistance(self):
        global ACCUMULATED_DISTANCE
        self.getDistanceTraveled()
        ACCUMULATED_DISTANCE = 0


    #MHH
    def getAngleRotated(self):
        global connection

        connection.write( SENSORS )
        connection.write( chr(2) )

        r = connection.read(size=6)

        r = [ ord(c) for c in r ]   # convert to ints

        print 'R = ', r

        angle = 0
        interpretedData = 0
        startofdata = 4
        interpretedData = self.twosComplementInt2bytesV2(r[startofdata], r[startofdata+1] )
        print 'Angle = ', interpretedData

        return interpretedData



