# Define the time interval (in seconds) between metric evaluations
evaluation_interval = 10  # Reevaluation period in seconds
MIN_AC_RUN_TIME = 300 # For example, 5 minutes

PROMETHEUS_URL = 'http://10.128.83.10:9090' 
# PROMETHEUS_URL = 'http://192.168.88.88:9090' # Testing URL

METRIC_THRESHOLDS = {
    'temperature_ambient': 25,  # Max Ambient outdoor temperature
    'temperature_floor': 20,  # Max Under floor temperature
    'temperature_hot': 31,  # Max Hot Aisle temperature
    'temperature_emergency': 36,  # Emergency Hot Aisle temperature
    'temperature_cold':20,  # Max Cold Aisle temperature
    'temperature_cold_warning': 25,  # Warming Cold Aisle temperature
    'temperature_cold_min': 10,  # Minimum Cold Aisle temperature
}
QUERIES = {
    'temperature_ambient': 'temperature{location="ambient"}',
    'temperature_floor': 'temperature{location="floor"}',
    'temperature_hot': 'temperature{location="hot"}',
    'temperature_emergency': 'temperature{location="hot"}',
    'temperature_cold': 'temperature{location="cold"}',
    'temperature_cold_warning': 'temperature{location="cold"}',
    'temperature_cold_min': 'temperature{location="cold"}'
}
