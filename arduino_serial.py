import time
import serial

# Globale Variable für die serielle Verbindung
ard_serial = None

def initialize_serial_connection(port='COM6', baudrate=9600, timeout=1):
    global ard_serial
    if ard_serial is None:
        ard_serial = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)  # Warten, bis die serielle Verbindung initialisiert ist
    return ard_serial

def befehl_an_arduino(smart: bool, modulnummer: int, dauer: int):
    global ard_serial
    # Dieser Bewässerungsbefehl soll zur korrekten Zeit an den Arduino
    # geschickt werden und enthält die nötigen Informationen im folgenden Format:
    # <Smartmodus binär> <Modulnummer> <Wässerungsgszeit in Minuten>
    # Beispiel: '0 0 01'
    
    if dauer < 10:
        dauer = '0' + str(dauer)
    
    # Bewässerungsbefehl zu einem string zusammenfassen
    watering_command = f"{int(smart)} {modulnummer} {dauer}"
    
    # Serielle Verbindung initialisieren, wenn sie noch nicht besteht
    ard_serial = initialize_serial_connection()
    
    # Debugging-Ausgabe
    print(f"Sende Befehl an Arduino: {watering_command}")
    
    # Write to serial
    ard_serial.write(watering_command.encode())
    
def stop_befehl_an_arduino():
    global ard_serial
    # Serielle Verbindung initialisieren, wenn sie noch nicht besteht
    ard_serial = initialize_serial_connection()
    
    command = "STOP"
    
    # Debugging-Ausgabe
    print("Sende STOP-Befehl an Arduino")
    
    # Write to serial
    ard_serial.write(command.encode())

# Beispiel für das Schließen der seriellen Verbindung beim Beenden des Programms
def close_serial_connection():
    global ard_serial
    if ard_serial is not None:
        ard_serial.close()
        ard_serial = None
        print("Serielle Verbindung geschlossen")