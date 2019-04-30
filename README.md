# RPIasBootFirmwareProgrammer
Develop a Programming Jig to use in production

This code is use in programming multiple Atmega Chips used in production line.
It uses the ICSP of microntroller in order to bootload and burn firmware to several chips.

AVRdude was used in order to make this possible. In order to make serveral ISCP pins in RPI, a config file was created with
IDs : JIG_1, JIG_2, JIG_3, JIG_4, JIG_5, JIG_6.
Each Jig ID utilizes its own MOSI-MISO-SCK pins to eliminate pulse contention. Each IDs utilizes a a single reset pin.

A config file for the python program to read is also created

~USAGE:
SYNTAX: sudo python [program_name] [jig_config_file] [number_of_jigs]

~INSIDE CONFIG FILE:
Format:
  [JIG_#]
  Bootloader_HEX_file     -> Type of bootloader environment [Arduino pro mini, Uno, etc]
  Selected_Chip           -> type of Chip used [Atmega328p alike] 
  Firmware_HEX_file       -> Firmware you created using Arduino IDE
  
 
