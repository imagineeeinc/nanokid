# Cyclone Shell
An OS shell like program that lets you load and switch programs on the fly without needing another device and do other small tasks.

## Installation
1. Copy the `code.py` into the root of the device.
2. Create a `cyclone` folder in the root of the device.
3. Copy the `cyclone.json` into the `cyclone/` folder.
4. Just add your code to the `cyclone/` folder.

## Configuration
The `cyclone.json` file holds information for the cyclone shell at runtime to be used. You will need to configure it in JSON.

### Options
- `"autoboot"`: A string that defines a program from the `cyclone` folder to auto boot into on start-up. When set to `"0"` it won't boot into any program and load into the shell. Auto boot can be cancelled by holding `b` on start-up.

## Making Programs
Making programs is no different to programming normal programs for the NanoKid (Thunder).