#!/usr/bin/env python3
"""Simple test for 1 HC-SR04 ultrasonic sensor on a Raspberry Pi.
Equivalent of the Arduino sketch (prints distance in cm every 200 ms).

Wiring (Pi GPIO is 3.3V ONLY):
  VCC  -> 5V (Pi pin 2)
  GND  -> GND
  TRIG -> GPIO23 (Pi pin 16)   (3.3V output is enough to trigger it)
  ECHO -> GPIO24 (Pi pin 18)   THROUGH A VOLTAGE DIVIDER:
          ECHO -> 1 kOhm -> GPIO24 -> 2 kOhm -> GND
  The echo pin outputs 5V; connecting it directly can damage the Pi.

Setup:  sudo apt install python3-gpiozero   (usually preinstalled)
Run:    python3 ultrasonic_test.py          (Ctrl+C to stop)
"""

from time import sleep
from gpiozero import DistanceSensor

TRIG = 23           # GPIO number (BCM), not the physical pin number
ECHO = 24
MAX_DISTANCE_M = 4  # HC-SR04 reliable range is about 4 m

# threshold_distance / max_distance are in metres
sensor = DistanceSensor(echo=ECHO, trigger=TRIG, max_distance=MAX_DISTANCE_M)


def read_distance_cm():
    """Return distance in cm, or -1 if nothing is detected in range."""
    d = sensor.distance * 100  # metres -> cm
    if d >= MAX_DISTANCE_M * 100:
        return -1              # no echo / out of range (same as Arduino)
    return d


try:
    while True:
        d = read_distance_cm()
        if d < 0:
            print("Distance: no echo")
        else:
            print(f"Distance: {d:.1f} cm")
        sleep(0.2)
except KeyboardInterrupt:
    print("\nStopped")
