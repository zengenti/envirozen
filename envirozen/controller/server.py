from prometheus_api_client import PrometheusConnect
import config as config
from flask import Flask, render_template

app = Flask(__name__)

# Initialize Prometheus client using the URL from config
prometheus_api = PrometheusConnect(url=config.PROMETHEUS_URL)

@app.route('/')
def display_temperature():
    # Create an empty dictionary to store metric names and values
    metric_values = {}

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

if __name__ == '__main__':
    app.run()
