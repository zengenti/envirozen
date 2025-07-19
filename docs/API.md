# Envirozen API Documentation

## Overview

Envirozen provides several interfaces for monitoring and controlling the environmental system:

1. **Web Interface** - Flask-based web UI for manual control
2. **Sensor Endpoints** - Prometheus metrics from Pico W sensors
3. **Prometheus API** - Time-series data storage and retrieval
4. **System Control** - GPIO-based hardware control

## Web Interface API

The Flask web server provides a simple interface for manual control and monitoring.

### Base URL
```
http://your-controller-ip:5000
```

### Endpoints

#### GET /
**Description**: Main dashboard displaying current system status

**Response**: HTML page with:
- Current temperature readings from all sensors
- GPIO pin states (fans, AC, damper)
- Embedded Grafana dashboard
- Manual control links

**Example Response Elements**:
```html
<p>Hot Aisle: 28.5°C</p>
<p>Cold Aisle: 22.1°C</p>
<p>AC - State: <i class="fas fa-circle" style="color: red"></i> Off</p>
```

#### GET /ac
**Description**: Activate AC cooling mode

**Actions**:
- Closes damper
- Turns off both fans
- Turns on AC unit
- Sets system to manual mode

**Response**: Redirects to main dashboard

#### GET /freecooling
**Description**: Activate free cooling mode

**Actions**:
- Opens damper
- Turns on Fan 1
- Turns off Fan 2
- Turns off AC

**Response**: Redirects to main dashboard

#### GET /freecooling_turbo
**Description**: Activate turbo free cooling mode

**Actions**:
- Opens damper
- Turns on both fans
- Turns off AC

**Response**: Redirects to main dashboard

#### GET /passive
**Description**: Activate passive cooling mode

**Actions**:
- Opens damper
- Turns off both fans
- Turns off AC

**Response**: Redirects to main dashboard

#### GET /emergency
**Description**: Activate emergency cooling mode

**Actions**:
- Opens damper
- Turns on both fans
- Turns on AC

**Response**: Redirects to main dashboard

#### GET /auto
**Description**: Return to automatic mode

**Actions**:
- Sets status file to 'automatic'
- Resumes automated decision making

**Response**: Redirects to main dashboard

## Sensor API

Each Pico W sensor exposes a Prometheus-compatible metrics endpoint.

### Base URL
```
http://sensor-ip:80
```

### Endpoints

#### GET /metrics
**Description**: Prometheus-formatted sensor metrics

**Response Format**: Plain text Prometheus metrics

**Example Response**:
```
# HELP Temperature recorded in celcius
# TYPE temperature gauge
temperature{location="ambient"} 25.4

# HELP Humidity recorded in percent  
# TYPE humidity gauge
humidity{location="ambient"} 65.2

# HELP Air pressure recorded in hectopascals hPA
# TYPE pressure gauge
pressure{location="ambient"} 1013.25

# Luminance recorded as lux
# TYPE luminance gauge
luminance{location="ambient"} 450.7

# Color temperature recorded in kelvin
# TYPE color_temperature gauge
color_temperature{location="ambient"} 5600
```

**Sensor Locations**:
- `ambient` - Outdoor/ambient air sensor
- `cold` - Cold aisle sensor  
- `hot` - Hot aisle sensor
- `floor` - Under-floor sensor

## Prometheus API

Envirozen queries Prometheus for sensor data. These are standard Prometheus API endpoints.

### Base URL
```
http://prometheus-ip:9090
```

### Key Queries Used

#### Temperature Queries
```
# Ambient temperature
temperature{location="ambient"}

# Cold aisle temperature  
temperature{location="cold"}

# Hot aisle temperature
temperature{location="hot"}

# Under-floor temperature
temperature{location="floor"}
```

#### Example API Call
```bash
curl 'http://prometheus-ip:9090/api/v1/query?query=temperature{location="cold"}'
```

**Response Format**:
```json
{
  "status": "success",
  "data": {
    "resultType": "vector",
    "result": [
      {
        "metric": {
          "__name__": "temperature",
          "location": "cold"
        },
        "value": [1640995200, "22.5"]
      }
    ]
  }
}
```

## GPIO Control Interface

Hardware control is managed through GPIO pins. This is internal to the system but documented for reference.

### Pin Mappings

