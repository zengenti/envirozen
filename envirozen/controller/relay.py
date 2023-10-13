import RPi.GPIO as GPIO
import time

def main():
    # Use Broadcom SOC channel numbers
    GPIO.setmode(GPIO.BCM)
    
    # Pin setup
    GPIO.setup(4, GPIO.OUT)   # Corresponds to WiringPi pin 7
    GPIO.setup(22, GPIO.OUT)  # Corresponds to WiringPi pin 3
    GPIO.setup(6, GPIO.OUT)   # Corresponds to WiringPi pin 22
    GPIO.setup(26, GPIO.OUT)  # Corresponds to WiringPi pin 25
    
    print("relay testing!")

    try:
        while True:
            GPIO.output(4, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(4, GPIO.LOW)

            GPIO.output(22, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(22, GPIO.LOW)

            GPIO.output(6, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(6, GPIO.LOW)

            GPIO.output(26, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(26, GPIO.LOW)
            
            time.sleep(0.5)

    except KeyboardInterrupt:
        # Exit on CTRL+C
        pass

    finally:
        # Cleanup the GPIO settings
        GPIO.cleanup()

if __name__ == "__main__":
    main()
