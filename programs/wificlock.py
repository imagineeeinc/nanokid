# A nice handheld clock with time of currewnt location and weather
# Make sure to have the space mono font converted to pcf format with 24 pt size and located at the root of the sdcard (file name: 'spacemono24.pcf')
# ttf2bdf: https://learn.adafruit.com/custom-fonts-for-pyportal-circuitpython-display/use-otf2bdf
# convert to pcf for faster loads: https://learn.adafruit.com/custom-fonts-for-pyportal-circuitpython-display/convert-to-pcf
# Make sure the 'earth-bg.bmp' is on the root of the sd card

# When green LED is on connectring to wifi and retriving time, when off retriving finish and display should turn on

import board, gc, os, time, rtc

from thunder.led import led
from thunder.mount_sd import init_sdcard
from thunder.wifi import Wifi
import circuitpython_schedule as schedule

led.value = True
init_sdcard()

# Setup wifi
wifi = Wifi()
wifi.connect()
wifi.setup_http()

# Time setting
global clock
def get_time():
  url = "https://worldtimeapi.org/api/ip/"
  print("Making a request for current time...")
  response = wifi.fetch(url)
  if not hasattr(response, "json"):
    print(f"Failed to fetch:\n{response}")
    return
  print("Response recieved for current time")

  json = response.json()
  unixtime = json["unixtime"]
  raw_offset = json["raw_offset"]
  dst_offset = json["dst_offset"]
  location_time = unixtime + raw_offset + dst_offset
  current_time = time.localtime(location_time)

  global clock
  clock = rtc.RTC()
  clock.datetime = time.struct_time(current_time)

global temp
global weather
global wind
def get_weather():
  url = "http://ip-api.com/json/"
  print("Making a request for location...")
  response = wifi.fetch(url)
  if not hasattr(response, "json"):
    print(f"Failed to fetch:\n{response}")
    return
  print("Response recieved for location")

  json = response.json()
  lat = json["lat"]
  lon = json["lon"]

  url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={os.getenv('OPENWEATHER_API_KEY')}"
  print("Making a request for weather...")
  response = wifi.fetch(url)
  if not hasattr(response, "json"):
    print(f"Failed to fetch:\n{response}")
    return
  print("Response recieved for weather")

  json = response.json()
  global temp
  global weather
  global wind
  temp = int(json["main"]["temp"])
  weather = json["weather"][0]["main"]
  wind = json["wind"]["speed"]#m/s

get_time()
gc.collect()
get_weather()
gc.collect()

# Schedule set
schedule.every().day.at("02:01").do(get_time)
schedule.every().hour.at(":00").do(get_weather)
print("Schedule set for getting time at 02:01 and weather every one hour")

led.value = False

# Display import
import displayio
from thunder.display import Display
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label

# Display Setup
scale = 1
display = Display()
screen = display.screen

# Font
spacefont = bitmap_font.load_font("/sd/spacemono24.pcf")
print("Loaded font")

# Values
length = int(240/scale)
half = int(length/2)
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# BG
earth = displayio.OnDiskBitmap("/sd/earth-bg.bmp")
bg = displayio.TileGrid(earth, pixel_shader=earth.pixel_shader, x=0, y=240-100)
screen.append(bg)

# Drawing
gc.collect()
time_box = label.Label(spacefont, text="00:00", color=0xFFFFFF, x=5, y=20, scale=2)# terminalio.FONT
screen.append(time_box)
seconds_box = label.Label(spacefont, text="00", color=0xC0C0C0, x=length-25, y=55, scale=1, label_direction="UPR")# terminalio.FONT
screen.append(seconds_box)
date_box = label.Label(spacefont, text="000 00/00", color=0xA0A0A0, x=5, y=35*2, scale=1)# terminalio.FONT
screen.append(date_box)
temp_box = label.Label(spacefont, text="00C 00.00m/s", color=0xA0A0A0, x=5, y=35*3, scale=1, line_spacing=0.6)# terminalio.FONT
screen.append(temp_box)

seconds_pass = clock.datetime.tm_sec
def draw_time():
  time_box.text = f"{clock.datetime.tm_hour:02d}:{clock.datetime.tm_min:02d}"
  date_box.text = f"{days[clock.datetime.tm_wday]} {clock.datetime.tm_mday:02d}/{clock.datetime.tm_mon:02d}"
  temp_box.text = f"{temp:02d}C {wind}m/s\n{weather}"
def draw():
  global seconds_pass
  seconds_pass = clock.datetime.tm_sec
  if seconds_pass >= 0 and seconds_pass <= 1:
    draw_time()
  seconds_box.text = f"{clock.datetime.tm_sec:02d}"

print("Drawing")
draw_time()

def mem_free():
  print(f"mem free: {gc.mem_free()}")

schedule.every(1).hour.do(mem_free)

while True:
  draw()
  gc.collect()
  schedule.run_pending()
  time.sleep(0.2)