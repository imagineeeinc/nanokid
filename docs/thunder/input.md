# Input
The NanoKid comes with a small selection of user inputs on the front.

## Example
```python
import time
import thunder.input as controls

while True:
	if controls.get_btn(controls.btna):
		print("A button pressed")
	if controls.get_axis(controls.y_axis) >= 0.8:
		print("thumb stick is being pushed down")
	time.sleep(0.1)
```

## API Reference

- `thunder.input`
  - [`get_btn`](#def-get_btn)
  - [`get_axis`](#def-get_axis)
  - [`y_axis`](#y_axis)
  - [`x_axis`](#x_axis)
  - [`btna`](#btna)
  - [`btnb`](#btnb)
  - [`btnst`](#btnst)
  - [`btnse`](#btnse)

### `def get_btn`
```python
get_btn(button: DigitalInOut)
```
Gets the current state of the `button` (A [`DigitalInOut`](https://docs.circuitpython.org/en/latest/shared-bindings/digitalio/index.html#digitalio.DigitalInOut) pointing to the pin of the button.), and returns `True` or `False`. If pressed it returns `True` else `False`

### `def get_axis`
```python
get_axis(axis: AnalogIn)
```
Get the current state of the `axis` (A [`AnalogIn`](https://docs.circuitpython.org/en/latest/shared-bindings/analogio/index.html#analogio.AnalogIn) pointing to the pin of the axis of the thumb stick.), and returns float between the values of `-1` and `1`. Up or Left is negative and Down or Right is positive.
### Input Values
Corresponding to the pins the buttons are connected to, used to extract values.
#### `y_axis`
The Vertical axis of the thumb stick. Represents a [`AnalogIn`](https://docs.circuitpython.org/en/latest/shared-bindings/analogio/index.html#analogio.AnalogIn) for the corresponding pin.
#### `x_axis`
The Horizonal axis of the thumb stick. Represents a [`AnalogIn`](https://docs.circuitpython.org/en/latest/shared-bindings/analogio/index.html#analogio.AnalogIn) for the corresponding pin.
#### `btna`
The input of button `A`. Represents a [`DigitalInOut`](https://docs.circuitpython.org/en/latest/shared-bindings/digitalio/index.html#digitalio.DigitalInOut) for the corresponding pin.
#### `btnb`
The input of button `B`. Represents a [`DigitalInOut`](https://docs.circuitpython.org/en/latest/shared-bindings/digitalio/index.html#digitalio.DigitalInOut) for the corresponding pin.
#### `btnst`
The input of button `start` (`st` for short). Represents a [`DigitalInOut`](https://docs.circuitpython.org/en/latest/shared-bindings/digitalio/index.html#digitalio.DigitalInOut) for the corresponding pin.
#### `btnse`
The input of button `select` (`se` for short). Represents a [`DigitalInOut`](https://docs.circuitpython.org/en/latest/shared-bindings/digitalio/index.html#digitalio.DigitalInOut) for the corresponding pin.