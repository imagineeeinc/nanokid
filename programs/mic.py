# A simple microphone loudness indicator

import time
import array
import math
import board
import audiobusio

from adafruit_display_shapes.rect import Rect

from thunder.display import Display

display = Display()
# Remove DC bias before computing RMS.
def mean(values):
  return sum(values) / len(values)


def normalized_rms(values):
  minbuf = int(mean(values))
  samples_sum = sum(
    float(sample - minbuf) * (sample - minbuf)
    for sample in values
  )

  return math.sqrt(samples_sum / len(values))


# Main program
mic = audiobusio.PDMIn(board.GP3, board.GP0, sample_rate=16000, bit_depth=16)
samples = array.array('H', [0] * 160)

r = Rect(0, 230, 240, 10, fill=0xFFAAFF)
display.screen.append(r)

while True:
	mic.record(samples, len(samples))
	magnitude = normalized_rms(samples)
	print(int(magnitude))
	r.y = int(magnitude/2000*230)
	time.sleep(0.1)