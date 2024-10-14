import RPi.GPIO as GPIO

# Disable GPIO warnings
GPIO.setwarnings(False)

# Use Broadcom SOC channel numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO pins
FAN_1_PIN = 22
FAN_2_PIN = 26
AC_PIN = 6
DAMPER_PIN = 4

# Pin setup
GPIO.setup(FAN_1_PIN, GPIO.OUT)   # Corresponds to WiringPi pin 3
GPIO.setup(FAN_2_PIN, GPIO.OUT)   # Corresponds to WiringPi pin 25
GPIO.setup(AC_PIN, GPIO.OUT)       # Corresponds to WiringPi pin 22
GPIO.setup(DAMPER_PIN, GPIO.OUT)   # Corresponds to WiringPi pin 7

def cleanup_gpio():
    """Cleans up all the GPIO settings by resetting the GPIO pins."""
    GPIO.cleanup()

def turn_on_fan_1():
    """Turns on fan 1 by setting its GPIO pin to HIGH."""
    GPIO.output(FAN_1_PIN, GPIO.HIGH)

def turn_off_fan_1():
    """Turns off fan 1 by setting its GPIO pin to LOW."""
    GPIO.output(FAN_1_PIN, GPIO.LOW)

def turn_on_fan_2():
    """Turns on fan 2 by setting its GPIO pin to HIGH."""
    GPIO.output(FAN_2_PIN, GPIO.HIGH)

def turn_off_fan_2():
    """Turns off fan 2 by setting its GPIO pin to LOW."""
    GPIO.output(FAN_2_PIN, GPIO.LOW)

def turn_on_ac():
    """Turns on the AC unit by setting its GPIO pin to LOW."""
    GPIO.output(AC_PIN, GPIO.LOW)

def turn_off_ac():
    """Turns off the AC unit by setting its GPIO pin to HIGH."""
    GPIO.output(AC_PIN, GPIO.HIGH)

def open_damper():
    """Opens the damper by setting its GPIO pin to HIGH."""
    GPIO.output(DAMPER_PIN, GPIO.HIGH)

def close_damper():
    """Closes the damper by setting its GPIO pin to LOW."""
    GPIO.output(DAMPER_PIN, GPIO.LOW)

def ac_on(temperature_value):
    """
    Activates the AC unit and prepares for cooling.

    Closes the damper, turns off both fans, and turns on the AC unit.
    
    Parameters:
    - temperature_value (float): The current temperature reading (not used in this function).
    """
    close_damper()
    turn_off_fan_1()
    turn_off_fan_2()
    turn_on_ac()

def freecooling(temperature_value):
    """
    Activates free cooling mode.

    Opens the damper, turns on fan 1, turns off fan 2, and turns off the AC unit.

    Parameters:
    - temperature_value (float): The current temperature reading (not used in this function).
    """
    open_damper()
    turn_on_fan_1()
    turn_off_fan_2()
    turn_off_ac()

def freecooling_turbo(temperature_value):
    """
    Activates turbo free cooling mode.

    Opens the damper, turns on both fans, and turns off the AC unit.

    Parameters:
    - temperature_value (float): The current temperature reading (not used in this function).
    """
    open_damper()
    turn_on_fan_1()
    turn_on_fan_2()
    turn_off_ac()

def passive_cooling(temperature_value):
    """
    Activates passive cooling mode.

    Opens the damper, turns off both fans, and turns off the AC unit.

    Parameters:
    - temperature_value (float): The current temperature reading (not used in this function).
    """
    open_damper()
    turn_off_fan_1()
    turn_off_fan_2()
    turn_off_ac()

def emergency(temperature_value):
    """
    Emergency Mode, something has gone wrong.
    Something like the AC has failed try everything to cool down.

    Opens the damper, turns on both fans, and turns on the AC unit.
    """
    open_damper()
    turn_on_fan_1()
    turn_on_fan_2()
    turn_on_ac()

def ac_on_web():
    """
    Activates the AC unit for web control.

    Closes the damper, turns off both fans, and turns on the AC unit.
    """
    close_damper()
    turn_off_fan_1()
    turn_off_fan_2()
    turn_on_ac()

def freecooling_web():
    """
    Activates free cooling mode for web control.

    Opens the damper, turns on fan 1, turns off fan 2, and turns off the AC unit.
    """
    open_damper()
    turn_on_fan_1()
    turn_off_fan_2()
    turn_off_ac()

def freecooling_turbo_web():
    """
    Activates turbo free cooling mode for web control.

    Opens the damper, turns on both fans, and turns off the AC unit.
    """
    open_damper()
    turn_on_fan_1()
    turn_on_fan_2()
    turn_off_ac()

def passive_cooling_web():
    """
    Activates passive cooling mode for web control.

    Opens the damper, turns off both fans, and turns off the AC unit.
    """
    open_damper()
    turn_off_fan_1()
    turn_off_fan_2()
    turn_off_ac()

def emergency_web():
    """
    Emergency Mode, something has gone wrong.
    Something like the AC has failed try everything to cool down.

    Opens the damper, turns on both fans, and turns on the AC unit.
    """
    open_damper()
    turn_on_fan_1()
    turn_on_fan_2()
    turn_on_ac()
