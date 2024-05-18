# A microphone talkback, connect a speaker to the headphone jack and hear what you say into the microphone
import board, time
import array, math, asyncio
import audiobusio, audiopwmio, audiocore
buzzer = audiopwmio.PWMAudioOut(board.GP15)

# Main program
mic = audiobusio.PDMIn(board.GP3, board.GP0, sample_rate=16000, bit_depth=16)
samples = array.array('H', [0] * 10000)

async def record():
	mic.record(samples, len(samples))
async def play():
	buzzer.play(audiocore.RawSample(samples, sample_rate=8000))
async def main():
	while True:
		record_task = asyncio.create_task(record())
		play_task = asyncio.create_task(play())
		await asyncio.gather(record_task, play_task)

asyncio.run(main())