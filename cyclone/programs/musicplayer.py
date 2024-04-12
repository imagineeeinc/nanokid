import board, time, os, io, gc
import displayio, terminalio
from adafruit_display_text import label

from audiocore import WaveFile
from audiopwmio import PWMAudioOut as AudioOut

import thunder.utils as u

display = None
controls = None

led = None

boot_btns = []

# Init display
screen = None
chunksize = 8

# Init Audio
# 0-speaker, 1-wired
output = 0
def init_speaker(out):
  if out == 0:
    return AudioOut(board.GP14)
  elif out == 1:
    return AudioOut(board.GP15)
#wired = AudioOut(board.GP15)
audio = init_speaker(output)
decoder = None

# images
play_btn_image = displayio.OnDiskBitmap("/play.bmp")
pause_btn_image = displayio.OnDiskBitmap("/pause.bmp")
play_btn = displayio.TileGrid(play_btn_image, pixel_shader=play_btn_image.pixel_shader, x=8, y=200)

play_order_image = [
  displayio.OnDiskBitmap("/no-order.bmp"),
  displayio.OnDiskBitmap("/play-in-order.bmp"),
  displayio.OnDiskBitmap("/repeat-list.bmp"),
  displayio.OnDiskBitmap("/shuffle.bmp"),
  displayio.OnDiskBitmap("/repeat.bmp")
]
play_order_btn = displayio.TileGrid(play_order_image[1], pixel_shader=play_order_image[0].pixel_shader, x=8+38, y=216)

speaker_image = displayio.OnDiskBitmap("/speaker.bmp")
wired_image = displayio.OnDiskBitmap("/wired.bmp")
audio_out_btn = displayio.TileGrid(speaker_image, pixel_shader=speaker_image.pixel_shader, x=8+38+20, y=216)

pointer_y = 2
pointer_jump = 15
pointer_image = displayio.OnDiskBitmap("/pointer.bmp")
pointer = displayio.TileGrid(pointer_image, pixel_shader=pointer_image.pixel_shader, x=0, y=pointer_y)

# Text box
modal = label.Label(terminalio.FONT, text="",
color=0xc7dcd0, x=10, y=5)


default_notplaying = "..."
playing = label.Label(terminalio.FONT, text=default_notplaying,
color=0xdefaea, x=5, y=180, scale=2)

# Timer
start_timer = time.monotonic()

# playing settings
lastplayed = ""
played_now = False
# 0-no, 1-chronology, 2-repeat list, 3-shuffle, 4-replay
play_order = 1
play_screen_on = 30
screen_on_dur = 60
next_song = 0

def play(filename, name):
  global decoder, repeat, play_order, played_now, start_timer, next_song
  force_quit = False
  gc.collect()
  file = open(filename, "rb")
  if decoder == None:
    decoder = WaveFile(file)
  else:
    decoder.deinit()
    decoder = WaveFile(file)
  audio.play(decoder)
  # screen.pop(screen.index(play_btn))
  # screen.append(pause_btn)
  play_btn.bitmap = pause_btn_image
  if len(name)>= 19:
    name = name[:16]+"..."
  playing.text = name
  time.sleep(0.5)
  while audio.playing:
    if controls.get_btn(controls.btna):
      if audio.paused:
        audio.resume()
        play_btn.bitmap = pause_btn_image
      else:
        audio.pause()
        play_btn.bitmap = play_btn_image
      time.sleep(0.5)
    if controls.get_btn(controls.btnb):
      audio.stop()
      file.close()
      force_quit = True
      if display.backlight.value == False:
        display.backlight_on()
        led.value = False
        time.sleep(0.2)
      start_timer = time.monotonic()
      break
    if controls.get_btn(controls.btnst):
      if display.backlight.value == False:
        display.backlight_on()
        led.value = False
        time.sleep(0.2)
      start_timer = time.monotonic()
    if controls.get_btn(controls.btnse):
      if display.backlight.value == True:
        if controls.get_axis(controls.x_axis) < -0.4:
          if play_order > 0:
            play_order -= 1
          play_order_btn.bitmap = play_order_image[play_order]
          time.sleep(0.5)
        if controls.get_axis(controls.x_axis) > 0.4:
          if play_order < 4:
            play_order += 1
          play_order_btn.bitmap = play_order_image[play_order]
          time.sleep(0.5)
      else:
        display.backlight_on()
        led.value = False
        time.sleep(0.2)
      start_timer = time.monotonic()
    else:
      if controls.get_axis(controls.x_axis) < -0.4:
        next_song = -1
        audio.stop()
        file.close()
        time.sleep(0.2)
      if controls.get_axis(controls.x_axis) > 0.4:
        next_song = 1
        audio.stop()
        file.close()
        time.sleep(0.2)
    if time.monotonic() - start_timer >= play_screen_on:
      display.backlight_off()
      led.value = True
  play_btn.bitmap = play_btn_image
  playing.text = default_notplaying
  if force_quit == False:
    played_now = True
  else:
    played_now = False
  gc.collect()
  time.sleep(0.2)

# Explorer setup
root = "/sd/"
path = "music/"

