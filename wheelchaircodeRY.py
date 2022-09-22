import smbus
import math
import RPi.GPIO as GPIO
from time import sleep



GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
Motor1 = {'EN': 25, 'input1': 24, 'input2': 23}
Motor2 = {'EN': 17, 'input1': 27, 'input2': 22}
for x in Motor1:
    GPIO.setup(Motor1[x], GPIO.OUT)
    GPIO.setup(Motor2[x], GPIO.OUT)
EN1 = GPIO.PWM(Motor1['EN'], 100)
EN2 = GPIO.PWM(Motor2['EN'], 100)
EN1.start(0)
EN2.start(0)
while True:

    power_mgmt_1 = 0x6b
    power_mgmt_2 = 0x6c
     
    def read_byte(reg1):
        return bus.read_byte_data(address1, reg1)
     
    def read_word(reg1):
        h1 = bus1.read_byte_data(address1, reg1)
        l1 = bus1.read_byte_data(address1, reg1+1)
        value1 = (h1 << 8) + l1
        return value1
     
    def read_word_2c(reg1):
        val1 = read_word(reg1)
        if (val1 >= 0x8000):
            return -((65535 - val1) + 1)
        else:
            return val1
     
    def dist(a1,b1):
        return math.sqrt((a1*a1)+(b1*b1))
     
    def get_y_rotation(x1,y1,z1):
        radians1 = math.atan2(x1, dist(y1,z1))
        return -math.degrees(radians1)
     
    def get_x_rotation(x1,y1,z1):
        radians1 = math.atan2(y1, dist(x1,z1))
        return math.degrees(radians1)
     
    bus1 = smbus.SMBus(1) # bus = smbus.SMBus(0) Revision 1
    address1 = 0x69       # via i2cdetect
     
    bus1.write_byte_data(address1, power_mgmt_1, 0)

    ac_xout1 = read_word_2c(0x3b)
    ac_yout1 = read_word_2c(0x3d)
    ac_zout1 = read_word_2c(0x3f)
     
    ac_xout_scaled1 = ac_xout1 / 16384.0
    ac_yout_scaled1 = ac_yout1 / 16384.0
    ac_zout_scaled1 = ac_zout1 / 16384.0

    xrot1 = get_x_rotation(ac_xout_scaled1, ac_yout_scaled1, ac_zout_scaled1) #foward compared to xrot1
    yrot1 = get_y_rotation(ac_xout_scaled1, ac_yout_scaled1, ac_zout_scaled1) #side to side compared to yrot1

    print ("X Rotation1: " , xrot1)
    print ("Y Rotation1: " , yrot1)

    def read_byte(reg):
        return bus.read_byte_data(address, reg)
     
    def read_word(reg):
        h = bus.read_byte_data(address, reg)
        l = bus.read_byte_data(address, reg+1)
        value = (h << 8) + l
        return value
     
    def read_word_2c(reg):
        val = read_word(reg)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val
     
    def dist(a,b):
        return math.sqrt((a*a)+(b*b))
     
    def get_y_rotation(x,y,z):
        radians = math.atan2(x, dist(y,z))
        return -math.degrees(radians)
     
    def get_x_rotation(x,y,z):
        radians = math.atan2(y, dist(x,z))
        return math.degrees(radians)
     
    bus = smbus.SMBus(1) # bus = smbus.SMBus(0)
    address = 0x68       # via i2cdetect
     
    bus.write_byte_data(address, power_mgmt_1, 0)

    ac_xout = read_word_2c(0x3b)
    ac_yout = read_word_2c(0x3d)
    ac_zout = read_word_2c(0x3f)
     
    ac_xout_scaled = ac_xout / 16384.0
    ac_yout_scaled = ac_yout / 16384.0
    ac_zout_scaled = ac_zout / 16384.0

    xrot = get_x_rotation(ac_xout_scaled, ac_yout_scaled, ac_zout_scaled) #foward compared to xrot1
    yrot = get_y_rotation(ac_xout_scaled, ac_yout_scaled, ac_zout_scaled) #side to side compared to yrot1

    print ("X Rotation: " , xrot)
    print ("Y Rotation: " , yrot)
    print (" ")

    if math.isclose(xrot1, xrot, rel_tol = 2) == True and xrot1 > 40 and xrot1 < 260:
        EN1.ChangeDutyCycle(30)
        EN2.ChangeDutyCycle(30)
        GPIO.output(Motor1['input1'], GPIO.HIGH)
        GPIO.output(Motor1['input2'], GPIO.LOW)

        GPIO.output(Motor2['input1'], GPIO.HIGH)
        GPIO.output(Motor2['input2'], GPIO.LOW)
        sleep(0.1)
        print('BOTH TYRES')
    elif xrot1 < 40 and xrot1 > 0 and xrot < -15 and xrot > -35: #xrot is tan plate xrot1 is brown plate
        EN1.ChangeDutyCycle(30)
        EN2.ChangeDutyCycle(30)
        GPIO.output(Motor1['input1'], GPIO.HIGH)
        GPIO.output(Motor1['input2'], GPIO.LOW)

        GPIO.output(Motor2['input1'], GPIO.HIGH)
        GPIO.output(Motor2['input2'], GPIO.LOW)
        sleep(0.1)
        print('BOTH TYRES!')
           
    elif xrot1 > 40 and xrot1 < 260 and yrot1 < -40 and yrot1 > 200: #right
        EN1.ChangeDutyCycle(0)
        EN2.ChangeDutyCycle(0)
    elif xrot1 > 40 and xrot1 < 260 and yrot1 > 40 and yrot1 < 200: #left
        EN1.ChangeDutyCycle(0)
        EN2.ChangeDutyCycle(0)
    elif yrot1 < -40 and yrot1 > -200 :
        EN1.ChangeDutyCycle(30)
        GPIO.output(Motor1['input1'], GPIO.HIGH)
        GPIO.output(Motor1['input2'], GPIO.LOW)
        sleep(0.1)
        print('LEFT TYRE')
    elif yrot1 > 40 and yrot1 < 200:
        EN2.ChangeDutyCycle(30)
        GPIO.output(Motor2['input1'], GPIO.HIGH)
        GPIO.output(Motor2['input2'], GPIO.LOW)
        sleep(0.1)
        print('RIGHT TYRE')

    else:
        EN1.ChangeDutyCycle(0)
        EN2.ChangeDutyCycle(0)





