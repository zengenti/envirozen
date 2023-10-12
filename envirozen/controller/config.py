
PROMETHEUS_URL = 'http://192.168.88.72:9090'
METRIC_THRESHOLDS = {
    'temperature_ambient': 30,  # Max Ambient outdoor temperature
    'temperature_floor': 30,  # Max Under floor temperature
    'temperature_hot': 30,  # Max Hot Aisle temperature
    'temperature_cold': 30  # Max Cold Aisle temperature
}
QUERIES = {
    'temperature_ambient': 'temperature{location="ambient"}',
    'temperature_floor': 'temperature{location="floor"}',
    'temperature_hot': 'temperature{location="hot"}',
    'temperature_cold': 'temperature{location="cold"}'
}