| Device | GPIO Pin | WiringPi Pin | Function |
|--------|----------|--------------|----------|
| Fan 1 | 22 | 3 | Primary circulation fan |
| Fan 2 | 26 | 25 | Secondary circulation fan |
| AC Unit | 6 | 22 | Air conditioning control |
| Damper | 4 | 7 | External air damper |

### GPIO States

#### Fan Control
- `HIGH` (1) = Fan ON
- `LOW` (0) = Fan OFF

#### AC Control  
- `LOW` (0) = AC ON (inverted for fail-safe)
- `HIGH` (1) = AC OFF

#### Damper Control
- `HIGH` (1) = Damper OPEN
- `LOW` (0) = Damper CLOSED

## Configuration API

System configuration is managed through the `config.py` file.

### Temperature Thresholds

```python
METRIC_THRESHOLDS = {
    'temperature_ambient': 25,      # Max ambient temperature for free cooling
    'temperature_floor': 20,        # Max under-floor temperature  
    'temperature_hot': 31,          # Max hot aisle before AC required
    'temperature_emergency': 36,    # Emergency threshold
    'temperature_cold': 20,         # Target cold aisle temperature
    'temperature_cold_warning': 25, # Cold aisle warning threshold
    'temperature_cold_min': 10,     # Minimum cold aisle temperature
}
```

### Timing Configuration

```python
evaluation_interval = 10    # Seconds between evaluations
MIN_AC_RUN_TIME = 300      # Minimum AC runtime (seconds)
```

### Prometheus Configuration

```python
PROMETHEUS_URL = 'http://10.128.83.10:9090'
```

## Status File Interface

The system uses a simple file-based status tracking mechanism.

### Status File Location
```
envirozen/controller/status.txt
```

### Valid Status Values
- `automatic` - System operates in automatic mode
- `manual` - System in manual control mode

### Reading Status
```bash
cat status.txt
```

### Setting Status
```bash
echo "automatic" > status.txt
echo "manual" > status.txt
```

## Logging Interface

System logging is handled through Python's syslog module.

### Log Levels Used
- `LOG_INFO` - Normal operational messages
- `LOG_ERR` - Error conditions
- `LOG_CRIT` - Critical/emergency conditions

### Example Log Messages
```
envirozen: Room in Free Cooling Mode: Cold Aisle Temperature (18.5°C) is between Min and Normal
envirozen: Room in AC Mode: Temperature exceeds threshold  
envirozen: Emergency Mode: Hot Aisle Temperature (37.2°C) exceeds Emergency Threshold
```

### Viewing Logs
```bash
# System logs
sudo tail -f /var/log/syslog | grep envirozen

# Service logs  
sudo journalctl -u envirozen -f
```

## Error Handling

### Common Error Responses

#### Sensor Connection Errors
- **Symptom**: Temperature readings show as "N/A"
- **Cause**: Network connectivity or sensor failure
- **Resolution**: Check network connectivity and sensor status

#### GPIO Control Errors
- **Symptom**: Hardware doesn't respond to commands
- **Cause**: GPIO permission or hardware issues
- **Resolution**: Verify GPIO permissions and wiring

#### Prometheus Query Errors
- **Symptom**: System logs show query failures
- **Cause**: Prometheus server unavailable or query issues
- **Resolution**: Verify Prometheus connectivity and sensor data

### Error Logging
All errors are logged to syslog with appropriate severity levels. Monitor logs for troubleshooting.

## Security Considerations

### Authentication
- No authentication is currently implemented
- System should be deployed on isolated network
- Consider adding basic authentication for production use

### Access Control
- Web interface accessible to anyone on network
- GPIO control requires system-level access
- Sensor endpoints are read-only

### Network Security
- All communication is unencrypted HTTP
- Suitable for isolated internal networks
- Consider HTTPS for external access

## Rate Limiting

### Evaluation Frequency
- Main control loop runs every 10 seconds (configurable)
- Web interface has no rate limiting
- Sensor metrics updated continuously

### AC Control Protection
- Minimum 5-minute runtime prevents rapid cycling
- Protects AC equipment from damage
- Configurable via `MIN_AC_RUN_TIME`

## Monitoring and Metrics

### Key Performance Indicators
- Temperature differential across aisles
- System mode transitions
- AC runtime vs. free cooling time
- Power consumption (if monitored)

### Alerting Recommendations
Set up Grafana alerts for:
- Temperature exceeding emergency thresholds
- Sensor connectivity failures
- Excessive AC usage
- System mode stuck in emergency