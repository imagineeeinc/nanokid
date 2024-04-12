# Make sure the sd card is <32gb and is formated using the official sdcard formatter tool for highest compatibility (probably fat32 or fat16 will also work)

import board, busio, sdcardio, storage

# Globals
sdcard = None
vfs = None
def init_sdcard(sck=board.GP10, si=board.GP11, so=board.GP12, cs=board.GP13):
	spi = busio.SPI(sck, si, so)
	global sdcard, vfs
	sdcard = sdcardio.SDCard(spi, cs)
	vfs = storage.VfsFat(sdcard)
	storage.mount(vfs, '/sd')