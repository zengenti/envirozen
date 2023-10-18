import RPi.GPIO as GPIO

# Disable GPIO warnings
GPIO.setwarnings(False)

# Use Broadcom SOC channel numbers
GPIO.setmode(GPIO.BCM)
FAN_1_PIN = 22
FAN_2_PIN = 26
AC_PIN = 6
DAMPER_PIN = 4

# Pin setup
GPIO.setup(FAN_1_PIN, GPIO.OUT)   # Corresponds to WiringPi pin 3
GPIO.setup(FAN_2_PIN, GPIO.OUT)  # Corresponds to WiringPi pin 25
GPIO.setup(AC_PIN, GPIO.OUT)   # Corresponds to WiringPi pin 22
GPIO.setup(DAMPER_PIN, GPIO.OUT)  # Corresponds to WiringPi pin 7

def cleanup_gpio():
    GPIO.cleanup()

def turn_on_fan_1():
    GPIO.output(FAN_1_PIN, GPIO.HIGH)

def turn_off_fan_1():
    GPIO.output(FAN_1_PIN, GPIO.LOW)

def turn_on_fan_2():
    GPIO.output(FAN_2_PIN, GPIO.HIGH)

def turn_off_fan_2():
    GPIO.output(FAN_2_PIN, GPIO.LOW)

def turn_on_ac():
    GPIO.output(AC_PIN, GPIO.HIGH)

def turn_off_ac():
    GPIO.output(AC_PIN, GPIO.LOW)

def open_damper():
    GPIO.output(DAMPER_PIN, GPIO.HIGH)

def close_damper():
    GPIO.output(DAMPER_PIN, GPIO.LOW)

def ac_on(temperature_value):
    
    # Close the damper if AC is On
    # Turn off both fans
    # Turn on AC unit
    close_damper()
    turn_off_fan_1()
    turn_off_fan_2()
    turn_on_ac()

def freecooling(temperature_value):
    
    # Open the damper as AC is off
    # Turn on fan 1
    # Turn off fan 2
    # Turn off AC unit
    open_damper()
    turn_on_fan_1()
    turn_off_fan_2()
    turn_off_ac()

def freecooling_turbo(temperature_value):
    
    # Open the damper as AC is off
    # Turn on both fans
    # Turn off AC unit
    open_damper()
    turn_on_fan_1()
    turn_on_fan_2()
    turn_off_ac()

def passive_cooling(temperature_value):
    
    # Open the damper as AC is off
    # Turn off both fans
    # Turn off AC unit
    open_damper()
    turn_off_fan_1()
    turn_off_fan_2()
    turn_off_ac()
