import board, busio
from adafruit_st7789 import ST7789
import displayio
from digitalio import DigitalInOut, Direction, Pull


class Display:
	def __init__(self, mosi = board.GP19, clk = board.GP18, cs = board.GP17, dc = board.GP16, scale=1):
		self.power = DigitalInOut(board.GP21)
		self.power.direction = Direction.OUTPUT
		self.power.value = False
		self.power_on()

		self.backlight = DigitalInOut(board.GP20)
		self.backlight.direction = Direction.OUTPUT
		self.backlight.value = False
		self.backlight_on()

		self.scale = scale
		try:
			displayio.release_displays()
			self.spi = busio.SPI(clock=clk, MOSI=mosi)
			self.display_bus = displayio.FourWire(self.spi, command=dc, chip_select=cs)
			self.display = ST7789(self.display_bus, width=240, height=240, rowstart=80, colstart=0)

			self.screen = displayio.Group(scale=self.scale, x=0, y=0)
			self.display.root_group = self.screen
		except OSError as error:
			print(error)
			return error
	def backlight_off(self):
		self.backlight.value = False
	def backlight_on(self):
		self.backlight.value = True
	def power_off(self):
		self.power.value = False
	def power_on(self):
		self.power.value = True
	