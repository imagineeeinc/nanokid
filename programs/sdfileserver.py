# A file server to serve files from the /sd directory
import board, os

import socketpool
from adafruit_httpserver import Server, MIMETypes, FileResponse

from thunder.wifi import Wifi
from thunder.mount_sd import init_sdcard

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
  return FileResponse(request, path, "/sd")

print(os.listdir("/sd"))
server.serve_forever(str(wifi.radio.ipv4_address))
