from pyfirmata import Arduino,util
# import tensorflow
# import pandas
import os




# board = Arduino('/dev/cu.usbmodem1201')
# board = Arduino('/dev/cu.usbmodem21201')
# board = Arduino('/dev/cu.usbmodem21401')
board = Arduino('/dev/cu.usbmodem1401')


it = util.Iterator(board)
it.start()
board.analog[0].enable_reporting()
# can be changed due to port.
# use ls /dev to found your arduino.
# 컴터에 따라 뱌꿔요.


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

print('connected to Arduino')
class Car:
    def __init__(self):
        self.a = 1
        self.speed = 0
        self.steeringAngleRaw = 0
        self.status = "Cooling Down :D"
        self.batteryVoltage = 13.0
        
    def forward(self,speed):
        self.speed = speed
        self.status = "creeping forward"
        throttle_speed_pin.write(speed)
        throttle_speed_pin1.write(speed)
        throttle_IN0.write(1)
        throttle_IN1.write(0)
        throttle_IN01.write(1)
        throttle_IN11.write(0)

    def backward(self,speed):
        self.speed = -speed
        self.status = "backing up"
        throttle_speed_pin.write(speed)
        throttle_speed_pin1.write(speed)
        throttle_IN0.write(0)
        throttle_IN1.write(1)
        throttle_IN01.write(0)
        throttle_IN11.write(1)
        
    def stop(self):
        self.status = "Dispowering rear motors"
        throttle_speed_pin.write(0)
        throttle_speed_pin1.write(0)
        throttle_IN0.write(0)
        throttle_IN1.write(0)
        throttle_IN01.write(0)
        throttle_IN11.write(0)
        self.status = "Motor stoped"

    def left(self):
        ctd = steering_sig_pin.read()
        while(ctd - 0.025 < steering_sig_pin.read()):
            steering_IN0.write(1)
            steering_IN1.write(0)
        steering_IN0.write(0)
        steering_IN1.write(0)
        self.steeringAngleRaw = steering_sig_pin.read()

    def right(self):
        ctd = steering_sig_pin.read()
        while(ctd + 0.025 > steering_sig_pin.read()):
            steering_IN0.write(0)
            steering_IN1.write(1)
        steering_IN0.write(0)
        steering_IN1.write(0)
        self.steeringAngleRaw = steering_sig_pin.read()
        
    def getInfo(self):
        
        # sendInfo
        info = {
                "steeringAngleRaw":steering_sig_pin.read(),
                "steeringAngleDeg":360 * (steering_sig_pin.read()-0.5),
                "motorSpeed":self.speed,
                "batteryStatus": 0.82, #hardcoded data.
                "generalStatus": self.status
                }
        # print(info)
        return info
    def getFakeInfo(self):
        
        # sendInfo
        info = {
                "steeringAngleRaw":0.5,
                "steeringAngleDeg":0,
                "motorSpeed":0.42,
                "batteryStatus": 0.82,
                "generalStatus": "creeping forward"
                }
        return info

if __name__ == "__main__":
    from time import sleep as delay
    import csv
    import cv2
    import math

    cap = cv2.VideoCapture(0)
    car = Car()
    n = 0
    df = []
    while 1:
        where = input("press wasd:")
        if where =='w':
            car.forward(1)
            delay(0.5)
            car.stop()
        if where =='a':
            car.left()
        if where =='s':
            car.backward(1)
            delay(0.5)
            car.stop()
        if where =='d':
            car.right()
        
        ret, frame = cap.read()
        
        carInfo = car.getInfo()
        carInfo = [carInfo['steeringAngleRaw'],carInfo['motorSpeed']]
        print(carInfo)
        
        with open('dt.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(carInfo)
           
        filename = f"{n}_.jpg"
        delay(0.1)
        cv2.imwrite(filename, frame)
        
        n = n + 1
        