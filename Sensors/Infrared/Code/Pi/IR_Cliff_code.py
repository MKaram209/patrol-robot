#!/usr/bin/env python3
"""4 IR cliff sensors on a Raspberry Pi (port of the Arduino sketch).

Sensor output: LOW = floor detected, HIGH = cliff (no floor).

Wiring (Pi GPIO is 3.3V ONLY):
  Each sensor:  VCC -> 3.3V (Pi pin 1 or 17)   <-- NOT 5V
                GND -> GND  (e.g. Pi pin 6)
                OUT -> GPIO pin below
  If a sensor is powered from 5V its OUT can reach 5V and damage the Pi.

  FL -> GPIO4  (pin 7)
  FR -> GPIO27 (pin 13)
  BL -> GPIO20 (pin 38)
  BR -> GPIO21 (pin 40)
  (chosen to avoid the LED/buzzer/PIR/ultrasonic/motor pins used elsewhere)

Run:  python3 ir_cliff.py     (Ctrl+C to stop)
"""

import time
from gpiozero import DigitalInputDevice

PIN_FL = 4    # front-left sensor OUT   (GPIO number, BCM)
PIN_FR = 27   # front-right sensor OUT
PIN_BL = 20   # back-left sensor OUT
PIN_BR = 21   # back-right sensor OUT

NAMES = ["FL", "FR", "BL", "BR"]
PINS = [PIN_FL, PIN_FR, PIN_BL, PIN_BR]
DEBOUNCE_S = 0.030     # ignore a change unless it holds this long (30 ms)
PRINT_STATUS = True
PRINT_EVERY_S = 0.2

GO_FORWARD, TURN_LEFT, TURN_RIGHT, BACK_UP, STOP_NOW = (
    "GO_FORWARD", "TURN_LEFT", "TURN_RIGHT", "BACK_UP", "STOP_NOW")

# Internal pull-up: an unplugged pin reads HIGH -> treated as cliff (safe failure).
# active_state=True means is_active == True when the pin is HIGH (= cliff).
sensors = [DigitalInputDevice(p, pull_up=True, active_state=True) for p in PINS]

now = time.monotonic()
last_raw = [s.is_active for s in sensors]
cliff = list(last_raw)
changed_at = [now] * len(sensors)


def read_sensors():
    t = time.monotonic()
    for i, s in enumerate(sensors):
        raw = s.is_active
        if raw != last_raw[i]:
            last_raw[i] = raw
            changed_at[i] = t
        elif raw != cliff[i] and t - changed_at[i] >= DEBOUNCE_S:
            cliff[i] = raw


def decide():
    fl, fr, bl, br = cliff
    if fl and fr:
        return STOP_NOW if (bl or br) else BACK_UP
    if fl:
        return TURN_RIGHT
    if fr:
        return TURN_LEFT
    return GO_FORWARD


# ====== ACTION BLOCK - fill this in once you know your motor driver ======
def do_action(action):
    if action == GO_FORWARD:
        pass  # both motors forward
    elif action == TURN_LEFT:
        pass  # left motor backward (or stopped), right motor forward
    elif action == TURN_RIGHT:
        pass  # left motor forward, right motor backward (or stopped)
    elif action == BACK_UP:
        pass  # both motors backward
    elif action == STOP_NOW:
        pass  # both motors off


print("IR cliff sensors started")
last_print = 0.0
try:
    while True:
        read_sensors()
        action = decide()
        do_action(action)

        t = time.monotonic()
        if PRINT_STATUS and t - last_print >= PRINT_EVERY_S:
            last_print = t
            status = " ".join(
                f"{n}:{'CLIFF' if c else 'ok   '}" for n, c in zip(NAMES, cliff))
            print(f"{status} -> {action}")
        time.sleep(0.005)   # don't hog the CPU
except KeyboardInterrupt:
    print("\nStopped")
