# Import necessary configurations and functions
from config import QUERIES, METRIC_THRESHOLDS
from prometheus import query_prometheus
from actions import temperature_within_tolerance, temperature_above_tolerance

def print_metrics():
    # Iterate over all metric names and their corresponding queries
    for metric_name, query in QUERIES.items():
        # Query Prometheus for the metric data
        result = query_prometheus(query)
        # Print the name of the current metric
        print(f"{metric_name}:")

        # Iterate over the result set from Prometheus
        for entry in result:
            # Extract the temperature value from the result entry
            temperature_value = entry.get('value', [None, None])[1]
            
            # If a temperature value is found, process it
            if temperature_value:
                # Convert the temperature value to a float for comparison
                temperature_float = float(temperature_value)

                # Retrieve the threshold for the current metric from the METRIC_THRESHOLDS dictionary in config.py
                threshold = METRIC_THRESHOLDS.get(metric_name, None)
                
                # Check if there's a defined threshold for the current metric
                if threshold is not None:
                    # Compare the temperature with the threshold
                    if temperature_float < threshold:
                        # If temperature is within the threshold, call the appropriate action
                        temperature_within_tolerance(temperature_float)
                    else:
                        # If temperature exceeds the threshold, call the appropriate action
                        temperature_above_tolerance(temperature_float)
                else:
                    # If no threshold is defined for the metric, just print the temperature value
                    print(temperature_float)

        # Print a separator for clarity
        print("-----------------------")

# Main execution starts here
if __name__ == "__main__":
    print_metrics()
