void setup() {
  Serial.begin(9600); // Start serial communication at 9600 baud
}

void loop() {
  
  // Kommunikation mit RPI; String einlesen
  if (Serial.available()) {
    string data = Serial.readStringUntil('\n'); // Read the incoming data
  }

  // Messwert einlesen?
  int messwert = 17; // Dummy Messwert

  // Daten zurückschicken?
  Serial.println(messwert);

  // Delay for stability
  delay(100);

  // Wenn Befehl erhalten wurde; befehl ausführen; data zurücksetzen
  if(!data.empty()){
    // TODO: Pumpe ansteuern
    data = "";
  }
}
