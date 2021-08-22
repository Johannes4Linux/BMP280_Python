# bmp280.py
# Simple python script to read out the temperature of the
# BMP280 temperature and pressure sensor

import smbus
from time import sleep

# BMP280 I2C address
bmp_addr = 0x76

# Get access to the i2c bus
i2c = smbus.SMBus(1)

# Setup the config register

i2c.write_byte_data(bmp_addr, 0xf5, (5<<5))
i2c.write_byte_data(bmp_addr, 0xf4, ((5<<5) | (3<<0)))

# Sensor is set up and will do a measurement every 1s

dig_T1 = i2c.read_word_data(bmp_addr, 0x88)
dig_T2 = i2c.read_word_data(bmp_addr, 0x8A)
dig_T3 = i2c.read_word_data(bmp_addr, 0x8C)

if(dig_T2 > 32767):
    dig_T2 -= 65536
if(dig_T3 > 32767):
    dig_T3 -= 65536

while True:
# Read the raw temperature
    d1 = i2c.read_byte_data(bmp_addr, 0xfa)
    d2 = i2c.read_byte_data(bmp_addr, 0xfb)
    d3 = i2c.read_byte_data(bmp_addr, 0xfc)

    adc_T = ((d1 << 16) | (d2 << 8) | d3) >> 4

# Calculate temperature
    var1 = ((((adc_T>>3) - (dig_T1<<1))) * (dig_T2)) >> 11;
    var2 = (((((adc_T>>4) - (dig_T1)) * ((adc_T>>4) - (dig_T1))) >> 12) * (dig_T3)) >> 14;
    t_fine = var1 + var2;
    T = (t_fine * 5 + 128) >> 8;
    T = T / 100

    print("Temperature: " +str(T))
    sleep(1)



