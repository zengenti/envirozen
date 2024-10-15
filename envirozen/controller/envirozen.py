from prometheus import query_prometheus
import config as config
import actions as actions
import time
import subprocess
import syslog

def start_server():
    """Start the Flask web server as a separate process."""
    subprocess.Popen(["python3", "server.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

STATUS_FILE = 'status.txt'
last_ac_activation_time = None
ac_running = False  # Track whether the AC is currently running

def evaluate_metrics():
    """Evaluate temperature metrics and determine the appropriate cooling mode."""
    
    global last_ac_activation_time, ac_running  # Track AC state and last activation time

    # Check if we're in automatic mode
    with open(STATUS_FILE, 'r') as file:
        if file.read().strip() != 'automatic':
            syslog.syslog(syslog.LOG_INFO, "In Manual mode; Envirozen automatic actions paused.")
            return

    # Query Prometheus for temperature data
    def get_temperature(metric_name):
        query = config.QUERIES.get(metric_name)
        if not query:
            syslog.syslog(syslog.LOG_ERR, f"Invalid query for metric '{metric_name}'")
            return None
        
        result = query_prometheus(query=query)
        if result:
            temperature = result[0].get('value', [None, None])[1]
            return float(temperature) if temperature is not None else None
        return None

    # Get the current temperature readings
    temp_ambient = get_temperature('temperature_ambient')
    temp_cold = get_temperature('temperature_cold')
    temp_hot = get_temperature('temperature_hot')

    if temp_cold is None or temp_hot is None or temp_ambient is None:
        syslog.syslog(syslog.LOG_ERR, "Failed to get temperature readings")
        return

    # Load thresholds from config
    temperature_ambient = config.METRIC_THRESHOLDS.get('temperature_ambient')
    temperature_cold_min = config.METRIC_THRESHOLDS.get('temperature_cold_min')
    temperature_cold = config.METRIC_THRESHOLDS.get('temperature_cold')
    temperature_cold_warning = config.METRIC_THRESHOLDS.get('temperature_cold_warning')
    temperature_hot_warning = config.METRIC_THRESHOLDS.get('temperature_hot')
    temperature_emergency = config.METRIC_THRESHOLDS.get('temperature_emergency')  # Emergency threshold

    # If AC is currently running, check if it has run for at least MIN_AC_RUN_TIME
    if ac_running and time.time() - last_ac_activation_time < config.MIN_AC_RUN_TIME:
        # AC is still within the minimum run time, so prevent any mode switches
        syslog.syslog(syslog.LOG_INFO, "AC running, waiting for minimum runtime before evaluating further actions.")
        return

    # If the minimum run time has passed, we can switch the AC off or change modes
    if ac_running and time.time() - last_ac_activation_time >= config.MIN_AC_RUN_TIME:
        # AC has completed the minimum runtime, allow switching modes
        ac_running = False  # Reset AC state so it can be switched if necessary

    # Emergency condition: if temperature exceeds emergency threshold
    if temp_hot > temperature_emergency:
        # Emergency mode: Trigger emergency cooling actions
        actions.emergency(temp_hot)
        syslog.syslog(syslog.LOG_CRIT, f"Emergency Mode: Hot Aisle Temperature ({temp_hot}°C) exceeds Emergency Threshold")
        return

    # Evaluate other conditions based on temperature readings
    if temp_hot > temperature_hot_warning or temp_ambient > temperature_ambient:
        # AC mode: Hot aisle or Ambient temperature above the threshold, turn on AC
        if not ac_running:
            last_ac_activation_time = time.time()
            ac_running = True
            actions.ac_on(temp_hot if temp_hot > temperature_hot_warning else temp_ambient)
            syslog.syslog(syslog.LOG_INFO, f"Room in AC Mode: Temperature exceeds threshold")
        return

    if temp_cold < temperature_cold_min:
        # Passive cooling mode
        actions.passive_cooling(temp_cold)
        syslog.syslog(syslog.LOG_INFO, f"Room in Passive Cooling Mode: Cold Aisle Temperature ({temp_cold}°C) is below Minimum")
    elif temperature_cold_min <= temp_cold < temperature_cold:
        # Free cooling mode
        actions.freecooling(temp_cold)
        syslog.syslog(syslog.LOG_INFO, f"Room in Free Cooling Mode: Cold Aisle Temperature ({temp_cold}°C) is between Min and Normal")
    elif temperature_cold <= temp_cold < temperature_cold_warning:
        # Freecooling turbo mode
        actions.freecooling_turbo(temp_cold)
        syslog.syslog(syslog.LOG_INFO, f"Room in Freecooling Turbo Mode: Cold Aisle Temperature ({temp_cold}°C) is between Normal and Warning")
    else:
        # AC mode: Cold aisle temperature exceeds warning threshold
        if not ac_running:
            last_ac_activation_time = time.time()
            ac_running = True
            actions.ac_on(temp_cold)
            syslog.syslog(syslog.LOG_INFO, f"Room in AC Mode: Cold Aisle Temperature ({temp_cold}°C) is above Warning")

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
