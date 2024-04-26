# A file server to serve files from the /sd directory
import board, os

import socketpool
from adafruit_httpserver import Server, MIMETypes, FileResponse, Response

from thunder.wifi import Wifi
from thunder.mount_sd import init_sdcard

from thunder.display import Display
import displayio, terminalio, time
from adafruit_display_text import label

display = Display()

info = label.Label(terminalio.FONT,
color=0xFFFFFF, x=0, y=150,
text="use /?q=<file> to open files and end\nin a `/` to see list of files\nin a directory.")
display.screen.append(info)

MIMETypes.configure(
  default_to="text/plain",
  # Unregistering unnecessary MIME types can save memory
  keep_for=[".html", ".css", ".js", ".mp3", ".wav", ".bmp"]
)

# sd card
init_sdcard()

# Setup wifi
wifi = Wifi()
wifi.connect()
wifi.create_pool()
wifi.mdns_setup()

server = Server(wifi.pool, "/sd", debug=True)

@server.route("/")
def base(request: Request):
  path = request.query_params.get("q")
  path = path.replace("%20", " ")
  if path.endswith("/"):
    res = ""
    for i in os.listdir("/sd"+path):
      if os.stat("/sd"+path+i)[0] == 16384:
        i+="/"
      res+="<a href=\"/?q="+path+i+"\">"+i+"</a><br>"
    return Response(request, body=res, content_type="text/html")
  return FileResponse(request, path, "/sd")

l = label.Label(terminalio.FONT, text=str(wifi.radio.ipv4_address)+":5000\nor\nnanokid.local:5000",
color=0xFFFFFF, x=5, y=10, scale=2)
display.screen.append(l)

print(os.listdir("/sd"))
server.serve_forever(str(wifi.radio.ipv4_address))
