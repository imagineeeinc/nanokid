# A rudementry basic lang interpreter
import time, board, usb_cdc, math, io
import terminalio
from adafruit_display_text import label
from collections import OrderedDict
from digitalio import DigitalInOut, Direction, Pull

from thunder.display import Display
from thunder.mount_sd import init_sdcard
import thunder.input as controls
import thunder.utils as u
import thunder.sys as sys

init_sdcard()

display = Display()

led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False

term = label.Label(terminalio.FONT, text="",
color=0xFFFFFF, background_color=0x000000, x=0, y=5)

code = OrderedDict()
var = {}

s = usb_cdc.console

def read_serial(serial):
  available = serial.in_waiting
  text = ""
  while available:
    raw = serial.read(available)
    text = raw.decode("utf-8")
    available = serial.in_waiting
  return text

def sort(code):
  myKeys = list(code.keys())
  myKeys.sort()
  res = OrderedDict()
  for i in myKeys:
    res[i] = code[i]
  return res
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
  global code
  n = 0
  val = 0
  while n <= len(tree)-1:
    i = tree[n]
    if i == "print":
      del tree[0]
      if tree[0][0] == "$":
        print(var[tree[0]])
      else:
        string = " ".join(tree)
        print(string)
      break
    if i == "echo":
      del tree[0]
      string = ""
      if tree[0][0] == "$":
        string = var[tree[0]]
      else:
        string = " ".join(tree)
      string = u.divide_chunks(str(string), 40)
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
      while j < len(code):
        tree = code[l[j]].split(" ")
        res = parse(tree)
        if res != 0:
          j = l.index(res)+1
        else:
          j+=1
        k = read_serial(s)
        if k == "C":
          break
      break
    if i == "goto":
      if checkDigit(tree[n+1]):
        nn = int(tree[n+1])
        tree = code[nn].split(" ")
        parse(tree)
        val = nn
      break
    if i == "wait":
      if checkDigit(tree[n+1]):
        time.sleep(float(tree[n+1]))
      break
    if i == "ls" or i == "list":
      j = 0
      l = list(code.keys())
      while j <= (len(code)-1):
        print(str(l[j])+" "+code[l[j]])
        j+=1
      break
    if i == "ld" or i == "load":
      content = io.open(tree[1], mode='r').read()
      prog_tree = content.split("\n")
      for pos in range(0, len(prog_tree)):
        code[pos+1] = prog_tree[pos]
        code = sort(code)
      break
    if i == "shift":
      if checkDigit(tree[n+1]):
        # take all the lines strored in code and shift the kets by tree[n+1]
        l = list(code.keys())
        temp = OrderedDict()
        for pos in range(0, len(l)):
          temp[l[pos]+int(tree[n+1])] = code[l[pos]]
        code = sort(temp)
        break
    if i == "exit":
      val = -1
      break
    if i == "mv":
      if int(tree[1]) in code:
        code[int(tree[2])] = code[int(tree[1])]
        code.pop(int(tree[1]))
        code = sort(code)
        break
    if i == "del":
      if int(tree[1]) in code:
        code.pop(int(tree[1]))
        break
    if checkDigit(i):
      del tree[0]
      code[int(i)] = " ".join(tree)
      code = sort(code)
      break
    elif i[0] == "$":
      if tree[1] == "=":
        del tree[0]
        del tree[0]
        var[i] = " ".join(tree)
      elif tree[1] == "mat":
        del tree[0]
        del tree[0]
        var[i] = eval(" ".join(tree))
    n+=1
  return val
def main():
  display.screen.append(term)
  while True:
    inp = input(">>> ")
    tree = inp.split(" ")
    status = parse(tree)
    if status == -1:
      break
main()
sys.exit_to_shell()