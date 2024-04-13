# Cyclone Shell
An OS shell like program that lets you load and switch programs on the fly without needing another device and do other small tasks.

## Installation
1. Copy the `code.py` into the root of the device.
2. Create a `cyclone` folder in the root of the device.
3. Copy the `cyclone.json` into the `cyclone/` folder

## Configuration
The `cyclone.json` file holds information for the cyclone shell at runtime to be used. You will need to configure it in JSON.

### Options
- `"autoboot"`: A string that defines a program from the `cyclone` folder to auto boot into on startup. When set to `"0"` it won't boot into any program and load into the shell. Auto boot can be canceled by holding `b` on startup.

## Making Programs
When making programs to be compatible with the cyclone shell, there needs to be some defaults in your program to be used.

### Variables
- `display`: A variable that holds the `thunder.Dispaly` class (Reference thunder docs for more on display usage).
- `controls`: A variable that holds the `thunder.controls` module to be used at runtime (Reference thunder docs for more on controls).
- `led`: A variable that holds the `DigitalInOut(board.LED)`. This can be used to access rpi pico's built in led and relay information to the user. `led.value = True` turns on the led and vice versa.

### Functions
A `main()` function is required as the entrance to the program.

### Template
```python
# Import modules here

# Handed over Variables
display = None
controls = None
led = None

# Entrance function
def main():
  # Replace the pass bellow with your initialization code.
  pass
```
