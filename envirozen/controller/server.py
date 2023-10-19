from prometheus_api_client import PrometheusConnect
import config as config
from flask import Flask, render_template, redirect, url_for
import actions
import envirozen

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

@app.route('/ac')
def ac_on():
    actions.ac_on_web()
    # Redirect back to the main page after the action is performed
    return redirect(url_for('display_temperature'))

@app.route('/freecooling')
def freecooling():
    actions.freecooling_web()
    # Redirect back to the main page after the action is performed
    return redirect(url_for('display_temperature'))

@app.route('/freecooling_turbo')
def freecooling_turbo():
    actions.freecooling_turbo_web()
    # Redirect back to the main page after the action is performed
    return redirect(url_for('display_temperature'))

@app.route('/passive')
def passive_cooling_web():
    actions.passive_cooling_web()
    # Redirect back to the main page after the action is performed
    return redirect(url_for('display_temperature'))

@app.route('/auto')
def auto():
    envirozen.room_mode()
    # Redirect back to the main page after the action is performed
    return redirect(url_for('display_temperature'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
