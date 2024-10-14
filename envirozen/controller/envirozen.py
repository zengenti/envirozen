from prometheus import query_prometheus
import config as config
import actions as actions
import time
import subprocess
import syslog

def start_server():
    """Start the Flask web server as a separate process."""
    subprocess.Popen(["python3", "server.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

# Create a file that records the mode of operation (manual or automatic)
STATUS_FILE = 'status.txt'
last_ac_activation_time = None

def evaluate_metrics():
    """Evaluate temperature metrics and determine the appropriate cooling mode."""
    
    # Define conditions under which AC should be turned on
    ac_on_conditions = {
        'temperature_ambient': (actions.ac_on, 'AC Mode', 'Ambient Temperature', 'above Tolerance'),
        'temperature_hot': (actions.ac_on, 'AC Mode', 'Hot Aisle Temperature', 'above Tolerance'),
        'temperature_cold': (actions.ac_on, 'AC Mode', 'Cold Aisle Temperature', 'above Tolerance'),
    }

    # Define conditions for other cooling methods if AC is not needed
    ac_off_conditions = {
        'temperature_cold_min': (actions.freecooling_turbo, 'Freecooling Mode', 'Cold Aisle Temperature', 'Within Tolerances'),
        'temperature_cold_warning': (actions.freecooling_turbo, 'Freecooling Turbo Mode', 'Cold Aisle Temperature', 'above Tolerance'),
    }

    # Define emergency conditions for extremely high temperatures
    emergency_conditions = {
        'temperature_hot_emergency': (actions.emergency, 'Emergency AC Mode', 'Hot Aisle Temperature', 'exceeds tolerance by 10°C'),
    }

    # Check if we're in automatic mode
    with open(STATUS_FILE, 'r') as file:
        if file.read().strip() != 'automatic':
            syslog.syslog(syslog.LOG_INFO, "In Manual mode; Envirozen automatic actions paused.")
            return

    def evaluate_condition_set(condition_set):
        """Evaluate a set of conditions against the current metrics."""
        global last_ac_activation_time  # Use the global variable for tracking AC activation time
        for metric_name, (action_function, mode, temp_type, tolerance_desc) in condition_set.items():
            # Query Prometheus for the metric data
            result = query_prometheus(query=config.QUERIES.get(metric_name))
            temperature_value = None  # Initialize temperature value

            for entry in result:
                # Extract and process temperature value
                temperature = entry.get('value', [None, None])[1]
                if temperature is not None:
                    temperature_value = float(temperature)
                    threshold = config.METRIC_THRESHOLDS.get(metric_name)

                    # Check for emergency condition: if temperature exceeds the hot tolerance threshold by 10 degrees
                    if metric_name == 'temperature_hot' and temperature_value > threshold + 10:
                        actions.ac_on(temperature_value)
                        syslog.syslog(syslog.LOG_ALERT, f"EMERGENCY: {mode}: {temp_type} of ({temperature_value}°C) is {tolerance_desc}")
                        return True  # Emergency action taken

                    # Check for normal conditions
                    if threshold is not None and temperature_value > threshold:
                        # Condition met, perform action
                        if last_ac_activation_time is None or time.time() - last_ac_activation_time >= config.MIN_AC_RUN_TIME:
                            last_ac_activation_time = time.time()  # Update the timestamp here
                            action_function(temperature_value)
                            syslog.syslog(syslog.LOG_INFO, f"Room in {mode}: {temp_type} of ({temperature_value}°C) is {tolerance_desc}")
                            return True  # Exiting function since condition was met
        return False  # No conditions were met

    # Evaluate emergency conditions first
    emergency_activated = evaluate_condition_set(emergency_conditions)

    # If no emergency conditions met, evaluate conditions for turning on the AC
    if not emergency_activated:
        ac_needed = evaluate_condition_set(ac_on_conditions)

        # If no AC on conditions met, evaluate the second set of conditions
        if not ac_needed:
            if last_ac_activation_time is not None:
                elapsed_time = time.time() - last_ac_activation_time
                if elapsed_time < config.MIN_AC_RUN_TIME:
                    syslog.syslog(syslog.LOG_INFO, "AC minimum run time not yet met, keeping AC on.")
                    return  # Skip turning off AC or alternative cooling
            alternative_cooling_activated = evaluate_condition_set(ac_off_conditions)

            # If no conditions in the second set are met, default to passive cooling
            if not alternative_cooling_activated:
                actions.passive_cooling(None)  # Assuming temperature value isn't needed here
                syslog.syslog(syslog.LOG_INFO, "Room in Passive Cooling Mode")


    # First, evaluate conditions for turning on the AC
    ac_needed = evaluate_condition_set(ac_on_conditions)

    # If no AC on conditions met, evaluate the second set of conditions
    if not ac_needed:
        if last_ac_activation_time is not None:
            elapsed_time = time.time() - last_ac_activation_time
            if elapsed_time < config.MIN_AC_RUN_TIME:
                syslog.syslog(syslog.LOG_INFO, "AC minimum run time not yet met, keeping AC on.")
                return  # Skip turning off AC or alternative cooling
        alternative_cooling_activated = evaluate_condition_set(ac_off_conditions)

        # If no conditions in the second set are met, default to passive cooling
        if not alternative_cooling_activated:
            actions.passive_cooling(None)  # Assuming temperature value isn't needed here
            syslog.syslog(syslog.LOG_INFO, "Room in Passive Cooling Mode")

def main():
    """Main function to start the server and continuously evaluate metrics."""
    start_server()
    while True:
        evaluate_metrics()
        time.sleep(config.evaluation_interval)

if __name__ == "__main__":
    # Set default mode to automatic
    with open(STATUS_FILE, 'w') as file:
        file.write('automatic')  
    main()
