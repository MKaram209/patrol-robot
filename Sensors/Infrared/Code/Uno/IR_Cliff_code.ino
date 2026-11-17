// ====== 4 IR cliff sensors — pin template ======
// Wiring: each sensor's OUT pin goes to one of these. VCC -> 5V, GND -> GND.
// Sensor output: 0 = floor detected, 1 = cliff (no floor).

const int PIN_FL = 2;   // front-left sensor's OUT wire goes here
const int PIN_FR = 3;   // front-right sensor's OUT wire goes here
const int PIN_BL = 4;   // back-left sensor's OUT wire goes here
const int PIN_BR = 5;   // back-right sensor's OUT wire goes here

const int NUM = 4;
const int PINS[NUM]       = {PIN_FL, PIN_FR, PIN_BL, PIN_BR};
const char* NAMES[NUM]    = {"FL",   "FR",   "BL",   "BR"};
const unsigned long DEBOUNCE_MS = 30;   // ignore a change unless it holds for this long
const bool PRINT_STATUS = true;

bool cliff[NUM];
bool lastRaw[NUM];
unsigned long changedAt[NUM];

enum Action { GO_FORWARD, TURN_LEFT, TURN_RIGHT, BACK_UP, STOP_NOW };
const char* ACTION_NAMES[] = {"GO_FORWARD", "TURN_LEFT", "TURN_RIGHT", "BACK_UP", "STOP_NOW"};

void setup() {
  Serial.begin(9600);
  Serial.println("IR cliff sensors started");
  for (int i = 0; i < NUM; i++) {
    pinMode(PINS[i], INPUT_PULLUP);   // unplugged pin reads HIGH -> treated as cliff (safe failure)
    lastRaw[i] = digitalRead(PINS[i]) == HIGH;
    cliff[i] = lastRaw[i];
    changedAt[i] = millis();
  }
}

void readSensors() {
  for (int i = 0; i < NUM; i++) {
    bool raw = digitalRead(PINS[i]) == HIGH;
    if (raw != lastRaw[i]) {
      lastRaw[i] = raw;
      changedAt[i] = millis();
    } else if (raw != cliff[i] && millis() - changedAt[i] >= DEBOUNCE_MS) {
      cliff[i] = raw;
    }
  }
}

Action decide() {
  bool fl = cliff[0], fr = cliff[1], bl = cliff[2], br = cliff[3];
  if (fl && fr) return (bl || br) ? STOP_NOW : BACK_UP;
  if (fl) return TURN_RIGHT;
  if (fr) return TURN_LEFT;
  return GO_FORWARD;
}

// ====== ACTION BLOCK — fill this in once you know your motor driver ======
void doAction(Action a) {
  switch (a) {
    case GO_FORWARD:
      // both motors forward
      break;
    case TURN_LEFT:
      // left motor backward (or stopped), right motor forward
      break;
    case TURN_RIGHT:
      // left motor forward, right motor backward (or stopped)
      break;
    case BACK_UP:
      // both motors backward
      break;
    case STOP_NOW:
      // both motors off
      break;
  }
}

void loop() {
  readSensors();
  Action action = decide();
  doAction(action);

  static unsigned long lastPrint = 0;
  if (PRINT_STATUS && millis() - lastPrint >= 200) {
    lastPrint = millis();
    for (int i = 0; i < NUM; i++) {
      Serial.print(NAMES[i]);
      Serial.print(cliff[i] ? ":CLIFF " : ":ok    ");
    }
    Serial.print("-> ");
    Serial.println(ACTION_NAMES[action]);
  }
}