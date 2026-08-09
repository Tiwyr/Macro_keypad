from serial.tools import list_ports

def find_keypad_port():
    for port in list_ports.comports():
        print(
            "Device:",
            port.device,
            "\nDescription:",
            port.description,
            "\nVID:",
            port.vid,
            "\nPID:",
            port.pid,
            "\nSerial Number:",
            port.serial_number,
        )


    
if __name__ == "__main__":
    find_keypad_port()
