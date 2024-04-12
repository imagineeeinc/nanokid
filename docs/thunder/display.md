# Display
Powering the NanoKid Display is the ST7789 Display. It's a square 1.3 inch (diagonal) at 240x240 resolution.

## Example
```python
import time
from thunder.display import Display
import terminalio
from adafruit_display_text import label

disp = Display()
screen = disp.screen

text = label.Label(terminalio.FONT, text="Hello, World!",
color=0xc7dcd0, background_color=0x000000, x=100, y=100, scale=4)
screen.append(text)

while True:
  # Turns the backlight off after 5 seconds
  time.sleep(5)
  disp.backlight_off()
  # Turns the backlight on after 2 seconds
  time.sleep(2)
  disp.backlight_on()
```
## API Reference

- `thunder.display`
  - [`Display`](#class-display)

### `class Display`
The main object used to abstract the creation and usage of the display.
```python
class Display(mosi=board.GP19, clk=board.GP18, cs=board.GP17, dc=board.GP16, scale=1)
```
- Parameter
  - `mosi: board.GP19`: mosi line for the display, used if its on another pin.
  - `clk: board.GP18`: clk line for the display, used if its on another pin.
  - `cs: board.GP17`: cs line for the display, used if its on another pin.
  - `dc: board.GP16`: dc line for the display, used if its on another pin.
  - `scale: 1`: the scale of the root display group; leave as is if you don't know what to do.
- Properties
  - `power`: creates a [`DigitalInOut`](https://docs.circuitpython.org/en/latest/shared-bindings/digitalio/index.html#digitalio.DigitalInOut) from the [`digitalio`](https://docs.circuitpython.org/en/latest/shared-bindings/digitalio/index.html#module-digitalio). Is used to programmatically turn on the display when the display is inited to save battery power. When `power.value` is `True` the display is on, and vice versa.
  - `backlight`: creates a [`DigitalInOut`](https://docs.circuitpython.org/en/latest/shared-bindings/digitalio/index.html#digitalio.DigitalInOut) from the [`digitalio`](https://docs.circuitpython.org/en/latest/shared-bindings/digitalio/index.html#module-digitalio). Used to turn of the backlight when you want to be in standby but don't want to waste power to keep the backlight on. When `backlight.value` is `False` the backlight is off, and vice versa.
  - `scale`: stores the current screen's scale.
  - `display`: create a display driver from [`adafruit_ST7789`](https://docs.circuitpython.org/projects/st7789/en/latest/api.html#adafruit-st7789).
  - `screen`: creates a group to add screen elements to. Creates [`displayio.Group`](https://docs.circuitpython.org/en/latest/shared-bindings/displayio/#displayio.Group).
- Functions
  - `backlight_on()`: turns the backlight on.
  - `backlight_off()`: turns backlight off.

## Adding elements to screen
Thunder uses the built in [`displayio`](https://docs.circuitpython.org/en/latest/shared-bindings/displayio/#module-displayio) for a default and simple way of drawing to the display.

### Shapes
To add shapes, use the [`adafruit_display_shapes`](https://docs.circuitpython.org/projects/display-shapes/en/latest/api.html) library. Simply create the the shape using the constructors, then simply append it to the screen property.

**Example**
```python
from thunder.display import Display
from adafruit_display_shapes.triangle import Triangle

disp = Display()
tri = Triangle(0, 0, 10, 5, 0, 10, fill=0xc7dcd0, outline=0xFFFFFF)
disp.screen.append(tri)

while True:
  pass
```

### Text
To add text, use the [`adafruit_display_text`](https://docs.circuitpython.org/projects/display_text/en/latest/api.html#adafruit-display-text) library. Also you need a font you can use the [built in font](https://docs.circuitpython.org/en/latest/shared-bindings/terminalio/index.html#terminalio.FONT) in the the [`terminalio`](https://docs.circuitpython.org/en/latest/shared-bindings/terminalio/index.html#module-terminalio) library.
Simply create the the label using the constructors, then simply append it to the screen property.
```python
from thunder.display import Display
import terminalio
from adafruit_display_text import label

disp = Display()
text = label.Label(terminalio.FONT, text="Hello, World!",
color=0xffffff, x=100, y=100, scale=4)
disp.screen.append(text)

while True:
  pass
```
