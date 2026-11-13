# Waits for the reader's USB serial port (Espressif VID 0x303A), then appends every line it prints, time-stamped, to a
# log file; reconnects when the port drops (the reader reboots on a flash or sleep). Runs until killed.
# Usage: .pio-venv/Scripts/python.exe -I -X utf8 tools/serial_log.py <log file>  (pyserial from the PlatformIO venv; run in the background)
import sys
import time
from datetime import datetime

import serial
from serial.tools import list_ports

ESPRESSIF_VID = 0x303A
BAUD = 115200
POLL_S = 2


def find_port():
    for p in list_ports.comports():
        if p.vid == ESPRESSIF_VID:
            return p.device
    return None


def main():
    out = open(sys.argv[1], "a", encoding="utf-8", buffering=1)
    out.write(f"# {datetime.now():%Y-%m-%d %H:%M:%S} logger started, waiting for VID 303A\n")
    while True:
        port = find_port()
        if not port:
            time.sleep(POLL_S)
            continue
        out.write(f"# {datetime.now():%H:%M:%S} port {port} found\n")
        try:
            with serial.Serial(port, BAUD, timeout=1) as s:
                while True:
                    raw = s.readline()
                    if raw:
                        line = raw.decode("utf-8", "replace").rstrip()
                        out.write(f"{datetime.now():%H:%M:%S} {line}\n")
        except (serial.SerialException, OSError) as e:
            out.write(f"# {datetime.now():%H:%M:%S} port lost: {e}\n")
            time.sleep(POLL_S)


main()
