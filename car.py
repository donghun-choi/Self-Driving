from pyfirmata import Arduino,util
import time
print("welcome!")

board = Arduino('/dev/cu.usbmodem1301')
print('connected')

analogreading = util.Iterator(board)
analogreading.start()

for i in range(6):
    board.analog[i].enable_reporting()


MOTOR_0 = board.get_pin('d:3:o')
MOTOR_1 = board.get_pin('d:4:o')
MOTOR_2 = board.get_pin('d:5:o')
MOTOR_3 = board.get_pin('d:6:o')

THROTTLE_PIN_0 = board.get_pin('d:9:p')
THROTTLE_PIN_1 = board.get_pin('d:10:p')



class Car:
    def __init__(self):
        self.speed = 0
        self.statusMessage = "Ready To Go"
        self.batteryVoltage = None
        self.rpm = 0
        self.steering_angle = 0
        # cammalCase : experimental features
        # snake_case : features usable
        
    def move_y(self,speed):
        self.speed = speed
        THROTTLE_PIN_0.write(abs(self.speed))
        THROTTLE_PIN_1.write(abs(self.speed))
        if self.speed ==0:
            pass
        
        elif self.speed > 0:
            MOTOR_0.write(1)
            MOTOR_1.write(0)
            MOTOR_2.write(1)
            MOTOR_3.write(0)
            
            
        elif self.speed < 0:
            MOTOR_0.write(0)
            MOTOR_1.write(1)
            MOTOR_2.write(0)
            MOTOR_3.write(1)
    def get_rpm(self):
        pass
    
    
    def em_stop(self):
        MOTOR_0.write(0)
        MOTOR_1.write(0)
        MOTOR_2.write(0)
        MOTOR_3.write(0)