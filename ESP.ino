void setup() {
  Serial.begin(9600);
}

void loop() {
  int speed = random(0,100); // voorbeeldwaarde
  int rpm = random(0,100); // voorbeeldwaarde

  // Stuur JSON-achtige string
  Serial.print("{\"speed\":");
  Serial.print(speed);
  Serial.print(",\"rpm\":");
  Serial.print(rpm);
  Serial.println("}");

  delay(1000);
}
