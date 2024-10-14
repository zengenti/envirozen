from prometheus_api_client import PrometheusConnect
import config as config
from flask import Flask, render_template, redirect, url_for
import actions
import envirozen
import RPi.GPIO as GPIO
import os
import syslog

app = Flask(__name__)

# Initialize Prometheus client using the URL from config
prometheus_api = PrometheusConnect(url=config.PROMETHEUS_URL)
STATUS_FILE = 'status.txt'

@app.route('/')
def display_temperature():
    # Create an empty dictionary to store metric names and values
    metric_values = {}

    FAN_1_PIN = 22
    FAN_2_PIN = 26
    AC_PIN = 6
    DAMPER_PIN = 4

    # Read the state of PINs
    ac_pin_state = GPIO.input(AC_PIN)
    damper_pin_state = GPIO.input(DAMPER_PIN)
    fan1_pin_state = GPIO.input(FAN_1_PIN)
    fan2_pin_state = GPIO.input(FAN_2_PIN)

    # Map GPIO states to human-readable strings
    pin_state_mapping = {GPIO.HIGH: "ON", GPIO.LOW: "OFF"}
    # AC PIN state mapping is reveresed as we want the default (power absent)
    # to mean we run with AC. This protects against the controller power failing etc.
    ac_pin_state_mapping = {GPIO.HIGH: "OFF", GPIO.LOW: "ON"} 

    # Add PIN states to the metric_values dictionary
    metric_values['ac_pin_state'] = ac_pin_state_mapping.get(ac_pin_state, "UNKNOWN")
    metric_values['damper_pin_state'] = pin_state_mapping.get(damper_pin_state, "UNKNOWN")
    metric_values['fan1_pin_state'] = pin_state_mapping.get(fan1_pin_state, "UNKNOWN")
    metric_values['fan2_pin_state'] = pin_state_mapping.get(fan2_pin_state, "UNKNOWN")

    # Iterate over all metric names and their corresponding queries
    for metric_name, query in config.QUERIES.items():
        # Query Prometheus for the metric data
        result = prometheus_api.custom_query(query=query)

        # Iterate over the result set from Prometheus
        for entry in result:
            # Extract the temperature value from the result entry
            temperature = entry.get('value', [None, None])[1]

            # Store the metric name and value in the dictionary
            metric_values[metric_name] = temperature

    # Render an HTML template with the metric values
    return render_template('server.html', metric_values=metric_values)

@app.route('/ac')
def ac_on():
    with open(STATUS_FILE, 'w') as file:
        file.write('manual')  # Switch to manual mode
    actions.ac_on_web()
    syslog.syslog(syslog.LOG_INFO, "Manual AC Mode")
    # Redirect back to the main page after the action is performed
    return redirect(url_for('display_temperature'))

@app.route('/freecooling')
def freecooling():
    with open(STATUS_FILE, 'w') as file:
        file.write('manual')  # Switch to manual mode
    actions.freecooling_web()
    syslog.syslog(syslog.LOG_INFO, "Manual Freecooling Mode")
    # Redirect back to the main page after the action is performed
    return redirect(url_for('display_temperature'))

@app.route('/freecooling_turbo')
def freecooling_turbo():
    with open(STATUS_FILE, 'w') as file:
        file.write('manual')  # Switch to manual mode
    actions.freecooling_turbo_web()
    syslog.syslog(syslog.LOG_INFO, "Manual Freecooling Turbo Mode")
    # Redirect back to the main page after the action is performed
    return redirect(url_for('display_temperature'))

@app.route('/passive')
def passive_cooling_web():
    with open(STATUS_FILE, 'w') as file:
        file.write('manual')  # Switch to manual mode
    actions.passive_cooling_web()
    syslog.syslog(syslog.LOG_INFO, "Manual Passive Mode")
    # Redirect back to the main page after the action is performed
    return redirect(url_for('display_temperature'))

@app.route('/emergency')
def emergency_web():
    with open(STATUS_FILE, 'w') as file:
        file.write('emergency')  # Switch to emergency mode
    actions.passive_cooling_web()
    syslog.syslog(syslog.LOG_INFO, "Emergency Mode - All on")
    # Redirect back to the main page after the action is performed
    return redirect(url_for('display_temperature'))

@app.route('/auto')
def auto():
    with open(STATUS_FILE, 'w') as file:
        file.write('automatic')  # Switch back to automatic mode
    envirozen.evaluate_metrics()
    syslog.syslog(syslog.LOG_INFO, "Automatic Mode")
    # Redirect back to the main page after the action is performed
    return redirect(url_for('display_temperature'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