def parse_path(cur, next):
  stack = cur[0:len(cur)-1].split("/")
  if next == "../" :
    stack.pop()
  else:
    stack.append(next[:len(next)-1])
  return "/".join(stack)+"/"


# chunkify
def divide_chunks(l, n):
  list=[]
  for i in range(0, len(l), n): 
    x = i
    list.append(l[x:x+n]) 
  return list
# read list of files
def read_files():
  inlist = os.listdir(root+path)
  inlist.sort()
  outlist = os.listdir(root+path)
  outlist.sort()
  shift = 0
  for i in range(0,len(inlist)):
    text = inlist[i]
    if os.stat(root+path+text)[0] == 16384:
      outlist[i-shift] = inlist[i] + "/"
    elif not (text.endswith(".wav")) :
      outlist.pop(i-shift)
      shift += 1
  outlist.insert(0, "../")
  return u.divide_chunks(outlist, chunksize)

# files
files = read_files()

# UI vars
lastpoy=-1
poy=1
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
  dfiles = files[chunk]
  text = ""
  for i in range(0, len(dfiles)):
    # if i == poy:
    #   text +="> "
    text += dfiles[i]+"\n"
  del dfiles
  gc.collect()
  modal.text = text

def draw_pointer():
  pointer.y = pointer_y+pointer_jump*poy

def draw():
  global lastpoy
  global poy
  global chunk
  global files
  global start_timer
  if controls.get_axis(controls.y_axis) > 0.2:
    if display.backlight.value == True:
      if controls.get_btn(controls.btnse):
        poy+=jump_distance
      else:
        poy+=1
    else:
      display.backlight_on()
      led.value = False
      time.sleep(0.2)
    start_timer = time.monotonic()
  elif controls.get_axis(controls.y_axis) < -0.2:
    if display.backlight.value == True:
      if controls.get_btn(controls.btnse):
        poy-=jump_distance
      else:
        poy-=1
    else:
      display.backlight_on()
      led.value = False
      time.sleep(0.2)
    start_timer = time.monotonic()
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
  if poy != lastpoy:
    draw_pointer()
  lastpoy = poy
  gc.collect()

def to_dir(loc):
  global path, files
  path = parse_path(path, loc)
  files = read_files()
  global lastpoy, chunk, poy
  lastpoy = -1
  chunk = 0
  poy = 1
  draw_modal()
  draw_pointer()
  time.sleep(0.2)

def main():
  global screen
  screen = display.screen
  screen.append(play_btn)
  screen.append(play_order_btn)
  screen.append(audio_out_btn)
  screen.append(pointer)
  screen.append(modal)
  screen.append(playing)
  if controls.btnst in boot_btns:
    annoy()
  draw_modal()
  global played_now, play_order, start_timer, screen_on_dur, files, chunk, poy, audio, next_song
  while True:
    if played_now and play_order == 4:
      play(root+path+files[chunk][poy], files[chunk][poy])
    elif played_now and (play_order == 1 or play_order == 2):
      if next_song != 0:
        poy+=next_song
        next_song = 0
      else:
        poy+=1
      if poy >= chunksize or poy >= len(files[chunk]):
        if chunk == len(files)-1:
          if play_order == 2:
            poy = 1
            chunk = 0
            draw_modal()
            draw_pointer()
            play(root+path+files[chunk][poy], files[chunk][poy])
          else:
            poy = chunksize-1
            played_now = False
            draw_modal()
        else:
          chunk+=1
          poy=0
          draw_modal()
          draw_pointer()
          play(root+path+files[chunk][poy], files[chunk][poy])
      else:
        draw_pointer()
        play(root+path+files[chunk][poy], files[chunk][poy])
    draw()
    time.sleep(1/12)
    if controls.get_btn(controls.btna):
      if display.backlight.value == True:
        if files[chunk][poy].endswith("/"):
          #path += files[chunk][poy]
          to_dir(files[chunk][poy])
        elif files[chunk][poy].endswith(".wav"):
          play(root+path+files[chunk][poy], files[chunk][poy])
      else:
        display.backlight_on()
        led.value = False
        time.sleep(0.2)
      start_timer = time.monotonic()
    elif controls.get_btn(controls.btnb):
      if display.backlight.value == True:
        to_dir("../")
      else:
        display.backlight_on()
        led.value = False
        time.sleep(0.2)
      start_timer = time.monotonic()
    elif controls.get_btn(controls.btnse):
        if display.backlight.value == True:
          if controls.get_axis(controls.x_axis) < -0.4:
            output = 0
            audio_out_btn.bitmap = speaker_image
            audio.deinit()
            audio = init_speaker(output)
            time.sleep(0.5)
          if controls.get_axis(controls.x_axis) > 0.4:
            output = 1
            audio_out_btn.bitmap = wired_image
            audio.deinit()
            audio = init_speaker(output)
            time.sleep(0.5)
        else:
          display.backlight_on()
          led.value = False
          time.sleep(0.2)
        start_timer = time.monotonic()
    if time.monotonic() - start_timer >= screen_on_dur:
      display.backlight_off()
      led.value = True
    gc.collect()