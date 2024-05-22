# physics toy
import time

from adafruit_display_shapes.rect import Rect

from thunder.mpu6050 import Mpu
from thunder.display import Display

display = Display()

x = 240/2-5
y = 240/2-5
mpu = Mpu()
r = Rect(int(x), int(y), 10, 10, fill=0xFFAAFF)
display.screen.append(r)

while True:
	val = mpu.get_values()
	if abs(val["accel_x"]*10) >= 1:
		x += val["accel_x"]*10
	if abs(val["accel_y"]*10) >= 1:
		y += val["accel_y"]*10
	if x<0:
		x = 0
	if x>230:
		x = 230
	if y<0:
		y = 0
	if y>230:
		y = 230
	r.x = int(x)
	r.y = int(y)
	time.sleep(1/30)