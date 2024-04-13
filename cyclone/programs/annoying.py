from pwmio import PWMOut
import board, time

display = None
controls = None
led = None

def main():
	tone = PWMOut(board.GP14, variable_frequency=True)
	volume = 1500
	tone.duty_cycle=0
	freq = 15000
	tone.duty_cycle = volume
	tone.frequency = freq
	led.value = True
	while True:
		if controls.get_axis(controls.y_axis) >= 0.2 or controls.get_axis(controls.y_axis) <= -0.2:
			freq += int(controls.get_axis(controls.y_axis)*100)
		if controls.get_btn(controls.btna):
			volume += 100
		elif controls.get_btn(controls.btnb):
			volume -= 100
		if freq <= 10:
			freq = 100
		if volume <= 10:
			volume = 100
		tone.frequency = freq
		tone.duty_cycle = volume
		time.sleep(1/24)
