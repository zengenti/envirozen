from config import QUERIES
from prometheus import query_prometheus
from actions import temperature_within_tolerance, temperature_above_tolerance

def print_metrics():
    for metric_name, query in QUERIES.items():
        result = query_prometheus(query)
        print(f"{metric_name}:")

        for entry in result:
            temperature_value = entry.get('value', [None, None])[1]
            if temperature_value:
                temperature_float = float(temperature_value)

                if metric_name == 'temperature_ambient':
                    if temperature_float < 30:
                        temperature_within_tolerance(temperature_float)
                    else:
                        temperature_above_tolerance(temperature_float)
                else:
                    print(temperature_float)

        print("-----------------------")

if __name__ == "__main__":
    print_metrics()
