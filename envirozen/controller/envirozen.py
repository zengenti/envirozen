from prometheus import query_prometheus
import config as config
import actions as actions
import time
import subprocess
import syslog

def start_server():
    # Start server.py as a separate process. Flask Web app @ http://envirozen.zengenti.io
    subprocess.Popen(["python3", "server.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

# Create a file that records the mode of operation (manual or automatic)
STATUS_FILE = 'status.txt'

def evaluate_metrics():
    # First, define the conditions under which AC should be turned on
    ac_on_conditions = {
        'temperature_ambient': (actions.ac_on, 'AC Mode', 'Ambient Temperature', 'above Tolerance'),
        'temperature_hot': (actions.ac_on, 'AC Mode', 'Hot Aisle Temperature', 'above Tolerance'),
        'temperature_cold': (actions.ac_on, 'AC Mode', 'Cold Aisle Temperature', 'above Tolerance'),
    }

    # Then, define the conditions for other cooling methods if AC is not needed. Neeeds work on ordering
    ac_off_conditions = {
        'temperature_cold_min': (actions.freecooling_turbo, 'Freecooling Mode', 'Cold Aisle Temperature', 'Within Tolerances'),
        'temperature_cold_warning': (actions.freecooling_turbo, 'Freecooling Turbo Mode', 'Cold Aisle Temperature', 'above Tolerance'),
    }

    # Check if we're in automatic mode
    with open(STATUS_FILE, 'r') as file:
        if file.read().strip() != 'automatic':
            syslog.syslog(syslog.LOG_INFO, "In Manual mode; Envirozen automatic actions paused.")
            return

    def evaluate_condition_set(condition_set):
        """Evaluate a set of conditions against the current metrics."""
        for metric_name, (action_function, mode, temp_type, tolerance_desc) in condition_set.items():
            # Query Prometheus for the metric data
            result = query_prometheus(query=config.QUERIES.get(metric_name))
            temperature_value = None  # Initialize temperature_value

            for entry in result:
                # Extract and process temperature value
                temperature = entry.get('value', [None, None])[1]
                if temperature is not None:
                    temperature_value = float(temperature)
                    threshold = config.METRIC_THRESHOLDS.get(metric_name)

                    if threshold is not None and temperature_value > threshold:
                        # Condition met, perform action, and return True
                        action_function(temperature_value)
                        syslog.syslog(syslog.LOG_INFO, f"Room in {mode}: {temp_type} of ({temperature_value}°C) is {tolerance_desc}")
                        return True  # Exiting function since condition was met
        return False  # No conditions were met

    # First, evaluate conditions for turning on the AC
    ac_needed = evaluate_condition_set(ac_on_conditions)

    # If no AC on conditions met, evaluate the second set of conditions
    if not ac_needed:
        alternative_cooling_activated = evaluate_condition_set(ac_off_conditions)

        # If no conditions in the second set are met, default to passive cooling
        if not alternative_cooling_activated:
            actions.passive_cooling(None)  # Assuming temperature value isn't needed here
            syslog.syslog(syslog.LOG_INFO, "Room in Passive Cooling Mode")

def main():
    start_server()
    while True:
        evaluate_metrics()
        time.sleep(config.evaluation_interval)

if __name__ == "__main__":
    with open(STATUS_FILE, 'w') as file:
        file.write('automatic')  # Default mode
    main()
