from pyfirmata import Arduino,util
# import tensorflow
# import pandas
import os

board = Arduino('/dev/cu.usbmodem1201')


analogreading = util.Iterator(board)
analogreading.start()

board.analog[0].enable_reporting()
board.analog[1].enable_reporting()

steering_speed_pin = board.get_pin('d:10:p')
steering_IN0= board.get_pin('d:9:o')
steering_IN1= board.get_pin('d:8:o')

steering_sig_pin = board.get_pin('a:0:i')
batteryVoltagePin = board.get_pin('a:1:i')

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
        
    def move_y(self,speed):
        # 양수가 들어오면 전진, 음수가 들어오면 후진. 범위는 -512 ~ 512
        # 로직:
        
        # 0. __safety__ 512 ~ -512 범위 안인지 검사
        if speed >= 512 or speed <= -512:
            return 0
        
        # 1. 방향 정하기 (앞,뒤)
        direction = -1 if speed < 0 else 0 if speed == 0 else 1
        
        # 2. 속도 절댓값으로 던지기
        speed = abs(speed)
        
        # 2. 속도 0~1사이로 변환하기
        realSpeedForActuactor = speed/512.0
        
        # 3. GOGOGO
        
        

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
        infoJson = {
                "steeringAngleRaw":steering_sig_pin.read(),
                "steeringAngleDeg":360 * (steering_sig_pin.read()-0.5),
                "motorSpeed":self.speed,
                "batteryStatus": (batteryVoltagePin.read() * 5.0) / 1024.0 / ( 7500.0 / ( 30000.0 + 7500.0)),
                "generalStatus": self.status
                }
        return infoJson

if __name__ == "__main__":
    from time import sleep as delay
    import csv
    import cv2

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
        
        with open('./camdata/dt.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(carInfo)
           
        filename = f"./camdata/{n}_.jpg"
        delay(0.1)
        cv2.imwrite(filename, frame)
        
        n = n + 1