void setup() {
  Serial.begin(9600); // Start serial communication at 9600 baud
  pinMode(A0, INPUT);
  pinMode(9, OUTPUT);
}

void loop() {
  // Delay for stability
  delay(100);
  
  // Eingelesene Daten zurücksetzen
  string data = "";
  
  // Kommunikation mit RPI; String einlesen
  if (Serial.available()) {
    data = Serial.readStringUntil('\n'); // Read the incoming data
  }
  else {
    return;
  }

  // Data auslesen
  int modulnummer = int(data[0]);
  int modulnummer = 0; // Es gibt vorerst nur ein modul
  int minuten = int(data[2]) * 10 + int(data[3]);
  bool smart = bool(data[5]);

  // Minuten bounds check
  if (minuten > 20 || minuten < 1){
    return; // Startet die main-loop erneut
  }

  // Check smart modus und messwert
  int grenzwert = 100; // Dummy Grenzwert
  if (smart){
    int messwert = analogRead(A0);
    if ( messwert > grenzwert){
      return; // Startet die main-loop erneut
    }
  }
  
  // Befehl ausführen
  if(!data.empty()){
    // Motor ansteuern für x minuten
    digitalWrite(9, HIGH);
    delay(1000*60*minuten); // 1000ms * 60 * minuten = minuten, für die gewässert werden soll
    digitalWrite(9, LOW);
    data = "";
  }
}
