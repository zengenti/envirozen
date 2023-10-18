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
        print(f"{metric_name}:")

        # Iterate over the result set from Prometheus
        for entry in result:
            # Extract the temperature value from the result entry
            temperature = entry.get('value', [None, None])[1]
            
            # If a temperature value is found, process it
            if temperature:
                # Convert the temperature value to a float for comparison
                temperature_value = float(temperature_value)

                # Retrieve the threshold for the current metric from the METRIC_THRESHOLDS dictionary in config.py
                threshold = config.METRIC_THRESHOLDS.get(metric_name, None)
                
                # Check if there's a defined threshold for the current metric
                if threshold is not None:
                    # Check if the current metric is 'temperature_ambient'
                    if metric_name == 'temperature_ambient' and temperature_value > threshold:
                        # Call the 'ac_on' function when 'temperature_ambient' exceeds threshold
                        actions.ac_on(temperature_value)
                        print(f" Room in AC Mode: Ambient Temperature of ({temperature_value}°C) is above Tolerance")
                    elif metric_name == 'temperature_hot' and temperature_value > threshold:
                        # Call the 'ac_on' function when 'temperature_hot' exceeds threshold
                        actions.ac_on(temperature_value)
                        print(f" Room in AC Mode: Hot Ailse Temperature of ({temperature_value}°C) is above Tolerance")
                    elif metric_name == 'temperature_cold' and temperature_value > threshold:
                        # Call the 'ac_on' function when 'temperature_cold' exceeds threshold
                        actions.ac_on(temperature_value)
                        print(f" Room in AC Mode: Cold Ailse Temperature of ({temperature_value}°C) is above Tolerance")
                    elif metric_name == 'temperature_cold_warning' and temperature_value > threshold:
                        # Call the 'freecooling_turbo' function when 'temperature_cold_warning' exceeds threshold
                        actions.freecooling_turbo(temperature_value)
                        print(f" Room in Freecooling Turbo Mode: Cold Ailse Temperature of ({temperature_value}°C) is above Tolerance")
                    elif metric_name == 'temperature_cold_min' and temperature_value < threshold:
                        # Call the 'passive_cooling' function when 'temperature_cold_min' is under the threshold
                        actions.passive_cooling(temperature_value)
                        print(f" Room in Passive Mode: Cold Ailse Temperature of ({temperature_value}°C) is below Tolerance")
                    else:
                        # All values are within tolerence for FreeCooling
                        actions.freecooling()
                        print(f" Room in Freecooling Mode: All temperature are with Tolerance")
                else:
                    # If no threshold is defined for the metric, just print the temperature value
                    print(temperature_value)

        # Print a separator for clarity
        print("-----------------------")

# Main execution starts here
if __name__ == "__main__":

    while True:
        room_mode()  # Perform metric evaluation and actions
        time.sleep(config.evaluation_interval)  # Wait for the specified interval before re-evaluating
