#!/usr/bin/env python3
"""serial_sender.py

Simple script to send single key presses over a serial port to the Arduino
sketch. It opens a serial connection (default 115200) and sends the pressed
key as a single byte. Works on macOS, Linux and Windows.

Usage:
  python3 serial_sender.py /dev/ttyUSB0
  python3 serial_sender.py COM3  # on Windows

Install:
  pip install pyserial

Controls:
  Press the keys shown in the Arduino sketch (d/a, s/w, i/k, l/o, q/e).
  Press Ctrl-C to exit.
"""

import sys
import time
import argparse

try:
    import serial
except ImportError:
    print("pyserial is required. Install with: pip install pyserial")
    sys.exit(1)

# Cross-platform single-keypress
if sys.platform.startswith("win"):
    import msvcrt

    def getch():
        return msvcrt.getch()
else:
    import tty
    import termios

    def getch():
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            return ch.encode('utf-8')
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


def main():
    parser = argparse.ArgumentParser(description="Send single key presses over serial")
    parser.add_argument("port", help="Serial port to open (e.g. /dev/ttyUSB0 or COM3)")
    parser.add_argument("-b", "--baud", type=int, default=115200, help="Baud rate (default 115200)")
    args = parser.parse_args()

    try:
        ser = serial.Serial(args.port, args.baud, timeout=0.1)
    except Exception as e:
        print(f"Failed to open serial port {args.port}: {e}")
        sys.exit(1)

    print(f"Opened {args.port} @ {args.baud}. Press keys to send; Ctrl-C to exit.")
    try:
        while True:
            ch = getch()
            if not ch:
                continue
            # msvcrt returns bytes already; on POSIX we returned bytes
            # Send single byte over serial
            try:
                ser.write(ch[:1])
                # optional small delay to ensure Arduino receives
                time.sleep(0.01)
            except Exception as e:
                print(f"Serial write failed: {e}")
                break
            # Echo what we sent for user feedback
            try:
                printable = ch.decode('utf-8', errors='replace')
            except Exception:
                printable = '?'
            print(f"Sent: {printable}")
    except KeyboardInterrupt:
        print("\nExiting")
    finally:
        ser.close()


if __name__ == '__main__':
    main()
