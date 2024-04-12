# Mount_SD
The NanoKid is fitted with a microSD Card reader to store larger files that won't fit on the RaspberryPi Pico's flash.

## SD Card Limitations
The microSD Card **MUST be under 32GB** in capacity. And should be formatted to `Fat32` or `Fat16`.
### Formatting
> **It is strongly recommend you use the official SD card formatter utility - written by the SD association it solves many problems that come with bad formatting!**
> 
> **Download the formatter from [www.sdcard.org/downloads/formatter/](https://www.sdcard.org/downloads/formatter/)**

## Example
1. Connect the microSD card to your device and make sure it is properly formatted according to the [formatting guidelines](#formatting)
2. Load a file onto the microSD card using your device; in this example it's a file called `hello.txt`.
3. Take the microSD card out of your device and plug it into the back of the NanoKid, **make sure it is powered off or no code is running**.
```python
from thunder.mount_sd import init_sdcard
import io

init_sdcard()

# Anything stored on the sdcard is accsesible under the '/sd' path.

print(io.open("/sd/hello.txt", mode="r").read())
```

## API Reference

- `thunder.mount_sd`
  - [`init_sdcard`](#def-init_sdcard)
  - [`mount`](#mount)
  - [`sdcard`](#sdcard)
  - [`vfs`](#vfs)

### `def init_sdcard`
Initialises the microSD card and mounts it to the [mount location](#mount) (default is `/sd`).

### `mount`
`Default: '/sd'`

A string variable which represents the path the microSD card should mount to. It should be changed before calling [`init_sdcard()`](#def-init_sdcard). If set to `'/'` it will be reverted back to the default when initialising the microSD card.

### `sdcard`
Represents the [`sdcardio.SDCard`](https://docs.circuitpython.org/en/latest/shared-bindings/sdcardio/index.html#sdcardio.SDCard) class in the CircuitPython sdcardio module.

Used to access information on the microSD card and deinit it after use.

### `vfs`
*Used internally*

Represents the [`VfsFat`](https://docs.circuitpython.org/en/latest/shared-bindings/storage/index.html#storage.VfsFat) class in the CircuitPython storage module.