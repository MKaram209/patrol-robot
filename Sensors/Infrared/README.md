# IR Obstacle / Cliff Sensor

## Quick reference
- Used for: cliff detection, mounted at the robot's corners (FL / FR / BL / BR)
- Pins used in this project: see current wiring in `Code/` (not fixed yet, may change)
- Output: digital, LOW = obstacle/edge detected, HIGH = clear
- Operating voltage: 3.3V - 5V (powered from Uno 5V)
- Detection range: 2-30cm, adjustable via onboard potentiometer
- Status: tested individually, working. Full multi-sensor integration pending.

## Wiring
VCC -> 5V rail, GND -> GND rail, OUT -> any free digital pin (check the sketch for the pin currently assigned to each sensor).

## Known issues / notes
- Unwired pins read as a false "cliff" due to INPUT_PULLUP — only trust readings from pins actually connected.
- Potentiometer needs adjusting per-sensor if detection distance looks off.

## Code
See `Code/` for the test sketch.

---

## Full datasheet (reference)

**Infrared IR Obstacle Avoidance Sensor Board, 3 Pin**

Infrared transmitter/receiver pair. Emits IR at a set frequency; when reflected by an obstacle, the sensor's LED lights up and OUT goes low.

**Features**
- Adjustable sensitivity via potentiometer
- Compact, lightweight, 3-pin interface
- Digital (DO) and analog (AO) output variants exist
- Low power, fast response (<2ms)
- Compatible with Arduino, Raspberry Pi, PIC, AVR, STM32

**Specifications**

| Specification | Details |
|---|---|
| Operating Voltage | 3.3V - 5V DC |
| Current Consumption | 20mA |
| Detection Range | 2cm - 30cm, adjustable |
| Detection Angle | 35° |
| Output Type | Digital: High = no obstacle, Low = obstacle |
| IR Wavelength | 850-950nm |
| Response Time | <2ms |
| Pin Pitch | 2.54mm |
| Dimensions | 32 x 14mm |

**Pin configuration**
- VCC: power (3.3-5V)
- GND: ground
- OUT: digital output
- Power LED: on when powered
- Obstacle LED: on when obstacle detected
- Distance Adjust: CCW = shorter range, CW = longer range

**Applications**
Robotics/automation, smart vehicles, security/surveillance, industrial, consumer electronics, assistive devices.
