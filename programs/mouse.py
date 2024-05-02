# A virtual mouse
# a:left click b:right click select:middle mouse start+joystick:scroll joystick:mouse movement
import board, time
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.mouse import Mouse

mouse = Mouse(usb_hid.devices)

y_axis = AnalogIn(board.A0)
x_axis = AnalogIn(board.A1)
light = AnalogIn(board.A2)

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT

# Button
btna = DigitalInOut(board.GP6)
btna.switch_to_input(pull=Pull.UP)

btnb = DigitalInOut(board.GP7)
btnb.switch_to_input(pull=Pull.UP)

btnst = DigitalInOut(board.GP8)
btnst.switch_to_input(pull=Pull.UP)

btnse = DigitalInOut(board.GP9)
btnse.switch_to_input(pull=Pull.UP)

def get_joystick(pin):
  return ((pin.value / 65536) * 2) - 1
def get_voltage(pin):
	return (pin.value * 3.3) / 65536

threshold = 0.5

while True:
  x = get_joystick(x_axis)
  y = get_joystick(y_axis)
  if x <= 0.1 and x >= -0.1:
    x = 0
  if y <= 0.1 and y >= -0.1:
    y = 0
  if btnst.value:
    accel = 20
    if x <= threshold and y <= threshold and x >= -threshold and y >= -threshold:
      accel = 10
    x = int(x*accel)*1
    y = -int(y*accel)*1
    mouse.move(x=int(x), y=int(-y))
  else:
    if y != 0:
      time.sleep(1/abs(y*50))
    if y>0:
      y=1
    elif y<0:
      y=-1
    mouse.move(wheel=int(round(-y,1)))

  if not btna.value:
    mouse.press(Mouse.LEFT_BUTTON)
  else:
    mouse.release(Mouse.LEFT_BUTTON)
  if not btnb.value:
    mouse.press(Mouse.RIGHT_BUTTON)
  else:
    mouse.release(Mouse.RIGHT_BUTTON)
  if not btnse.value:
    mouse.press(Mouse.MIDDLE_BUTTON)
  else:
    mouse.release(Mouse.MIDDLE_BUTTON)