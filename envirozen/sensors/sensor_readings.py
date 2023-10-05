# Import necessary libraries and modules
import math, time, machine, os, urequests, ujson
from machine import Pin, PWM, Timer
from pimoroni_i2c import PimoroniI2C
from pcf85063a import PCF85063A
from breakout_bme68x import BreakoutBME68X
from breakout_bh1745 import BreakoutBH1745
# from enviro import logging, enviro
# from constants import *


# common pins
HOLD_VSYS_EN_PIN              = 2
EXTERNAL_INTERRUPT_PIN        = 3
I2C_SDA_PIN                   = 4
I2C_SCL_PIN                   = 5
ACTIVITY_LED_PIN              = 6
BUTTON_PIN                    = 7
RTC_ALARM_PIN                 = 8
RAIN_PIN                      = 10

# warning led states
WARN_LED_OFF = 0
WARN_LED_ON = 1
WARN_LED_BLINK = 2

# wake reasons
WAKE_REASON_UNKNOWN           = None
WAKE_REASON_PROVISION         = 1
WAKE_REASON_BUTTON_PRESS      = 2
WAKE_REASON_RTC_ALARM         = 3
WAKE_REASON_EXTERNAL_TRIGGER  = 4
WAKE_REASON_RAIN_TRIGGER      = 5

# set up the button, external trigger, and rtc alarm pins
button_pin = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)
rtc_alarm_pin = Pin(RTC_ALARM_PIN, Pin.IN, Pin.PULL_DOWN)
external_trigger_pin = Pin(EXTERNAL_INTERRUPT_PIN, Pin.IN, Pin.PULL_DOWN)

hold_vsys_en_pin = Pin(HOLD_VSYS_EN_PIN, Pin.OUT, value=True)

# setup the i2c bus
i2c = PimoroniI2C(I2C_SDA_PIN, I2C_SCL_PIN, 100000)

# set up the activity led
activity_led_pwm = PWM(Pin(ACTIVITY_LED_PIN))
activity_led_pwm.freq(1000)
activity_led_pwm.duty_u16(0)

activity_led_timer = Timer(-1)
activity_led_pulse_speed_hz = 1

# intialise the pcf85063a real time clock chip
rtc = PCF85063A(i2c)

# ensure rtc clock is running - this should be true anyway?
i2c.writeto_mem(0x51, 0x00, b'\x00')

def warn_led(state):
  if state == WARN_LED_OFF:
    rtc.set_clock_output(PCF85063A.CLOCK_OUT_OFF)
  elif state == WARN_LED_ON:
    rtc.set_clock_output(PCF85063A.CLOCK_OUT_1024HZ)
  elif state == WARN_LED_BLINK:
    rtc.set_clock_output(PCF85063A.CLOCK_OUT_1HZ)
    
# the pcf85063a defaults to 32KHz clock output so
# we need to explicitly turn that off by default
warn_led(WARN_LED_OFF)

def get_date_str(self):
  datetime = rtc.datetime()
  return "{:04}-{:02}-{:02}".format(datetime[0], datetime[1], datetime[2])

def get_datetime_str(self):
  datetime = rtc.datetime()
  return "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(datetime[0], datetime[1], datetime[2], datetime[4], datetime[5], datetime[6])

def activity_led(brightness):
  brightness = max(0, min(100, brightness)) # clamp to range
  # gamma correct the brightness (gamma 2.8)
  value = int(pow(brightness / 100.0, 2.8) * 65535.0 + 0.5)
  activity_led_pwm.duty_u16(value)
  
def activity_led_callback(t):
  # updates the activity led brightness based on a sinusoid seeded by the current time
  activity_led((math.sin(time.ticks_ms() * math.pi * 2 / (1000 / activity_led_pulse_speed_hz)) * 40) + 60)

def pulse_activity_led(speed_hz = 1):
  global activity_led_timer, activity_led_pulse_speed_hz
  activity_led_pulse_speed_hz = speed_hz
  stop_activity_led() # if led already active then kill timer
  activity_led_timer.init(period=50, mode=Timer.PERIODIC, callback=activity_led_callback)

