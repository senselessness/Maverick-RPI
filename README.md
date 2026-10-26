Mavrik Distribution System
Includes a scrapped web app template
Two pump control for bottle distribution with recipes.
Current design is 5 recipes controlled by 3 buttons.
  Up arrow, down arrow, and select.
App currently incomplete. Left off on Navigation 10/26/2026
Equipment:
  RPI 3B+ with python ~3.14
  Diaphragm Pump On/Off control.
  Peristaltic Pump with Modbus Communication
  USB->Modbus communication device
    Max485 with Signal Converter in back pocket for later implementation.
    Had issues prior. 
      Assuming RPI UART 3.3V comm signals need to be 5V comm signals to communicate with pump.
      Will test with Signal Converter
  Relay HAT
  LCD Screen with I2C
