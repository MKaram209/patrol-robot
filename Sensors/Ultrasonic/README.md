# HC-SR04 Ultrasonic Sensor

## Quick reference
- Used for: obstacle avoidance (backup to lidar per build guide)
- Pins used in this project: see current wiring in `Code/` (not fixed yet, may change)
- Operating voltage: 3.3V - 5V (wired direct to Uno 5V, no divider needed)
- Measuring range: 2cm - 400cm, accuracy ~3mm
- Status: single-sensor test working, returns distance in cm over Serial.

## Wiring
VCC -> 5V, GND -> GND, Trig -> any free digital pin, Echo -> any free digital pin (check the sketch for current assignment).

## Known issues / notes
- A reading of -1 means no echo returned within the timeout — check wiring (Trig/Echo swapped is the usual culprit) before assuming it's out of range.
- Uno is 5V logic so no voltage divider needed on Echo; this would NOT be true on a Raspberry Pi (3.3V GPIO).

## Code
See `Code/` for the test sketch.

---

## Full datasheet (reference)

**HC-SR04 Ultrasonic Sensor Detector, 3.3V-5V**

Distance-measuring module using ultrasonic pulses: a transmitter/receiver pair times the round trip of a 40kHz pulse to calculate distance.

**Features**
- Works with both 3.3V and 5V logic
- Range: 2cm - 400cm (4m)
- Accuracy: ~±3mm
- Simple Trigger/Echo interface
- Low power, compact

**Specifications**

| Specification | Details |
|---|---|
| Operating Voltage | 3.3V - 5V |
| Operating Current | 15mA |
| Operating Frequency | 40kHz |
| Measuring Range | 2cm - 400cm |
| Accuracy | ±3mm |
| Trigger Input | 10µs TTL pulse |
| Echo Output | TTL pulse, proportional to distance |
| Measuring Angle | <15° |
| Dimensions | 45 x 20 x 15mm |

**Pinout**

| Pin | Name | Description |
|---|---|---|
| 1 | Vcc | Power, 3.3-5V |
| 2 | Trigger | Input — hold high 10µs to start a measurement |
| 3 | Echo | Output — stays high for a duration proportional to distance |
| 4 | Ground | GND |

**How it works**
Trigger pin sends a pulse, the module emits an ultrasonic burst, and Echo goes high for the time it takes the pulse to bounce back — that duration converts directly to distance.
