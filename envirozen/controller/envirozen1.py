from prometheus import query_prometheus
import config as config
import actions as actions
import time
import subprocess

def start_server():
    # Start server.py as a separate process
    subprocess.Popen(["python3", "server.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

def evaluate_metrics():
    # Create a dictionary that maps metric names to actions and thresholds
    metric_actions = {
        'temperature_ambient': (actions.ac_on, 'AC Mode', 'Ambient Temperature', 'above Tolerance'),
        'temperature_hot': (actions.ac_on, 'AC Mode', 'Hot Aisle Temperature', 'above Tolerance'),
        'temperature_cold_min': (actions.freecooling, 'Freecooling Mode', 'Cold Aisle Temperature', 'Within Tolerances'),
        'temperature_cold_warning': (actions.freecooling_turbo, 'Freecooling Turbo Mode', 'Cold Aisle Temperature', 'above Tolerance'),
        'temperature_cold': (actions.ac_on, 'AC Mode', 'Cold Aisle Temperature', 'above Tolerance'),
    }

    # Initialize a flag to determine if any condition was met
    condition_met = False

    # Iterate over all metric names and their corresponding queries
    for metric_name, (action_function, mode, temp_type, tolerance_desc) in metric_actions.items():
        if condition_met:
            break  # If a condition was met in a previous iteration, stop evaluating further

        # Query Prometheus for the metric data
        result = query_prometheus(query=config.QUERIES.get(metric_name))

        # Initialize temperature_value with a default value (e.g., None)
        temperature_value = None

        # Iterate over the result set from Prometheus
        for entry in result:
            # Extract the temperature value from the result entry
            temperature = entry.get('value', [None, None])[1]

            # If a temperature value is found, process it
            if temperature is not None:
                temperature_value = float(temperature)

                # Retrieve the threshold for the current metric
                threshold = config.METRIC_THRESHOLDS.get(metric_name)

                # Check if the temperature_value crosses the threshold
                if threshold is not None and temperature_value > threshold:
                    # If it crosses, perform the associated action, set the condition flag, and break the loop
                    action_function(temperature_value)
                    print(f"Room in {mode}: {temp_type} of ({temperature_value}°C) is {tolerance_desc}")
                    condition_met = True
                    break  # This will only break the inner loop (iterating over the result set)

    # If no condition was met, set the room mode to passive
    if not condition_met:
        actions.passive_cooling(temperature_value)
        print(f"Room in Passive Cooling Mode: ({temperature_value}°C)")

def main():
    start_server()  # Start the server process
    while True:
        evaluate_metrics()  # Perform metric evaluation and actions
        time.sleep(config.evaluation_interval)  # Wait for the specified interval before re-evaluating

if __name__ == "__main__":
    main()
