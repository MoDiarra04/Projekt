import serial
import time

def befehl_an_arduino(befehl):

    # Dieser Bewässerungsbefehl soll zur korrekten Zeit an den Arduino
    # geschickt werden und enthält die nötigen Informationen im folgenden Format:
    # <Smartmodus binär> <Modulnummer> <Wässerungsgszeit in Minuten>
    # Beispiel: '0 10 0'
    
    watering_command = 'b' + befehl # b to encode to bytes

    # ard_serial: Schnittstelle zum Arduino
    ard_serial = serial.Serial('/dev/ttyACM0',9600,timeout=1)

    # Wait for the serial connection to initialize
    time.sleep(2) 

    while True:
        # Send string to arduino
        ard_serial.write(watering_command)
        
        # Wait for and read response
        if ard_serial.in_waiting > 0:
            
            # received_string = ard_serial.readline().decode('utf-8').rstrip()
            # print(f'Received: {received_string}')
            break
        
        # For stability
        time.sleep(1) 
        
