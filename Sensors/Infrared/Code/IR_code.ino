// Simple test for 1 HC-SR04 ultrasonic sensor
// Wiring: VCC -> 5V, GND -> GND (direct, no divider needed on Uno)

const int TRIG = 6;
const int ECHO = 7;

void setup() {
  Serial.begin(9600);
  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);
}

float readDistanceCM() {
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG, LOW);

  long duration = pulseIn(ECHO, HIGH, 30000);   // 30ms timeout ~ 5m max range
  if (duration == 0) return -1;                 // no echo received
  return duration * 0.0343 / 2;                 // speed of sound -> cm
}

void loop() {
  float d = readDistanceCM();
  Serial.print("Distance: ");
  Serial.print(d);
  Serial.println(" cm");
  delay(200);
}