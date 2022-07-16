import time
import board
import adafruit_bh1750

i2c = board.I2C()
sensor_in = adafruit_bh1750.BH1750(i2c, address=0x23)
sensor_out = adafruit_bh1750.BH1750(i2c, address=0x5C)

while True:
    # print("%.2f Lux"%sensor.lux)
    print(f'{sensor_in.lux=}; {sensor_out.lux=}')
    time.sleep(1)