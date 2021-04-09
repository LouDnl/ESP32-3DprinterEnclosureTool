# WORK IN PROGRESS
This project is still in development. \
The files are still full of debug logs and commented out test code.

# Micropython ESP32 3D printer enclosure tools
I wanted to be able to monitor the temperature in the enclosure of my 3D printer and the CPU temperature of my printer mainboard.
For this I used Micropython on an ESP32 board.

Hardware used:
- ESP-WROOM-32 board 
- AHT-10 temperature and humidity sensor
- Thermistor

Micropython libraries used:
- [AHT-10](https://github.com/LouDnl/AHT10-Micropython-ESP32)
- Thermistor library
- LCD library

# To Do:
- Better webserver implementation
- MQTT or any other tool to make the board remote controllable
- RGB LED bar controls