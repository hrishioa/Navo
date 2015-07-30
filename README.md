# Navo

Developed in part using [Mopusworks Tweeq library](https://github.com/hrishioa/tweeq-MPLABX-Examples).

There are three components to the system.

### Tweeq hardware
The code for the Tweeq hardware platform can be found in /Projects/BLE_Navo.X. The system collects IMU data, and transmits over Bluetooth Low Energy. Some refresh-rate calibration system has been implemented.

### Companion BLE Android App
The android app receives transmissions from Tweeq hardware and transmits it to an IOT dashboard after some postprocessing. Enables debugging. Located in /Android.

### Raspberry Pi Hardware companion.
The Raspberry Pi code pulls data from the IOT dashboard, uses IMU data collected onboard and computes possible courses for both devices. When a collision course is detected, relays are activated that cut the transmission line and enable the brake. Located in /Raspi-Code.
