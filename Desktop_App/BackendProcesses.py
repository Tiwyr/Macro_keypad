from PySide6 import QtCore
import pyserial as serial
from serial.tools import list_ports
import time


KEYPAD_VID = 0x239A
KEYPAD_PID = 0x8106
KEYPAD_SERIAL_NUMBER = "DF648C8653620E32"


def find_keypad_port():
    for port in list_ports.comports():
        if (
            port.vid == KEYPAD_VID
            and port.pid == KEYPAD_PID
            and port.serial_number == KEYPAD_SERIAL_NUMBER
        ):
            return port.device

    return None

class BackgroundProcess(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.connection = False
        self.ping_timeStamp = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.connect_task)
        self.timer.start(500)  # Run every 500 milliseconds
        self.serial_port = serial.Serial("COM3", timeout=None)

    @QtCore.Slot()
    def connect_task(self):
        port = find_keypad_port()
        if self.connection == False:
            if port:
                print(f"Keypad found on port: {port}")
                self.serial_port.port = port
                self.serial_port.open()
                if self.handshake():
                    self.connection = True
                    self.timer.stop()
                    return port
            else:
                pass  # Keypad not found, do nothing

    def handshake(self):
        last_attempt = 0
        connection_attempt = 1
        
        while True:
            if last_attempt != connection_attempt:
                self.serial_port.write(b"PING\n")
                self.ping_timeStamp = time.monotonic()

            if connection_attempt > 3:
                print("Failed to establish connection after 3 attempts.")
                return False
            
            elif self.serial_port.in_waiting > 0:
                response = self.serial_port.readline().decode().strip()
                if response == "PONG":
                    print("Connection established successfully!")
                    return True
                else:
                    print(f"Unexpected response: {response}")
                    print(f"Connection attempt {connection_attempt} failed retrying...")
                    connection_attempt += 1

            elif time.monotonic() - self.ping_timeStamp > 3:  # 3 seconds timeout
                print(f"Connection attempt {self.connection_attempt} failed retrying...")
                self.connection_attempt += 1




if __name__ == "__main__":
    import sys

    app = QtCore.QCoreApplication(sys.argv)
    worker = BackgroundProcess()

    sys.exit(app.exec())