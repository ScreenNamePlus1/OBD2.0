# OBD-II Diagnostic Tool

A Python GUI application built with Tkinter and the `python-obd` library to read diagnostic trouble codes (DTCs) and real-time vehicle data (e.g., RPM, speed, coolant temperature) via an OBD-II adapter.

## Features
- Connect to an OBD-II adapter (e.g., ELM327) via USB, Bluetooth, or Wi-Fi.
- Display diagnostic trouble codes (DTCs) in a scrollable text area.
- Monitor real-time vehicle data, including RPM, speed, and coolant temperature.
- User-friendly GUI with start/stop monitoring and connection status.

## Requirements
- **Hardware**:
  - OBD-II adapter (e.g., ELM327, USB or Bluetooth).
  - A vehicle with an OBD-II port (standard in most cars post-1996 in the US).
- **Software**:
  - Python 3.x
  - `python-obd` library (`pip install obd`)
ល
  - `pyserial` for USB adapters (`pip install pyserial`)
  - Tkinter (included with standard Python installations)

## Installation
1. Install Python 3.x from [python.org](https://www.python.org).
2. Install required libraries:
   ```bash
   pip install obd pyserial
