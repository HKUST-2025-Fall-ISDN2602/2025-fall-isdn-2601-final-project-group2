#!/usr/bin/env python3
"""serial_sender.py

PyQt5-based serial sender that captures multiple simultaneous key presses
and sends them to an Arduino over serial.

Usage:
  python3 serial_sender.py /dev/cu.usbserial-XXX
  python3 serial_sender.py COM3  # on Windows

Install:
  pip install pyserial PyQt5

Controls:
  Press the keys shown in the Arduino sketch (d/a, s/w, i/k, l/o, q/e).
  Multiple keys can be held simultaneously.
  Close the window or press Escape to exit.
"""

import sys
import argparse

try:
    import serial
except ImportError:
    print("pyserial is required. Install with: pip install pyserial")
    sys.exit(1)

try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
    from PyQt5.QtCore import Qt, QTimer
    from PyQt5.QtGui import QFont
except ImportError:
    print("PyQt5 is required. Install with: pip install PyQt5")
    sys.exit(1)


class ServoController(QMainWindow):
    def __init__(self, ser, send_interval_ms=50):
        super().__init__()
        self.ser = ser
        self.pressed_keys = set()  # Currently held keys
        self.send_interval_ms = send_interval_ms

        self.init_ui()

        # Timer to send keys repeatedly while held
        self.timer = QTimer()
        self.timer.timeout.connect(self.send_pressed_keys)
        self.timer.start(self.send_interval_ms)

    def init_ui(self):
        self.setWindowTitle("Servo Controller - Press keys to control")
        self.setGeometry(100, 100, 400, 300)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        info = QLabel(
            "Controls:\n"
            "  d/a = servo1 -/+\n"
            "  s/w = servo2 -/+\n"
            "  i/k = servo3 -/+\n"
            "  l/o = servo4 -/+\n"
            "  q/e = servo5 -/+\n\n"
            "Hold multiple keys to move multiple servos.\n"
            "Press Escape to exit."
        )
        info.setFont(QFont("Courier", 14))
        layout.addWidget(info)

        self.status_label = QLabel("Pressed: (none)")
        self.status_label.setFont(QFont("Courier", 12))
        layout.addWidget(self.status_label)

    def keyPressEvent(self, event):
        if event.isAutoRepeat():
            return
        key = event.text().lower()
        if key in "adwsikolqe":
            self.pressed_keys.add(key)
            self.update_status()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def keyReleaseEvent(self, event):
        if event.isAutoRepeat():
            return
        key = event.text().lower()
        self.pressed_keys.discard(key)
        self.update_status()

    def update_status(self):
        if self.pressed_keys:
            self.status_label.setText(f"Pressed: {', '.join(sorted(self.pressed_keys))}")
        else:
            self.status_label.setText("Pressed: (none)")

    def send_pressed_keys(self):
        for key in self.pressed_keys:
            try:
                self.ser.write(key.encode('utf-8'))
            except Exception as e:
                print(f"Serial write failed: {e}")

    def closeEvent(self, event):
        self.timer.stop()
        try:
            self.ser.close()
        except Exception:
            pass
        event.accept()


def main():
    parser = argparse.ArgumentParser(description="PyQt5 serial sender for servo control")
    parser.add_argument("port", help="Serial port (e.g. /dev/cu.usbserial-XXX or COM3)")
    parser.add_argument("-b", "--baud", type=int, default=115200, help="Baud rate (default 115200)")
    parser.add_argument("-i", "--interval", type=int, default=50, help="Send interval in ms (default 50)")
    args = parser.parse_args()

    try:
        ser = serial.Serial(args.port, args.baud, timeout=0.1)
    except Exception as e:
        print(f"Failed to open serial port {args.port}: {e}")
        sys.exit(1)

    print(f"Opened {args.port} @ {args.baud}. Launching GUI...")

    app = QApplication(sys.argv)
    window = ServoController(ser, args.interval)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
