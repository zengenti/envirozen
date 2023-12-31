# Import necessary configurations and functions
from prometheus import query_prometheus
import config as config
import actions as actions
import time

def room_mode():
    # Iterate over all metric names and their corresponding queries
    for metric_name, query in config.QUERIES.items():
        # Query Prometheus for the metric data
        result = query_prometheus(query)
        # Print the name of the current metric
        # print(f"{metric_name}:")

        # Initialize temperature_value with a default value (e.g., None)
        temperature_value = 1

        # Iterate over the result set from Prometheus
        for entry in result:
            # Extract the temperature value from the result entry
            temperature = entry.get('value', [None, None])[1]
            
            # If a temperature value is found, process it
            if temperature:
                # Convert the temperature value to a float for comparison
                temperature_value = float(temperature)
                action_taken = False

                # Retrieve the threshold for the current metric from the METRIC_THRESHOLDS dictionary in config.py
                threshold = config.METRIC_THRESHOLDS.get(metric_name, None)
                
                # Check if there's a defined threshold for the current metric
                if threshold is not None:

                    # Call the 'ac_on' function when 'temperature_ambient' exceeds threshold
                    if metric_name == 'temperature_ambient' and temperature_value > threshold:
                        actions.ac_on(temperature_value)
                        print(f" Room in AC Mode: Ambient Temperature of ({temperature_value}°C) is above Tolerance")
                        action_taken = True
                        break  # Exit the loop once the condition is met
                    # Call the 'ac_on' function when 'temperature_hot' exceeds threshold
                    elif metric_name == 'temperature_hot' and temperature_value > threshold:
                        actions.ac_on(temperature_value)
                        print(f" Room in AC Mode: Hot Ailse Temperature of ({temperature_value}°C) is above Tolerance")
                        action_taken = True
                        break  # Exit the loop once the condition is met
                    # Call the 'ac_on' function when 'temperature_cold' exceeds threshold
                    elif metric_name == 'temperature_cold' and temperature_value > threshold:
                        actions.ac_on(temperature_value)
                        print(f" Room in AC Mode: Cold Ailse Temperature of ({temperature_value}°C) is above Tolerance")
                        action_taken = True
                        break  # Exit the loop once the condition is met
                    # Call the 'freecooling_turbo' function when 'temperature_cold_warning' exceeds threshold
                    elif metric_name == 'temperature_cold_warning' and temperature_value > threshold:
                        actions.freecooling_turbo(temperature_value)
                        print(f" Room in Freecooling Turbo Mode: Cold Ailse Temperature of ({temperature_value}°C) is above Tolerance")
                        action_taken = True
                        break  # Exit the loop once the condition is met
                    # Call the 'passive_cooling' function when 'temperature_cold_min' is under the threshold
                    elif metric_name == 'temperature_cold_min' and temperature_value < threshold:
                        actions.passive_cooling(temperature_value)
                        print(f" Room in Passive Mode: Cold Ailse Temperature of ({temperature_value}°C) is below Tolerance")
                        action_taken = True
                        break  # Exit the loop once the condition is met
                    else:
                        # All values are within tolerence for FreeCooling
                        actions.freecooling(temperature_value)
                        print(f" Room in Freecooling Mode: All temperature are with Tolerance")
                else:
                    # If no threshold is defined for the metric, just print the temperature value
                    print(temperature_value)
        # If an action was taken, break out of the outer loop
        if action_taken:
            break

        # Print a separator for clarity
        print("-----------------------")

# Main execution starts here
if __name__ == "__main__":

    while True:
        room_mode()  # Perform metric evaluation and actions
        time.sleep(config.evaluation_interval)  # Wait for the specified interval before re-evaluating


