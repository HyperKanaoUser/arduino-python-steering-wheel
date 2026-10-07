// Pin Joystick
const int joystickX = A1;  // Sumbu X joystick shifter
const int joystickY = A2;  // Sumbu Y joystick shifter

// Pin Potensiometer Steering
const int potSteering = A0;

// Tombol Lainnya
const int buttonLeftSignal = 2;
const int buttonRightSignal = 3;
const int buttonHorn = 4;
const int buttonBrake = 9;
const int buttonGas = 10;
const int buttonGearMode = 8; // Tombol untuk mengganti mode gigi (High/Low)

void setup() {
  Serial.begin(115200);

  // Setup tombol sebagai INPUT_PULLUP
  pinMode(buttonLeftSignal, INPUT_PULLUP);
  pinMode(buttonRightSignal, INPUT_PULLUP);
  pinMode(buttonHorn, INPUT_PULLUP);
  pinMode(buttonBrake, INPUT_PULLUP);
  pinMode(buttonGas, INPUT_PULLUP);
  pinMode(buttonGearMode, INPUT_PULLUP);
}

void loop() {
  // Baca steering
  int steeringValue = analogRead(potSteering);
  int mappedSteering = map(steeringValue, 0, 1023, 0, 32767);

  // Baca tombol lainnya
  bool leftSignalState = (digitalRead(buttonLeftSignal) == LOW);
  bool rightSignalState = (digitalRead(buttonRightSignal) == LOW);
  bool hornState = (digitalRead(buttonHorn) == LOW);
  bool hazardState = (digitalRead(buttonBrake) == LOW);
  bool lightsState = (digitalRead(buttonGas) == LOW);
  bool gearModeState = (digitalRead(buttonGearMode) == LOW);

  // Baca nilai X dan Y joystick
  int xValue = analogRead(joystickX);
  int yValue = analogRead(joystickY);

  // Kirim data ke serial: steering, tombol, X, Y, mode gigi
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
  Serial.print(yValue);
  Serial.print(",");
  Serial.println(gearModeState ? 1 : 0); // Kirim status tombol mode gigi

  delay(10);
}
