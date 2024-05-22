# Advanced physics toy
import time

from adafruit_display_shapes.circle import Circle

from thunder.mpu6050 import Mpu
from thunder.display import Display

display = Display()

w = 20
h = w
x = 240/2-(w/2)
y = 240/2-(h/2)
velox = 0
veloy = 0
resistance = 0.7
friction = 0.8
conservation = 0.64
mpu = Mpu()
r = Circle(int(x), int(y), int(w/2), fill=0xFFAAFF)
display.screen.append(r)

while True:
	val = mpu.get_values()
	if abs(val["accel_x"]) >= 0.5:
		velox += val["accel_x"]
	if abs(val["accel_y"]) >= 0.5:
		veloy += val["accel_y"]
	x+=velox * resistance
	y+=veloy * resistance
	
	if x<=0:
		x = 0
		velox = -velox*conservation
		veloy *= friction
	if x>=240-w:
		x = 240-w
		velox = -velox*conservation
		veloy *= friction
	if y<=0:
		y = 0
		veloy = -veloy*conservation
		velox *= friction
	if y>=240-h:
		y = 240-h
		veloy = -veloy*conservation
		velox *= friction
	r.x = int(x)
	r.y = int(y)