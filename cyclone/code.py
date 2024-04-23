import board, time, os, io, gc, sys, json, supervisor
from thunder.mount_sd import init_sdcard
import thunder.input as controls
import thunder.utils as u

from thunder.display import Display
import terminalio
from adafruit_display_text import label
from adafruit_display_shapes.triangle import Triangle

from digitalio import DigitalInOut, Direction, Pull

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False

boot = json.loads(io.open('/cyclone/cyclone.json', 'r').read())['auto_boot']
if boot != "0" and controls.get_btn(controls.btnb) == False:
  location = '/cyclone/'+boot+'.py'
  supervisor.set_next_code_file(location)
  supervisor.reload()

# Init SD card
init_sdcard()
# Init display
disp = Display()
screen = disp.screen
chunksize = 16

# Text box
modal = label.Label(terminalio.FONT, text="",
color=0xc7dcd0, background_color=0x000000, x=20, y=5)
screen.append(modal)

pointer = Triangle(0, 0, 10, 5, 0, 10, fill=0xc7dcd0, outline=0xFFFFFF)
screen.append(pointer)

# menu mode
menu = [
  ["Charging Mode", "chr"],
  ["Wifi Connect", "wifi"]
]
menu_mode = False

# Explorer setup
root = "/"
path = "cyclone/"

# read list of files
def read_files():
  inlist = os.listdir(root+path)
  inlist.sort()
  outlist = os.listdir(root+path)
  outlist.sort()
  shift = 0
  for i in range(0,len(inlist)):
    text = inlist[i]
    if not (text.endswith(".py")) :
      outlist.pop(i-shift)
      shift += 1
    elif text == "__init__.py" :
      outlist.pop(i-shift)
      shift += 1
  return u.divide_chunks(outlist, chunksize)

# files
files = read_files()

# UI vars
poy=0
chunk=0
jump_distance=4

def clamp(n, min, max): 
  if n < min: 
    return min
  elif n > max: 
    return max
  else:
    return n
def draw_modal():
  text = ""
  if menu_mode == False:
    dfiles = files[chunk]
    for i in range(0, len(dfiles)):
      text += dfiles[i]+"\n"
  else:
    dfiles = menu
    for i in range(0, len(dfiles)):
      text += dfiles[i][0]+"\n"
  del dfiles
  gc.collect()
  modal.text = text

def draw_pointer():
  pointer.y = poy*15

def draw():
  global poy
  global chunk
  global files
  if controls.get_axis(controls.y_axis) > 0.2:
    if controls.get_btn(controls.btnse):
      poy+=jump_distance
    else:
      poy+=1
  elif controls.get_axis(controls.y_axis) < -0.2:
    if controls.get_btn(controls.btnse):
      poy-=jump_distance
    else:
      poy-=1
  if poy <= -1:
    if chunk == 0:
      poy = 0
    else:
      chunk-=1
      poy=chunksize-1
      draw_modal()
  if poy >= chunksize:
    if chunk == len(files)-1:
      poy = chunksize-1
    else:
      chunk+=1
      poy=0
      draw_modal()
  if poy >= len(files[chunk])-1:
    poy = len(files[chunk])-1
  draw_pointer()
  gc.collect()

draw_modal()
while True:
  draw()
  if controls.get_btn(controls.btna):
    if menu_mode == False:
      location = root+path+files[chunk][poy]
      supervisor.set_next_code_file(location)
      supervisor.reload()
      break
    else:
      if menu[poy][1] == "chr":
        break
  elif controls.get_btn(controls.btnse):
    menu_mode = not menu_mode
    draw_modal()
    time.sleep(0.5)
  time.sleep(1/12)
