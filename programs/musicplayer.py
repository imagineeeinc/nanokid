# A featureful wav player
# Folder traversal, shuffling changing play order, mono wav playback to speaker or 3.5mm
# Cover image per folder support, simply put the cover for the folder in 80x80 bmp format called 'cover80.bmp'
import board, time, os, io, gc, random
import displayio, terminalio
from adafruit_display_text import label

from audiocore import WaveFile
from audiopwmio import PWMAudioOut as AudioOut
from digitalio import DigitalInOut, Direction, Pull

from thunder.display import Display
from thunder.mount_sd import init_sdcard
import thunder.input as controls
import thunder.utils as u
from thunder.led import led
import thunder.sys as sys

init_sdcard()

display = Display()

# Init display
screen = display.screen
chunksize = 10

# Init Audio
# 0-speaker, 1-wired
output = 0
def init_speaker(out):
  if out == 0:
    return AudioOut(board.GP14)
  elif out == 1:
    return AudioOut(board.GP15)
audio = init_speaker(output)
decoder = None

# images
play_btn_image = displayio.OnDiskBitmap("/cyclone/musicplayer/play.bmp")
pause_btn_image = displayio.OnDiskBitmap("/cyclone/musicplayer/pause.bmp")
play_btn = displayio.TileGrid(play_btn_image, pixel_shader=play_btn_image.pixel_shader, x=8, y=200)

play_order_image = [
  displayio.OnDiskBitmap("/cyclone/musicplayer/no-order.bmp"),
  displayio.OnDiskBitmap("/cyclone/musicplayer/play-in-order.bmp"),
  displayio.OnDiskBitmap("/cyclone/musicplayer/repeat-list.bmp"),
  displayio.OnDiskBitmap("/cyclone/musicplayer/repeat.bmp")
]
play_order_btn = displayio.TileGrid(play_order_image[1], pixel_shader=play_order_image[0].pixel_shader, x=8+38, y=216)

speaker_image = displayio.OnDiskBitmap("/cyclone/musicplayer/speaker.bmp")
wired_image = displayio.OnDiskBitmap("/cyclone/musicplayer/wired.bmp")
audio_out_btn = displayio.TileGrid(speaker_image, pixel_shader=speaker_image.pixel_shader, x=8+38+20, y=216)

no_shuffle = displayio.OnDiskBitmap("/cyclone/musicplayer/no-shuffle.bmp")
yes_shuffle = displayio.OnDiskBitmap("/cyclone/musicplayer/shuffle.bmp")
shuffle_btn = displayio.TileGrid(no_shuffle, pixel_shader=no_shuffle.pixel_shader, x=8+38+2*20, y=216)

pointer_y = 2
pointer_jump = 15
pointer_image = displayio.OnDiskBitmap("/cyclone/musicplayer/pointer.bmp")
pointer = displayio.TileGrid(pointer_image, pixel_shader=pointer_image.pixel_shader, x=0, y=pointer_y)

# Text box
modal = label.Label(terminalio.FONT, text="",
color=0xc7dcd0, x=10, y=5)

default_notplaying = "..."
playing = label.Label(terminalio.FONT, text=default_notplaying,
color=0xdefaea, x=5, y=180, scale=2)
dur = label.Label(terminalio.FONT, text="00:00",
color=0xc7dcd0, x=47, y=205)

default_cover = displayio.Bitmap(80,80,1)
cover = default_cover
cover_pre = displayio.TileGrid(cover, pixel_shader=pointer_image.pixel_shader, x=240-80, y=240-80)

# Timer
start_timer = time.monotonic()

# playing settings
lastplayed = ""
played_now = False
# 0-no, 1-chronology, 2-repeat list, 3-replay
play_order = 1
play_screen_on = 30
screen_on_dur = 60
next_song = 0
shuffled = False

