import serial
import time

def befehl_an_arduino(smart: bool, modulnummer: int, dauer: int):

    # Dieser Bewässerungsbefehl soll zur korrekten Zeit an den Arduino
    # geschickt werden und enthält die nötigen Informationen im folgenden Format:
    # <Smartmodus binär> <Modulnummer> <Wässerungsgszeit in Minuten>
    # Beispiel: '0 0 01'
    
    if dauer < 10:
        dauer = '0' + str(dauer)
    
    # Bewässerungsbefehl zu einem string zusammenfassen
    watering_command = str(smart) + ' ' + str(modulnummer) + ' ' + str(dauer)
    
    # ard_serial ist Schnittstelle zum Arduino
    # ard_serial = serial.Serial('/dev/ttyACM0', 9600,timeout=1) # connection from RPI
    ard_serial = serial.Serial('COM6', 9600, timeout=1) # connection from Windows
    # Um 'COMX' herauszufinden: Im Geräte Manager-> "Ports" oder "Anschlüsse" -> Arduino
    # Wenn das nicht klappt: in der Arduino IDE-> oben rechts: Serial Monitor -> Anschluss steht im Eingabefeld

    # Wait for the serial connection to initialize
    time.sleep(2) 
    
    # Write to serial
    ard_serial.write(watering_command.encode())
    print("reached")