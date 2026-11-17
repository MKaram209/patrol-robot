# IR Obstacle / Cliff Sensor

## Quick reference
- Used for: cliff detection, mounted at the robot's corners (FL / FR / BL / BR), Module 3
- Bought from: [Makers Electronics](https://makerselectronics.com/product/infrared-ir-sensor-board/) - https://makerselectronics.com/product/infrared-ir-sensor-board/
- Quantity needed: 4 (the build guide's buy list says 3, so one more is needed)
- Output: digital. **Pointing down at the floor: LOW = floor, HIGH = cliff (no floor).**
  The board itself reports LOW = something reflected the IR, HIGH = nothing in range.
- Operating voltage: 3.3V - 5V
- Detection range: 2-30cm, adjustable via onboard potentiometer
- Status: tested individually on Arduino, working. Multi-sensor sketch written; Pi version written, not tested yet.

## Wiring

### Arduino Uno
| Sensor | OUT -> Uno pin |
|---|---|
| FL (front-left) | D2 |
| FR (front-right) | D3 |
| BL (back-left) | D4 |
| BR (back-right) | D5 |

All sensors: VCC -> 5V, GND -> GND.

### Raspberry Pi (not tested yet)
| Sensor | OUT -> Pi GPIO | Physical pin |
|---|---|---|
| FL | GPIO4 | 7 |
| FR | GPIO27 | 13 |
| BL | GPIO20 | 38 |
| BR | GPIO21 | 40 |

All sensors: VCC -> **3.3V** (pin 1 or 17), GND -> GND (pin 6, 9 or 14).
Do not power them from 5V on the Pi: the OUT pin follows the supply voltage, and Pi GPIO is 3.3V only.

## Test: works when
- Held 1-3 cm above the floor, the sensor reads floor (obstacle LED on, `ok` in the output).
- Lifted off the floor or held over a table edge, it reads CLIFF (obstacle LED off).
- All four sensors do this independently.

## Measured results
_Fill in from your tests:_
- Mounting height above floor: ___
- Potentiometer setting that works: ___
- Floors tested (tile, wood, carpet): ___
- Surfaces that gave a false cliff (black, shiny): ___

## Known issues / notes
- Unwired pins read as a false "cliff" because of INPUT_PULLUP. This is intentional (an unplugged sensor fails safe), so only trust readings from pins that are actually connected.
- The potentiometer needs adjusting per sensor if the detection distance looks off. Turn it clockwise for longer range, counterclockwise for shorter.
- IR sensors can misread very dark or black surfaces (they absorb IR) and strong sunlight. Test on the surface the robot will actually patrol.
- The sketch debounces each reading for 30 ms to avoid flicker at an edge.

## Code
- `Code/arduino/` : 4-sensor cliff sketch with debounce and an empty motor action block
- `Code/pi/` : Python version using `gpiozero` (same logic, same output)

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
