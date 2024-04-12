import board
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction, Pull

y_axis = AnalogIn(board.A0)
x_axis = AnalogIn(board.A1)

btna = DigitalInOut(board.GP6)
btna.switch_to_input(pull=Pull.UP)

btnb = DigitalInOut(board.GP7)
btnb.switch_to_input(pull=Pull.UP)

btnst = DigitalInOut(board.GP8)
btnst.switch_to_input(pull=Pull.UP)

btnse = DigitalInOut(board.GP9)
btnse.switch_to_input(pull=Pull.UP)

def get_btn(button):
	return not button.value

def get_axis(axis):
  return ((axis.value / 65536) * 2) - 1