def stop_activity_led():
  global activity_led_timer
  activity_led_timer.deinit()
  activity_led(0)


def get_wake_reason():
  wake_reason = None
  if button_pin.value():
    wake_reason = WAKE_REASON_BUTTON_PRESS
  elif rtc_alarm_pin.value():
    wake_reason = WAKE_REASON_RTC_ALARM
  elif not external_trigger_pin.value():
    wake_reason = WAKE_REASON_EXTERNAL_TRIGGER


  return wake_reason

def wake_reason_name(wake_reason):
  wake_reason_names = {
    None: "unknown",
    WAKE_REASON_PROVISION: "provisioning",
    WAKE_REASON_BUTTON_PRESS: "button",
    WAKE_REASON_RTC_ALARM: "rtc_alarm",
    WAKE_REASON_EXTERNAL_TRIGGER: "external_trigger",
    WAKE_REASON_RAIN_TRIGGER: "rain_sensor"
  }

  if wake_reason in wake_reason_names:
    return wake_reason_names[wake_reason]
  return None



# guess which type of board this is based on the devices on the i2c bus
# and state of certain pins at startup
def model():
  # determine which type of board is connected
  i2c_devices = i2c.scan()

  result = None
  if 56 in i2c_devices: # 56 = colour / light sensor and only present on Indoor
    result = "indoor"
  elif 35 in i2c_devices: # 35 = ltr-599 on grow & weather
    # the wind vane pin is pulled high with a 10k resistor on the weather
    # board - we can detect this and disambiguate using it
    pump1_pin = Pin(10, Pin.IN, Pin.PULL_UP)
    result = "grow" if pump1_pin.value() == False else "weather"
    # disable the pull up (otherwise this keeps the weather board awake)
    pump1_pin.init(pull=None)
  else:
    # otherwise it's urban, we'll need to add camera in the future too...
    result = "urban"

  return result


def reset():
  machine.reset()


# from enviro.board import i2c

bme688 = BreakoutBME68X(i2c, address=0x77)

bh1745 = BreakoutBH1745(i2c)
# need to write default values back into bh1745 chip otherwise it
# reports bad results (this is undocumented...)
i2c.writeto_mem(0x38, 0x44, b'\x02')

def sensors():
  return [
    "temperature",
    "humidity",
    "pressure",
    "luminance",
    "color_temperature"
  ]

def lux_from_rgbc(r, g, b, c):
  if g < 1:
      tmp = 0
  elif (c / g < 0.160):
      tmp = 0.202 * r + 0.766 * g
  else:
      tmp = 0.159 * r + 0.646 * g
  tmp = 0 if tmp < 0 else tmp
  integration_time = 160
  gain = 1
  return round(tmp / gain / integration_time * 160)

def colour_temperature_from_rgbc(r, g, b, c):
  if (g < 1) or (r + g + b < 1):
      return 0
  r_ratio = r / (r + g + b)
  b_ratio = b / (r + g + b)
  e = 2.71828
  ct = 0
  if c / g < 0.160:
      b_eff = min(b_ratio * 3.13, 1)
      ct = ((1 - b_eff) * 12746 * (e ** (-2.911 * r_ratio))) + (b_eff * 1637 * (e ** (4.865 * b_ratio)))
  else:
      b_eff = min(b_ratio * 10.67, 1)
      ct = ((1 - b_eff) * 16234 * (e ** (-2.781 * r_ratio))) + (b_eff * 1882 * (e ** (4.448 * b_ratio)))
  if ct > 10000:
      ct = 10000
  return round(ct)

def get_sensor_readings():
  data = bme688.read()
  bh1745.measurement_time_ms(160)

  r, g, b, c = bh1745.rgbc_raw()

  return {
    "temperature": round(data[0], 2),
    "humidity": round(data[2], 2),
    "pressure": round(data[1] / 100.0, 2),
    "luminance": lux_from_rgbc(r, g, b, c),
    "color_temperature": colour_temperature_from_rgbc(r, g, b, c)
  }
