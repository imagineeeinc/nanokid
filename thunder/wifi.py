import board, os
import ssl, wifi, socketpool, adafruit_requests, mdns

class Wifi:
	def __init__(self):
		self._connected = False
		self.ipv4 = None
		self.wifi = wifi
		self.radio = wifi.radio
		self.ssl = ssl
		self.pool = None
		self.ssid = None
		self.password = None
		self.requests = None

	def connect(self, ssid=None, password=None):
		if ssid != None and password != None:
			self.ssid = ssid
			self.password = password
		else:
			no = 0
			try:
				no = int(os.getenv("WIFIS"))
			except(e):
				pass
			if no > 0:
				scaned = self.scan_wifi()
				for i in range(no):
					if os.getenv("WIFI_SSID"+str(i)) in scaned:
						self.ssid = os.getenv("WIFI_SSID"+str(i))
						self.password = os.getenv("WIFI_PASSWORD"+str(i))
						break
				if self.ssid == None:
					print("couldn't find a network to connect to")
					return False
			else:
				self.ssid = os.getenv("WIFI_SSID")
				self.password = os.getenv("WIFI_PASSWORD")

		wifi.radio.start_station()
		wifi.radio.connect(self.ssid, self.password)
		if wifi.radio.connected:
			self._connected = True
			self.ipv4 = wifi.radio.ipv4_address
			return True
		else:
			self._connected = False
			return False

	def scan_wifi(self, sort_by=1, order=True):
		access_points = []
		# Scan for WiFi networks
		for networks in (wifi.radio.start_scanning_networks()):
			s = "."*(20-len(str(networks.ssid, "utf-8")))
			access_points.append(networks.ssid)
		wifi.radio.stop_scanning_networks()
		return access_points

	def create_pool(self):
		self.pool = socketpool.SocketPool(wifi.radio)
		return self.pool

	def setup_http(self):
		if self.pool == None:
			self.create_pool()
		self.requests = adafruit_requests.Session(self.pool, ssl.create_default_context())
		return self.requests

	def fetch(self, url):
		try:
			return self.requests.get(url)
		except RuntimeError as er:
			return er
	
	def mdns_setup(self, addr="nanokid", p=5000):
		self.mdns_server = mdns.Server(self.wifi.radio)
		self.mdns_server.hostname = addr
		self.mdns_server.advertise_service(service_type="_http", protocol="_tcp", port=p)
		self.mdns_addr=addr+".local:"+p