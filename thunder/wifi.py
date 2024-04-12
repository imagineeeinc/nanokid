import board, os
import ssl, wifi, socketpool, adafruit_requests

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

	def connect(self, ssid=os.getenv("WIFI_SSID"), password=os.getenv("WIFI_PASSWORD")):
		self.ssid = ssid
		self.password = password
		wifi.radio.start_station()
		wifi.radio.connect(self.ssid, self.password)
		if wifi.radio.connected:
			self._connected = True
			self.ipv4 = wifi.radio.ipv4_address
			return True
		else:
			self._connected = False
			return False

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