from pyfirmata import Arduino,util
# import tensorflow
import pandas
import time
import os




board = Arduino('/dev/cu.usbmodem21401')
it = util.Iterator(board)
it.start()
board.analog[0].enable_reporting()
# can be changed due to port.
# use ls /dev to found your arduino.
# 컴터에 따라 뱌꿔요.

print('connected to Arduino')

# Set up Steering pins

steering_speed_pin = board.get_pin('d:10:p')
steering_IN0= board.get_pin('d:9:o')
steering_IN1= board.get_pin('d:8:o')

steering_sig_pin = board.get_pin('a:0:i')

# Set up throttle pins

throttle_speed_pin = board.get_pin('d:11:p')
throttle_IN0 = board.get_pin('d:12:o')
throttle_IN1 = board.get_pin('d:13:o')

throttle_speed_pin1 = board.get_pin('d:6:p')
throttle_IN01 = board.get_pin('d:5:o')
throttle_IN11 = board.get_pin('d:4:o')


steering_speed_pin.write(1)
throttle_speed_pin.write(1)
throttle_speed_pin1.write(1)

class Car:
    def __init__(self):
        self.a = 1
        self.speed = 0
        self.status = "Cooling Down :D"
        
    def forward(self,speed):
        self.speed = speed
        print("creeping forward")
        self.status = "creeping forward"
        throttle_speed_pin.write(speed)
        throttle_speed_pin1.write(speed)
        throttle_IN0.write(1)
        throttle_IN1.write(0)
        throttle_IN01.write(1)
        throttle_IN11.write(0)

    def backward(self,speed):
        self.speed = -speed
        print("backing up")
        throttle_speed_pin.write(speed)
        throttle_speed_pin1.write(speed)
        throttle_IN0.write(0)
        throttle_IN1.write(1)
        throttle_IN01.write(0)
        throttle_IN11.write(1)
        
    def stop(self):
        print("Dispowering motor")
        throttle_speed_pin.write(0)
        throttle_speed_pin1.write(0)
        print("Motor dispowered")
        print("Stopping motor")
        throttle_IN0.write(0)
        throttle_IN1.write(0)
        throttle_IN01.write(0)
        throttle_IN11.write(0)
        print("Motor stoped")

    def left(self):
        ctd = steering_sig_pin.read()
        while(ctd - 0.025 < steering_sig_pin.read()):
            steering_IN0.write(1)
            steering_IN1.write(0)
        steering_IN0.write(0)
        steering_IN1.write(0)

    def right(self):
        ctd = steering_sig_pin.read()
        while(ctd + 0.025 > steering_sig_pin.read()):
            steering_IN0.write(0)
            steering_IN1.write(1)
        steering_IN0.write(0)
        steering_IN1.write(0)
        
    def getInfo(self):
        
        # sendInfo
        info = {
                'steeringAngleRaw':steering_sig_pin.read(),
                'steeringAngleDeg':360 * (steering_sig_pin.read()-0.5),
                'motorSpeed':self.speed,
                'batteryStatus': 0.82, #hardcoded data.
                'generalStatus': self.status
                }
        return info
    
    