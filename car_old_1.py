from pyfirmata import Arduino,util

board = Arduino('/dev/cu.usbmodem1201')

analogreading = util.Iterator(board)
analogreading.start()

board.analog[0].enable_reporting()
board.analog[1].enable_reporting()
board.analog[2].enable_reporting()
board.analog[3].enable_reporting()



steering_speed_pin = board.get_pin('d:10:p')
steering_IN0= board.get_pin('d:9:o')
steering_IN1= board.get_pin('d:8:o')

steering_sig_pin = board.get_pin('a:0:i')
batteryVoltagePin = board.get_pin('a:1:i')

steering_input = board.get_pin('a:2:i')
throttle_input = board.get_pin('a:3:i')
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

print('connected to Arduino')



class Car:
    def __init__(self):
        self.speed = 0
        self.steeringAngleRaw = 0
        self.status = "Cooling Down :D"
        self.batteryVoltage = 12.0
        

    def forward(self,speed):
        self.speed = speed
        self.status = "forwarding"
        throttle_speed_pin.write(speed)
        throttle_speed_pin1.write(speed)
        throttle_IN0.write(1)
        throttle_IN1.write(0)
        throttle_IN01.write(1)
        throttle_IN11.write(0)

    def backward(self,speed):
        self.speed = -speed
        self.status = "backwarding"
        throttle_speed_pin.write(speed)
        throttle_speed_pin1.write(speed)
        throttle_IN0.write(0)
        throttle_IN1.write(1)
        throttle_IN01.write(0)
        throttle_IN11.write(1)

    def left(self):
        steering_IN0.write(1)
        steering_IN1.write(0)

    def right(self):
        steering_IN0.write(0)
        steering_IN1.write(1)
        
        
    def steer(self,rawAngle):
        ctr = steering_sig_pin.read()
        
    def throttle(self,rawThrottle): 
        return 0
        
    def move(self,x,y):
        print(x,y)
        
    def getInfo(self):
        infoJson = {
                "steeringAngleRaw":steering_sig_pin.read(),
                "steeringAngleDeg":360 * (steering_sig_pin.read()-0.5),
                "motorSpeed":self.speed,
                "generalStatus": self.status
                }
        return infoJson
    
car = Car()
import time

time.sleep(1)

# print(car.getInfo())

while 1:
    car.move(steering_input.read(),throttle_input.read())