void setup() {
  Serial.begin(9600); // Start serial communication at 9600 baud
  pinMode(A0, INPUT);
  pinMode(9, OUTPUT);
}

void loop() {
  // Delay for stability
  delay(100);
  
  // (Eingelesene) Daten zurücksetzen
  String data = ""; // String mit großem S und kein include string, weil das eine Arduino-Standard-library ist.

  // Kommunikation mit RPI; String einlesen; Serial ist Arduino Standard-library
  if (Serial.available()) {
    data = Serial.readStringUntil('\n');
    // Die Daten sollen folgendes Format haben:
    // <Smartmodus binär> <Modulnummer> <Wässerungsgszeit in Minuten(ggf. mit führender Null)>
    // Beispiel: '0 0 01'
  }
  else {
    return; // loop neustarten, um auf input zu warten
  }

  // Auf Serial Monitor ausgeben zum Überprüfen
  Serial.println(data);

  // Data auslesen, type casting ist komisch auf dem arduino
  bool smart = data[0] == '1';  // Convert char to boolean
  int modulnummer = data[2] - '0';  // Convert char to int; wegen ASCII Codierung minus char 0
  modulnummer = 0; // Es gibt vorerst nur ein modul
  int minuten = (data[4] - '0') * 10 + (data[5] - '0');  // Convert chars to int

  // Check smart modus und messwert
  if (smart){
    int grenzwert = 100; // Dummy Grenzwert
    int messwert = analogRead(A0);
    if ( messwert > grenzwert){
      return; // Startet die main-loop erneut
    }
  }

  // Motor ansteuern für x minuten
  digitalWrite(9, HIGH);
  delay(1000*60*minuten); // 1000ms * 60 * minuten = minuten, für die gewässert werden soll
  digitalWrite(9, LOW);
}