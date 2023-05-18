from pyfirmata import Arduino,util
import tensorflow
import pandas
import time



board = Arduino('/dev/cu.usbmodem21301')
# can be changed due to port.
# use ls /dev to found your arduino.
# 컴터에 따라 뱌꿔요.

print('connected to Arduino')

# Set up Steering pins

steering_speed_pin = board.get_pin('d:10:p')
steering_IN0= board.get_pin('d:9:o')
steering_IN1= board.get_pin('d:8:o')

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

throttle_IN0.write(0)
throttle_IN1.write(1)

time.sleep(4)
throttle_IN0.write(1)
throttle_IN1.write(1)
# 이게 포워드


class Car:
    def __init__(self, speed):
        self.speed = speed
        self.position = 0

    def forward(self):
        throttle_IN0.write(0)
        throttle_IN1.write(1)
        
    def backward(self):
        throttle_IN0.write(1)
        throttle_IN1.write(0)
        
    def left(self):
        return 0
    def right(self):
        return 0