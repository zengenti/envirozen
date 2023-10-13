import RPi.GPIO as GPIO

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

def temperature_within_tolerance(value):
    print(f"Temperature ({value}°C) is within Tolerance")

    # Close the damper if temperature is below tolerance
    close_damper()

def temperature_above_tolerance(value):
    print(f"Temperature ({value}°C) is above Tolerance")
    
    # Open the damper if temperature is above tolerance
    open_damper()
