 #!/usr/bin/python
import smbus
import math
import time
 
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
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
 
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect
 
bus.write_byte_data(address, power_mgmt_1, 0)

# Formula to convert g's into units
# 1 g = 9.80665 m/s^2 
highgyrox, highgyroy, highgyroz = 0


print (" ________ _____________________ _____________________ _____________________ _________________ _______________ _______________ _______________ ")
while True:
  gyrox = read_word_2c(0x43)/131
  gyroy = read_word_2c(0x45)/131
  gyroz = read_word_2c(0x47)/131
 
  accx = (read_word_2c(0x3b)/16384.0)*9.806664
  accy = (read_word_2c(0x3d)/16384.0)*9.806665
  accz = (read_word_2c(0x3f)/16384.0)*9.806665


  #TODO: not sure about scaling these, based on an example in german 
  #Inverted the accelerometer values for x and y to accurately show acceleration.
  print ("|  gyro  |  x: {0:5.1f}\u00b0  |  y: {1:5.1f}\u00b0  |  z: {2:5.1f}\u00b0  |  acc, in m/s^2  |  x: {3:5.1f}  |  y: {4:5.1f}  |  z: {5:5.1f}  |".format(gyrox, gyroy, gyroz, accx, accy, accz), end='\r')
  print("\n")
  if highgyrox < gyrox:
      highgyrox = gyrox
  if highgyroy < gyroy:
      highgyroy = gyroy
  if highgyroz < gyroz:
      highgyroz = gyroz
  print ("|  max gyro  |  x: {0:5.1f}\u00b0  |  y: {1:5.1f}\u00b0  |  z: {2:5.1f}\u00b0  |".format(highgyrox, highgyroy, highgyroz), end='\r')

  xskalier = accx / 16384.0
  yskalier = accy / 16384.0
  zskalier = accz / 16384.0 
  #print ("acc x:{0:3f} y:{1:3f} z:{2:3f}".format(accx/16384.0, accy/16384.0, accz/16384.0), end='\r')
 
  time.sleep(0.5)  

 
 
