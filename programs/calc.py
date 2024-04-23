import board, time
import displayio, terminalio
from adafruit_display_text import label
from adafruit_display_shapes.triangle import Triangle

from digitalio import DigitalInOut, Direction, Pull

from thunder.display import Display
from thunder.mount_sd import init_sdcard
import thunder.input as controls

init_sdcard()

display = Display()

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False

def calc(txt, cur, m):
  last=""
  left = ""
  for n in txt:
    if n in "01234567890+-*/.":
      left += n
    if n == "M":
      left += str(m)
    if n == "A":
      left += str(cur)
  return eval(left)

def main():
  global display, controls, led
  btns = [
    ["7", "8", "9", ">c", "Ans", "M", ">m", ">M"],
    ["4", "5", "6", "*", "/", "^", "sq", "root"],
    ["1", "2", "3", "+", "-", "sin", "cos", "tan"],
    ["0", ".", "(", ")", ">=", "^2", ",", "log"],
    ["", "", "", "", "e", "pi", "", ""]
  ]
  btn = label.Label(terminalio.FONT, text="7 8 9 C A M  =M M+\n4 5 6 * / ^  sq _ro\n1 2 3 + - si co ta\n0 . ( ) = ^2 ,  log\n        e pi",
  color=0xFFFFFF, background_color=0x000000, x=10, y=80, scale = 2)
  display.screen.append(btn)           
  preview = label.Label(terminalio.FONT, text="",
  color=0xFFFFFF, background_color=0x000000, x=5, y=10, scale = 2)
  display.screen.append(preview)
  last_val = label.Label(terminalio.FONT, text="",
  color=0xFFFFFF, background_color=0x000000, x=5, y=60)
  cur_val = label.Label(terminalio.FONT, text="",
  color=0xFFFFFF, background_color=0x000000, x=5, y=40, scale = 2)
  display.screen.append(last_val)
  display.screen.append(cur_val)
  pointer = Triangle(0, 0, 5, 5, 0, 10, fill=0x330033, outline=0xFFFFFF)
  pointer.y = 75+30
  display.screen.append(pointer)

  poy = 0
  pox = 0

  buffer=""
  last_res = 0
  cur_res = 0
  m = 0
  while True:
    # Update
    if controls.get_axis(controls.y_axis) > 0.2:
      poy+=1
      if poy >= 4:
        poy = 4
    elif controls.get_axis(controls.y_axis) < -0.2:
      poy-=1
      if poy <= 0:
        poy = 0
    if controls.get_axis(controls.x_axis) > 0.2:
      pox+=1
      if pox >= 7:
        pox = 7
    elif controls.get_axis(controls.x_axis) < -0.2:
      pox-=1
      if pox <= 0:
        pox = 0
    
    if controls.get_btn(controls.btna):
      if not btns[poy][pox].startswith(">"):
        buffer += btns[poy][pox]
      else:
        if btns[poy][pox][1] == "c":
          buffer = ""
        elif btns[poy][pox][1] == "m":
          m = cur_res
        elif btns[poy][pox][1] == "M":
          m += cur_res
        elif btns[poy][pox][1] == "=":
          last_res = cur_res
          cur_res = calc(buffer, cur_res, m)
      preview.text = buffer
      cur_val.text = str(cur_res)
      last_val.text = str(last_res)
      time.sleep(0.1)
    if controls.get_btn(controls.btnse):
      last_res = cur_res
      cur_res = calc(buffer, cur_res, m)
      preview.text = buffer
      cur_val.text = str(cur_res)
      last_val.text = str(last_res)
    if controls.get_btn(controls.btnb):
      buffer = buffer[:len(buffer)-1]
      preview.text = buffer
      time.sleep(0.1)
    # Draw
    pointer.y = 75+(poy*30)
    if pox < 6:
      pointer.x = pox*24
    else:
      pointer.x = 156+(pox-6)*36
    time.sleep(0.1)

main()