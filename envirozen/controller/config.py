# Define the time interval (in seconds) between metric evaluations
evaluation_interval = 10  # Reevaluation period in seconds

PROMETHEUS_URL = 'http://10.128.83.10:9090' 
PROMETHEUS_URL = 'http://192.168.88.88:9090' # Testing URL

METRIC_THRESHOLDS = {
    'temperature_ambient': 40,  # Max Ambient outdoor temperature
    'temperature_floor': 20,  # Max Under floor temperature
    'temperature_hot': 30,  # Max Hot Aisle temperature
    'temperature_cold': 20,  # Max Cold Aisle temperature
    'temperature_cold_warning': 25,  # Warming Cold Aisle temperature
    'temperature_cold_min': 5,  # Minimum Cold Aisle temperature
}
QUERIES = {
    'temperature_ambient': 'temperature{location="ambient"}',
    'temperature_floor': 'temperature{location="floor"}',
    'temperature_hot': 'temperature{location="hot"}',
    'temperature_cold': 'temperature{location="cold"}',
    'temperature_cold_warning': 'temperature{location="cold"}',
    'temperature_cold_min': 'temperature{location="cold"}'
}
