import board
from analogio import AnalogIn

light = AnalogIn(board.A2)

def get_light_intensity():
	return (light.value * 3.3) / 65536