def play(filename, name):
  global decoder, repeat, play_order, played_now, start_timer, next_song
  force_quit = False
  gc.collect()
  file = open(filename, "rb")
  header = file.read(44)
  data_size = int.from_bytes(header[40:44], 'little')
  sample_rate = int.from_bytes(header[24:28], 'little')
  duration_seconds = data_size / (sample_rate * 2)
  mins=duration_seconds//60
  sec=duration_seconds%60
  dur.text = str(int(mins))+":"+"{:02d}".format(int(sec))
  if decoder == None:
    decoder = WaveFile(file)
  else:
    decoder.deinit()
    decoder = WaveFile(file)
  audio.play(decoder)
  play_btn.bitmap = pause_btn_image
  name = name.replace("-qm","")
  name = name.replace(".wav","")
  if len(name)>= 13:
    name = name[:9]+"..."
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
          if play_order < 3:
            play_order += 1
          play_order_btn.bitmap = play_order_image[play_order]
          time.sleep(0.5)
      else:
        display.backlight_on()
        led.value = False
        time.sleep(0.2)
      start_timer = time.monotonic()
    else:
      if controls.get_axis(controls.x_axis) < -0.9:
        next_song = -1
        audio.stop()
        file.close()
        time.sleep(0.2)
      if controls.get_axis(controls.x_axis) > 0.8:
        next_song = 1
        audio.stop()
        file.close()
        time.sleep(0.2)
    if time.monotonic() - start_timer >= play_screen_on:
      display.backlight_off()
      led.value = True
  play_btn.bitmap = play_btn_image
  playing.text = default_notplaying
  dur.text = "00:00"
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

# read list of files
def read_files(shuffle=False):
  inlist = os.listdir(root+path)
  if shuffle == True:
    newinlist = []
    while len(newinlist) < len(inlist):
      r = random.randint(0, len(inlist)-1)
      if inlist[r] not in newinlist:
        newinlist.append(inlist[r])
    inlist = newinlist
  else:
    inlist.sort()
  outlist = inlist.copy()
  shift = 0
  for i in range(0,len(inlist)):
    text = inlist[i]
    if os.stat(root+path+text)[0] == 16384:
      if shuffle == False:
        outlist[i-shift] = inlist[i] + "/"
      else:
        outlist.pop(i-shift)
        shift += 1
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
jump_distance=5

def clamp(n, min, max): 
  if n < min: 
    return min
  elif n > max: 
    return max
  else:
    return n
def draw_modal():
  global chunk
  if chunk > len(files)-1:
    chunk = len(files)-1
  dfiles = files[chunk]
  text = ""
  for i in range(0, len(dfiles)):
    t = dfiles[i]
    t = t.replace("-qm","")
    t = t.replace(".wav","")
    text += t+"\n"
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
  global path, files, cover
  path = parse_path(path, loc)
  files = read_files()
  global lastpoy, chunk, poy
  lastpoy = -1
  chunk = 0
  poy = 1
  draw_modal()
  draw_pointer()
  try:
    status = os.stat(root+path+"cover80.bmp")
    cover = displayio.OnDiskBitmap(root+path+"cover80.bmp")
    cover_pre.bitmap = cover
  except OSError:
    cover = default_cover
    cover_pre.bitmap = cover
    gc.collect()

def main():
  screen.append(play_btn)
  screen.append(play_order_btn)
  screen.append(audio_out_btn)
  screen.append(pointer)
  screen.append(modal)
  screen.append(playing)
  screen.append(dur)
  screen.append(shuffle_btn)
  screen.append(cover_pre)
  draw_modal()
  global played_now, play_order, start_timer, screen_on_dur, files, chunk, poy, audio, next_song, shuffled
  while True:
    if played_now and play_order == 3:
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
        if controls.get_btn(controls.btnse):
          shuffled = not shuffled
          files = read_files(shuffled)
          draw_modal()
          if shuffled:
            shuffle_btn.bitmap = yes_shuffle
          else:
            shuffle_btn.bitmap = no_shuffle
        elif files[chunk][poy].endswith("/"):
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
        if controls.get_btn(controls.btnse):
          sys.exit_to_shell()
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

main()