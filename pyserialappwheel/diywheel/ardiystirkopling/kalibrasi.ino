// Pin Joystick
const int joystickX = A1;  // Sumbu X joystick shifter
const int joystickY = A2;  // Sumbu Y joystick shifter

// Pin Potensiometer Steering
const int potSteering = A0;

// Tombol Lainnya
const int buttonLeftSignal = 2;
const int buttonRightSignal = 3;
const int buttonHorn = 4;
const int buttonHazard = 5;
const int buttonLights = 6;

// Variabel Steering
int steeringValue = 0;
float smoothedSteeringValue = 0.0;
const float smoothingFactor = 0.1;

// Variabel Tombol
bool leftSignalState = false;
bool rightSignalState = false;
bool hornState = false;
bool hazardState = false;
bool lightsState = false;

void setup() {
  Serial.begin(115200);

  // Setup tombol sebagai INPUT_PULLUP
  pinMode(buttonLeftSignal, INPUT_PULLUP);
  pinMode(buttonRightSignal, INPUT_PULLUP);
  pinMode(buttonHorn, INPUT_PULLUP);
  pinMode(buttonHazard, INPUT_PULLUP);
  pinMode(buttonLights, INPUT_PULLUP);
}

void loop() {
  // Baca steering dengan smoothing
  steeringValue = analogRead(potSteering);
  smoothedSteeringValue = smoothedSteeringValue + smoothingFactor * (steeringValue - smoothedSteeringValue);
  int mappedSteering = map(smoothedSteeringValue, 0, 1023, 0, 32767);

  // Baca tombol lainnya
  leftSignalState = (digitalRead(buttonLeftSignal) == LOW);
  rightSignalState = (digitalRead(buttonRightSignal) == LOW);
  hornState = (digitalRead(buttonHorn) == LOW);
  hazardState = (digitalRead(buttonHazard) == LOW);
  lightsState = (digitalRead(buttonLights) == LOW);

  // Baca nilai X dan Y joystick
  int xValue = analogRead(joystickX);
  int yValue = analogRead(joystickY);

  // Kirim data ke serial: steering, tombol, X, Y
  Serial.print(mappedSteering);
  Serial.print(",");
  Serial.print(leftSignalState ? 1 : 0);
  Serial.print(",");
  Serial.print(rightSignalState ? 1 : 0);
  Serial.print(",");
  Serial.print(hornState ? 1 : 0);
  Serial.print(",");
  Serial.print(hazardState ? 1 : 0);
  Serial.print(",");
  Serial.print(lightsState ? 1 : 0);
  Serial.print(",");
  Serial.print(xValue);
  Serial.print(",");
  Serial.println(yValue);

  delay(10);
}
