import subprocess
import RPi.GPIO as GPIO
import sys
import thread
import time

#//===============CLEAR THE TERMINAL===============//
subprocess.call(["clear"])

#//===============SETUP GPIO PINS===============//
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

JIG_1_Signal = 12
JIG_2_Signal = 16
JIG_3_Signal = 18
JIG_4_Signal = 22
JIG_5_Signal = 24
JIG_6_Signal = 26

GPIO.setup(JIG_1_Signal, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(JIG_2_Signal, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(JIG_3_Signal, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(JIG_4_Signal, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(JIG_5_Signal, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(JIG_6_Signal, GPIO.OUT, initial=GPIO.LOW)

GPIO.output(JIG_1_Signal, GPIO.LOW)
GPIO.output(JIG_2_Signal, GPIO.LOW)
GPIO.output(JIG_3_Signal, GPIO.LOW)
GPIO.output(JIG_4_Signal, GPIO.LOW)
GPIO.output(JIG_5_Signal, GPIO.LOW)
GPIO.output(JIG_6_Signal, GPIO.LOW)

#//===============CONFIGURATION FILE===============//
File = sys.argv[1]
with open(File,"r") as Config_File:
    Config_Content = Config_File.readlines()
Config_Content = [x.strip() for x in Config_Content] 
	
Jig_Iterable = ["JIG_1","JIG_2","JIG_3","JIG_4","JIG_5","JIG_6"]
Number_of_JIGS = int(sys.argv[2])
if Number_of_JIGS > 6:
  Number_of_JIGS = 6
if Number_of_JIGS < 1:
  Number_of_JIGS = 1

JIG_1_Bootload_logfile = "/tmp/Jig1_Bootload.txt"
JIG_2_Bootload_logfile = "/tmp/Jig2_Bootload.txt"
JIG_3_Bootload_logfile = "/tmp/Jig3_Bootload.txt"
JIG_4_Bootload_logfile = "/tmp/Jig4_Bootload.txt"
JIG_5_Bootload_logfile = "/tmp/Jig5_Bootload.txt"
JIG_6_Bootload_logfile = "/tmp/Jig6_Bootload.txt"

#//===============FUNCTIONS===============//
# Burning of Bootloader/Firmware
def flash(jig_number, file, logfile, JigSignal, Chip):
  subprocess.call(["avrdude", "-p", Chip, "-C", "avrdude_gpio.conf", "-c", jig_number, "-U", file, "-l", logfile])

# Read of LogFile
def ReadLogFile(logfile):
  if 'AVR device not responding' in open(logfile).read():
    return True
	
#//===============MAIN LOOP PROGRAM===============//
#for JIG in Jig_Iterable:
for i in range(Number_of_JIGS):
  JIG = Jig_Iterable[i]
  print("===============" + JIG +"===============")

  Signal = JIG+"_Signal"
  Bootload_logfile = JIG+"_Bootload_logfile"
  
  # Read Each Line of Config File
  lineCounter = 0
  for line in Config_Content:
    #Find the configuration files for the current JIG
    if line == "["+JIG+"]":
      Bootloader_to_Upload = Config_Content[lineCounter+1]
      Selected_Chip = Config_Content[lineCounter+2]
      Firmware_to_Upload = Config_Content[lineCounter+3]
      print("BOOTLOADER:\t" +Bootloader_to_Upload)
      print("CHIP SELECTED:\t"+Selected_Chip)
      print("FIRMWARE:\t"+Firmware_to_Upload)
    else:
      lineCounter = lineCounter + 1

  print("Programming " + JIG +"...")
  print("\tBootloading " + JIG +"...")
  
  #Flash first using the bootloader file
  flash(JIG, Bootloader_to_Upload, eval(Bootload_logfile), Signal, Selected_Chip)
  if not ReadLogFile(eval(Bootload_logfile)):
    GPIO.output(eval(Signal), GPIO.LOW)
    print("\tBootLoad DONE!")
    print("\t\tUploading Firmware to " + JIG + "...")
	
	#if no problem occur, upload the firmware
    flash(JIG, Firmware_to_Upload, eval(Bootload_logfile), Signal, Selected_Chip)
    if not ReadLogFile(eval(Bootload_logfile)):
      GPIO.output(eval(Signal), GPIO.LOW)
      print("\t\tFirmWare DONE!")
    else:
      GPIO.output(eval(Signal), GPIO.HIGH)
      print("\t\tERROR! See log file at " + eval(Bootload_logfile))
  else:
    GPIO.output(eval(Signal), GPIO.HIGH)
    print("\tERROR! See log file at " + eval(Bootload_logfile))

Config_File.close()