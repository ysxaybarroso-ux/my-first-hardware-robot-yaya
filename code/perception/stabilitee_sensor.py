import board
import busio
import adafruit_bno055

i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_bno055.BNO055_I2C(i2c)

roll= None
pitch = None 

def lire_stabilitee():
    global roll , pitch
    while True:
        roll = sensor.euler[2]
        pitch = sensor.euler[1]