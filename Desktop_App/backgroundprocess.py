from PySide6 import QtCore
import serial as serial
from serial.tools import list_ports
import time
import re
import subprocess
import webbrowser

KEYPAD_VID = 0x239A
KEYPAD_PID = 0x8106
KEYPAD_SERIAL_NUMBER = "DF648C8653620E32"


def find_keypad_ports():
    matching_ports = []

    for port in list_ports.comports():
        if port.vid == KEYPAD_VID and port.serial_number == KEYPAD_SERIAL_NUMBER:
            matching_ports.append(port)

    def port_priority(port):
        metadata = f"{port.interface or ''} {port.description or ''}".lower()

        if "data" in metadata:
            return (0, 0)

        if "console" in metadata:
            return (2, 0)

        match = re.fullmatch(r"COM(\d+)", port.device, re.IGNORECASE)
        com_number = int(match.group(1)) if match else 0
        return (1, -com_number)

    matching_ports.sort(key=port_priority)

    return [port.device for port in matching_ports]


class BackgroundProcess(QtCore.QObject):
    connection_changed = QtCore.Signal(bool)

    def __init__(self, parent=None, print_connection = False):
        super().__init__(parent)
        self.serial_port = None
        self.connected = False
        self.ping_timeStamp = 0
        self.waiting_for_pong = False
        self.print = print_connection

        self.Connect_timer = QtCore.QTimer(self)
        self.Connect_timer.timeout.connect(self.connect_task)
        self.Connect_timer.start(500)  # Run every 500 milliseconds

        self.ConnectionUpkeep_timer = QtCore.QTimer(self)
        self.ConnectionUpkeep_timer.timeout.connect(self.Check_Connection)

        self.Listner_timer = QtCore.QTimer(self)
        self.Listner_timer.timeout.connect(self.Detect_Message)


    def set_connected(self, connected):
        if self.connected == connected:
            return
        self.connected = connected
        self.connection_changed.emit(connected)

        if connected:
            self.Connect_timer.stop()
            self.waiting_for_pong = False
            self.ConnectionUpkeep_timer.start(1000)
            self.Listner_timer.start(50)
        else:
            self.ConnectionUpkeep_timer.stop()
            self.Listner_timer.stop()
            self.waiting_for_pong = False

            if self.serial_port and self.serial_port.is_open:
                try:
                    self.serial_port.close()
                except (serial.SerialException, OSError):
                    pass

            self.serial_port = None
            self.Connect_timer.start(500)



    @QtCore.Slot()
    def Detect_Message(self):
        if not self.connected:
            return

        try:
            while self.serial_port.in_waiting > 0:
                response = self.serial_port.readline().decode(
                    errors="replace"
                ).strip()

                if response == "PONG":
                    self.waiting_for_pong = False
                    if self.print:
                        print("Connection Active")
                elif response:
                    self.execute_cmd(response)

            if (
                self.waiting_for_pong
                and time.monotonic() > self.ping_timeStamp + 0.75
            ):
                if self.print:
                    print("Connection deadline exceeded")
                self.set_connected(False)

        except (serial.SerialException, OSError) as error:
            if self.print:
                print(f"Keypad was removed: {error}")
            self.set_connected(False)

    @QtCore.Slot()
    def Check_Connection(self):
        if not self.connected or self.waiting_for_pong:
            return

        try:
            self.serial_port.write(b"PING\n")
            if self.print:
                print("Said: PING")
            self.ping_timeStamp = time.monotonic()
            self.waiting_for_pong = True

        except (serial.SerialException, OSError) as error:
            if self.print:
                print(f"Keypad was removed: {error}")
            self.set_connected(False)



    @QtCore.Slot()
    def connect_task(self):
        if self.connected:
            return

        for port in find_keypad_ports():
            try:
                print(f"Keypad found on port: {port}")
                self.serial_port = serial.Serial(
                    port=port,
                    baudrate=19200,
                    timeout=0.1,
                    write_timeout=1,
                )

                if self.handshake():
                    self.set_connected(True)
                    self.Connect_timer.stop()
                    return port

            except serial.SerialException as error:
                print(f"Could not communicate with {port}: {error}")

            if self.serial_port and self.serial_port.is_open:
                self.serial_port.close()

            self.serial_port = None

    def handshake(self):
        self.serial_port.reset_input_buffer()

        for connection_attempt in range(1, 4):
            self.serial_port.write(b"PING\n")
            if self.print:
                print("Said: PING")
            deadline = time.monotonic() + 3

            while time.monotonic() < deadline:
                if self.serial_port.in_waiting > 0:
                    response = (
                        self.serial_port.readline().decode(errors="replace").strip()
                    )

                    if response == "PONG":
                        if self.print:
                            print("Connection established successfully!")
                        return True

                    if self.print:
                        print(f"Unexpected response: {response}")

                time.sleep(0.01)
            if self.print:
                print(f"Connection attempt {connection_attempt} failed; retrying...")

        if self.print:
            print("Failed to establish connection after 3 attempts.")
        return False

    def execute_cmd(self, message):
        if message.startswith("LAUNCH:"):
                subprocess.Popen(
                [message[7:]],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=True,
                creationflags=(
                    subprocess.DETACHED_PROCESS
                    | subprocess.CREATE_NEW_PROCESS_GROUP
                    | subprocess.CREATE_BREAKAWAY_FROM_JOB
                ),
                )

        elif message.startswith("URL:"):
            url = message[4:]
            webbrowser.open(url)

        elif message.startswith("CMD:"):
            command = message[4:]
            subprocess.Popen(
                [
                    "powershell.exe",
                    "-NoProfile",
                    "-NonInteractive",
                    "-Command",
                    command,
                ],
                creationflags=subprocess.CREATE_NO_WINDOW,
            )

if __name__ == "__main__":
    import sys

    app = QtCore.QCoreApplication(sys.argv)
    worker = BackgroundProcess()

    sys.exit(app.exec())
