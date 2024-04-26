# A controller that maps to keyboard the Gameboy layout
# a:z b:x start:Enter select:RightShift
# Up:ArrowUp Down:ArrowDown Left:ArrowLeft Right:ArrowRight
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import time

import thunder.input as controls


# Initialize Keyboard
kbd = Keyboard(usb_hid.devices)
# Sensiytivity of thumbstick
sensitivity = 0.8

while True:
    # A
    if controls.get_btn(controls.btna):
        kbd.press(Keycode.Z)
    else:
        kbd.release(Keycode.Z)
    # B
    if controls.get_btn(controls.btnb):
        kbd.press(Keycode.X)
    else:
        kbd.release(Keycode.X)
    # Start
    if controls.get_btn(controls.btnst):
        kbd.press(Keycode.ENTER)
    else:
        kbd.release(Keycode.ENTER)
    # Select
    if controls.get_btn(controls.btnse):
        kbd.press(Keycode.RIGHT_SHIFT)
    else:
        kbd.release(Keycode.RIGHT_SHIFT)
    # arrows
    # horizontal
    if controls.get_axis(controls.x_axis) < -sensitivity:
        kbd.press(Keycode.LEFT_ARROW)
    elif controls.get_axis(controls.x_axis) > sensitivity:
        kbd.press(Keycode.RIGHT_ARROW)
    else:
        kbd.release(Keycode.LEFT_ARROW)
        kbd.release(Keycode.RIGHT_ARROW)
    # vertical
    if controls.get_axis(controls.y_axis) < -sensitivity:
        kbd.press(Keycode.UP_ARROW)
    elif controls.get_axis(controls.y_axis) > sensitivity:
        kbd.press(Keycode.DOWN_ARROW)
    else:
        kbd.release(Keycode.UP_ARROW)
        kbd.release(Keycode.DOWN_ARROW)
    