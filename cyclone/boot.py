import storage
import board, digitalio, supervisor

storage.remount("/", readonly=False)

m = storage.getmount("/")
# m.label = "CIRCUITPY"
m.label = "NANOKID"

btnst = digitalio.DigitalInOut(board.GP8)
btnst.switch_to_input(pull=digitalio.Pull.UP)

btnse = digitalio.DigitalInOut(board.GP9)
btnse.switch_to_input(pull=digitalio.Pull.UP)

if btnst.value or btnse.value:
	storage.remount("/", readonly=True)
	storage.enable_usb_drive()
else:
	storage.remount("/", readonly=False)
	storage.disable_usb_drive()