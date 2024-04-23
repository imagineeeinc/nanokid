# Led
The NanoKid has a built in led on the Raspberry pi Pico.

## Example
```python
import time
from thunder.led import led

while True:
	# Flips light on and of every half a second
	led.value = not led.value
	time.sleep(0.5)
```

## API Reference

- `thunder.led`
  - [`led`](#led)

### `led`
Represents a [`DigitalInOut`](https://docs.circuitpython.org/en/latest/shared-bindings/digitalio/index.html#digitalio.DigitalInOut) pointing to the led on the board. Simply use `led.value` to turn it on and off ([`value` docs](https://docs.circuitpython.org/en/latest/shared-bindings/digitalio/index.html#digitalio.DigitalInOut.value)). `True` turns it on and vice versa.