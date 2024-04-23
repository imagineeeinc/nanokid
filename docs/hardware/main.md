# NanoKid Hardware Guide
This document encloses some hardware information.

## Components
- **Computing Unit**
  - Raspberry Pi Pico W
    - Uses the **RP2040 mcu**
    - Built in Wifi And Bluetooth
    - MicroUSB Port
- **Display**
  - ST7789 LCD
    - 1.3 Inch
    - **240x240 Resolution**
    - Full Colour
- **Accelerometer & Gyroscope**
  - MPU6050
    - Accelerometer
    - Gyroscope
    - Temperature
    - Movement Interrupt

## I2C Addresses
- MPU:
  - Default
    - 1101000
    - 0x64
    - 104
  - ADO: 1
    - 1101001
    - 0x69
    - 105
