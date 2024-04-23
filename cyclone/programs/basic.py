import re, time, board, usb_cdc
import terminalio
from adafruit_display_text import label
from collections import OrderedDict
from digitalio import DigitalInOut, Direction, Pull

from thunder.display import Display
from thunder.mount_sd import init_sdcard
import thunder.input as controls
import thunder.utils as u

init_sdcard()

display = Display()

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False

term = label.Label(terminalio.FONT, text="",
color=0xFFFFFF, background_color=0x000000, x=0, y=5)

code = OrderedDict()

s = usb_cdc.console

def checkDigit(str):
  res=False
  for i in str:
    try:
      int(i)
      res=True
      break
    except:
      res=False
  return res
def parse(tree):
  n = 0
  val = 0
  while n <= len(tree)-1:
    i = tree[n]
    if i == "print":
      del tree[0]
      string = " ".join(tree)
      print(string)
      break
    if i == "echo":
      del tree[0]
      string = " ".join(tree)
      string = u.divide_chunks(string, 40)
      for i in string:
        term.text += i+"\n"
    if i == "scale":
      if checkDigit(tree[n+1]):
        term.scale = int(tree[n+1])
        term.y = 5+(5*int(tree[n+1]))
    if i == "cls":
      term.text = ""
      break
    if i == "led0":
      led.value = False
      break
    if i == "led1":
      led.value = True
      break
    if i == "run":
      j = 0
      l = list(code.keys())
      while j <= (len(code)-1):
        tree = code[l[j]].split(" ")
        res = parse(tree)
        if res != 0:
          j = l.index(res)+1
        else:
          j+=1
        k = s.read(2)
        if k == b'cc':
          break
      break
    if i == "goto":
      if checkDigit(tree[n+1]):
        nn = tree[n+1]
        tree = code[nn].split(" ")
        parse(tree)
        val = nn
      break
    if i == "wait":
      if checkDigit(tree[n+1]):
        time.sleep(float(tree[n+1]))
      break
    if i == "list":
      j = 0
      l = list(code.keys())
      while j <= (len(code)-1):
        print(l[j]+" "+code[l[j]])
        j+=1
      break
    if checkDigit(i):
      del tree[0]
      code[i] = " ".join(tree)
      break
    n+=1
  return val
def main():
  display.screen.append(term)
  while True:
    inp = input(">>> ")
    tree = inp.split(" ")
    parse(tree)

main()