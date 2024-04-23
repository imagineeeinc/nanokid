# Thunder Library
The main library to interface with the NanoKid's hardware.

The main library is installed in the `lib` directory and is accessed in your CircuitPython code.

All of the submodules can be accessed under the name `thunder` (e.g.: `from thunder.display import ...`).

## API Reference
- `thunder`
  - audio
  - [`display`](./display)
  - [`input`](./input)
  - IR
  - [`led`](./led)
  - light sensor
  - microphone
  - [`mount_sd`](./mount_sd)
  - [`mpu6050`](./mpu6050)
  - utils
  - [`wifi`](./wifi)

## Installation
### Manual
Simply copy the `thunder/` folder from the root of the project to the `lib/` folder on the NanoKid's storage. And you are ready to access all of the thunder API with the `thunder` prefix.