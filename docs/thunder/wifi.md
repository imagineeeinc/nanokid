# WIFI
All NanoKid's come pre assembled with a RaspberryPi Pico W, which is has wireless functionality built in. This includes Bluetooth and Wifi.

This module provides helpers that abstracts the wireless capabilities.

## Example
Please read on how to safely store and use your [Wifi detail](#setting-up-safe-wifi-connections) in code.
```python
from thunder.wifi import Wifi

wifi = Wifi()
# Wifi detatils stored in 'settings.toml'
wifi.connect()
wifi.setup_http()

# Prints out your ip
print(wifi.fetch("https://icanhazip.com").text)
```

## API Reference

- `thunder.wifi`
  - [`Wifi`](#class-wifi)

### `class Wifi`
The main object used to abstract the Wifi for usage.
- Properties
  - `_connected: False`: `True` when connected to an AP (access point), `False` when not connected to a AP.
  - `ipv4: None`: When connected to an AP (access point), it represents the device's IP address.
  - `wifi: wifi`: Represents the [native Wifi](https://docs.circuitpython.org/en/latest/shared-bindings/wifi/index.html#module-wifi) module in CircuitPython.
  - `radio: wifi.radio`: Represents the [radio property from the native Wifi](https://docs.circuitpython.org/en/latest/shared-bindings/wifi/index.html#wifi.Radio) module in CircuitPython.
  - `ssl: ssl`: Represents the [native SSL](https://docs.circuitpython.org/en/latest/shared-bindings/ssl/index.html) module in CircuitPython.
  - `pool: None`: Default is `None`, but when create_pool() function is ran, a [`socketpool.SocketPool`](https://docs.circuitpython.org/en/latest/shared-bindings/socketpool/index.html#socketpool.SocketPool) is created and stored.
  - `ssid: None`: Stores the current SSID when connected to an AP (access point).
  - `password: None`: Stores the current password for the connected AP (access point).
  - `requests: None`: When a [`adafruit_requests.Session`](https://docs.circuitpython.org/projects/requests/en/latest/api.html#adafruit_requests.Session) class is created, it's stored here used for http requests.
- Functions
  - `connect(ssid, password)`: connects to an AP (access point) with the specified SSID and password, if not specified tries to automatically connect with values from `settings.toml`, read more on [setting up multiple networks](#setting-up-multiple-wifi-connections); if you are using a hidden network, it won't work, so pass in the values using `os.getenv("WIFI_SSID")` and `os.getenv("WIFI_PASSWORD")` to securely store and access the values.
    - `ssid: os.getenv("WIFI_SSID")`: Default takes the value stored in [`settings.toml`](https://docs.circuitpython.org/en/latest/docs/environment.html) as `WIFI_SSID`. SSID of the AP (access point).
    - `password: os.getenv("WIFI_PASSWORD")`: Default takes the value stored in [`settings.toml`](https://docs.circuitpython.org/en/latest/docs/environment.html) as `WIFI_PASSWORD`. Password for the AP (access point).
  - `create_pool()`: Creates a [`socketpool.SocketPool`](https://docs.circuitpython.org/en/latest/shared-bindings/socketpool/index.html#socketpool.SocketPool) class and stores it in `Wifi.pool`. Useful for creating web servers.
  - `setup_http()`: Creates an [`adafruit_requests.Session`](https://docs.circuitpython.org/projects/requests/en/latest/api.html#adafruit_requests.Session) class and stores it in `Wifi.requests`. Sets up necessary things to make http requests.
  - `fetch(url)`: Used to make http requests to a URL specified in `url`. Returns a [`Response`](https://docs.circuitpython.org/projects/requests/en/latest/api.html#adafruit_requests.Response) that can be used to parse JSON or extract text.
    - `url`: string that represents a http URL to request
  - ` mdns_setup(addr, p)`: Creates a mdns address to use on local network for servers.
    - `addr: "nanokid"`: address used for mdns, default is `nanokid` and it resolves to `nanokid.local` if you use it in your local network.
    - `p: 5000`: Port advertise the server on, default is `5000`.

## Setting up safe Wifi connections
1. Create a `settings.toml` in the root of your devices storage, if it doesn't exist yet. The root is the immediate storage you access after opening the drive on file explorer.
2. Open the `settings.toml` file in a text editor, like notepad or preferred text editor.
3. Put in the text that is bellow:
	```toml
	WIFI_SSID="<ssid>"
	WIFI_PASSWORD="<pass>"
	```
4. Replace the `<ssid>`, from the above text in the `settings.toml`, with the name of your Wifi network exactly including spaces and capital.
5. Replace the `<pass>`, from the above text in the `settings.toml`, with the password of the same Wifi network exactly.
6. Make sure to save the file. And when connecting to Wifi in your code just call the `connect()` function with no other parameters.
7. **Do not share your `settings.toml` anywhere online and do not paste your Wifi name and password directly in your code. This information is stored in a separate file so that you don't accidently share your information online.**

## Setting up multiple Wifi connections
1. Create a `settings.toml` in the root of your devices storage, if it doesn't exist yet. The root is the immediate storage you access after opening the drive on file explorer.
2. Open the `settings.toml` file in a text editor, like notepad or preferred text editor.
3. Put in the text that is bellow:
  ```toml
  WIFI_SSID0="<ssid>"
  WIFI_PASSWORD0="<pass>"
  WIFIs="1"
  ```
4. Each time you add a new network add `WIFI_SSID<n>` replacing `<n>` with the nth ssid, same for password: `WIFI_SSID<n>` replacing `<n>` with the nth password, make sure the ssid and password match the n. And after that make sue to set `WIFIS` to the number of total networks saved.
5. Replace the `<ssid>`, from the above text in the `settings.toml`, with the name of your Wifi network exactly including spaces and capital.
6. Replace the `<pass>`, from the above text in the `settings.toml`, with the password of the same Wifi network exactly.
7. Make sure to save the file. And when connecting to Wifi in your code just call the `connect()` function with no other parameters.
8. **Do not share your `settings.toml` anywhere online and do not paste your Wifi name and password directly in your code. This information is stored in a separate file so that you don't accidently share your information online.**
9. Example:
  ```toml
  WIFI_SSID0="home"
  WIFI_PASSWORD0="homepass"
  WIFI_SSID1="office"
  WIFI_PASSWORD1="employeeonly"
  WIFI_SSID2="free club wifi"
  WIFI_PASSWORD2=""
  WIFIs="3"
  ```