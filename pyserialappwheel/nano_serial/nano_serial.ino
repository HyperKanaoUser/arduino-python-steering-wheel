// Pin Potensiometer dan Tombol
const int potSteering = A0;       // Potensiometer untuk steering wheel
const int buttonLeftSignal = 2;   // Tombol lampu sein kiri
const int buttonRightSignal = 3;  // Tombol lampu sein kanan
const int buttonHorn = 4;         // Tombol klakson
const int buttonHazard = 9;       // Tombol hazard
const int buttonLights = 10;       // Tombol lampu
const int buttonShiftUp = 7;      // Tombol shifter up
const int buttonShiftDown = 8;    // Tombol shifter down

// Variabel
int steeringValue = 0;
float smoothedSteeringValue = 0.0;
const float smoothingFactor = 0.75; // Faktor smoothing untuk stabilisasi potensiometer

bool leftSignalState = false;
bool rightSignalState = false;
bool hornState = false;
bool hazardState = false;
bool lightsState = false;
bool shiftUpState = false;
bool shiftDownState = false;

void setup() {
  Serial.begin(115200);

  // Mengaktifkan internal pull-up resistor pada tombol
  pinMode(buttonLeftSignal, INPUT_PULLUP);
  pinMode(buttonRightSignal, INPUT_PULLUP);
  pinMode(buttonHorn, INPUT_PULLUP);
  pinMode(buttonHazard, INPUT_PULLUP);
  pinMode(buttonLights, INPUT_PULLUP);
  pinMode(buttonShiftUp, INPUT_PULLUP);
  pinMode(buttonShiftDown, INPUT_PULLUP);
}

void loop() {
  // Membaca nilai potensiometer dan menerapkan Low-Pass Filter
  steeringValue = analogRead(potSteering);
  smoothedSteeringValue = smoothedSteeringValue + smoothingFactor * (steeringValue - smoothedSteeringValue);
  int mappedSteering = map(smoothedSteeringValue, 0, 1023, 0, 32767);

  // Membaca tombol (LOW artinya ditekan, karena menggunakan pull-up)
  leftSignalState = (digitalRead(buttonLeftSignal) == LOW);
  rightSignalState = (digitalRead(buttonRightSignal) == LOW);
  hornState = (digitalRead(buttonHorn) == LOW);
  hazardState = (digitalRead(buttonHazard) == LOW);
  lightsState = (digitalRead(buttonLights) == LOW);
  shiftUpState = (digitalRead(buttonShiftUp) == LOW);
  shiftDownState = (digitalRead(buttonShiftDown) == LOW);

  // Mengirimkan data sebagai CSV (format: steering,left_signal,right_signal,horn,hazard,lights,shift_up,shift_down)
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
  Serial.print(shiftUpState ? 1 : 0);
  Serial.print(",");
  Serial.println(shiftDownState ? 1 : 0);

  delay(10); // Mengurangi latency
}
