# Envirozen Installation Guide

## Prerequisites

### Hardware Requirements
- Raspberry Pi 4 (4GB RAM minimum recommended)
- MicroSD card (32GB minimum, Class 10)
- Enviro Indoor (Pico W) sensors (one per monitoring location)
- 2x 1.5kW fans for air circulation
- TUNE-S-600x600-M1 mechanical damper with M1 actuator
- Relay modules for AC control
- Weatherproof enclosures for outdoor sensors
- Network connectivity (WiFi or Ethernet)

### Software Requirements
- Ubuntu Server 22.04 LTS (recommended)
- Python 3.8+
- Internet connection for initial setup

## Installation Process

### 1. Raspberry Pi Setup

#### 1.1 Flash Ubuntu Server
1. Download [Ubuntu 22.04 Server for Raspberry Pi](https://ubuntu.com/download/raspberry-pi)
2. Flash to microSD card using [Raspberry Pi Imager](https://www.raspberrypi.com/software/)
3. Boot the Pi and complete initial setup

#### 1.2 Update System
```bash
sudo apt update && sudo apt upgrade -y
sudo reboot
```

#### 1.3 Install Required Packages
```bash
# Install NTP for time synchronization
sudo apt install ntp git python3-pip python3-venv -y

# Configure NTP
sudo nano /etc/ntp.conf
# Add your preferred NTP servers

# Restart NTP service
sudo systemctl restart ntp
sudo systemctl enable ntp
```

### 2. Monitoring Stack Setup

#### 2.1 Install Prometheus
```bash
# Install Prometheus using snap
sudo snap install prometheus

# Check installation
sudo snap services prometheus

# Prometheus will be available at http://your-pi-ip:9090
```

#### 2.2 Configure Prometheus
```bash
# Copy the provided prometheus.yml configuration
sudo cp envirozen/prometheus.yml /var/snap/prometheus/current/

# Update the configuration with your sensor IP addresses
sudo nano /var/snap/prometheus/current/prometheus.yml

# Restart Prometheus
sudo snap restart prometheus.prometheus
```

#### 2.3 Install Grafana
```bash
# Add Grafana repository
sudo apt-get install -y software-properties-common
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -

# Install Grafana
sudo apt-get update
sudo apt-get install grafana

# Enable and start Grafana
sudo systemctl enable grafana-server
sudo systemctl start grafana-server

# Grafana will be available at http://your-pi-ip:3000
# Default login: admin/admin
```

### 3. Sensor Setup (Pico W)

#### 3.1 Backup Original Firmware
Before modifying any Pico W sensors, backup the original `main.py`:
```bash
# Connect Pico W to computer
# Use Thonny or similar MicroPython IDE to backup main.py
```

#### 3.2 Deploy Sensor Code
1. Copy the sensor files to each Pico W:
   - `envirozen/sensors/main.py`
   - `envirozen/sensors/sensor_readings.py`

2. Update sensor configuration in `main.py`:
```python
# Update these values for each sensor
ssid = 'YOUR_WIFI_NETWORK'
password = 'YOUR_WIFI_PASSWORD'
location = 'SENSOR_LOCATION'  # e.g., 'ambient', 'cold', 'hot', 'floor'
```

#### 3.3 Test Sensor Connectivity
After deploying, verify each sensor is accessible:
```bash
# Test sensor endpoint
curl http://SENSOR_IP/metrics

# You should see Prometheus-formatted metrics
```

### 4. Envirozen Controller Setup

#### 4.1 Clone Repository
```bash
cd /opt
sudo git clone https://github.com/your-org/envirozen.git
sudo chown -R $USER:$USER envirozen
cd envirozen
```

#### 4.2 Create Virtual Environment
```bash
cd envirozen/controller
python3 -m venv venv
source venv/bin/activate
```

#### 4.3 Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 4.4 Configure Application
```bash
# Copy and edit configuration
cp config.py config.py.backup
nano config.py
```

Update the following in `config.py`:
- `PROMETHEUS_URL`: Your Prometheus server URL
- `METRIC_THRESHOLDS`: Adjust temperature thresholds for your environment
- `evaluation_interval`: How often to check conditions

#### 4.5 Hardware Wiring

Connect GPIO pins as defined in `actions.py`:
- Fan 1: GPIO 22 (WiringPi pin 3)
- Fan 2: GPIO 26 (WiringPi pin 25)
- AC Control: GPIO 6 (WiringPi pin 22)
- Damper Control: GPIO 4 (WiringPi pin 7)

**IMPORTANT**: Ensure proper relay modules and electrical safety measures are in place.

#### 4.6 Test Installation
```bash
# Test the application manually
python3 envirozen.py

# Check web interface at http://your-pi-ip:5000
```

### 5. System Service Setup

#### 5.1 Create Service File
```bash
sudo cp envirozen.service /etc/systemd/system/
sudo nano /etc/systemd/system/envirozen.service
```

Update paths in the service file:
```ini
[Unit]
Description=Envirozen Environmental Control
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/opt/envirozen/envirozen/controller
ExecStart=/opt/envirozen/envirozen/controller/venv/bin/python envirozen.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 5.2 Enable Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable envirozen
sudo systemctl start envirozen

# Check service status
sudo systemctl status envirozen
```

### 6. Final Configuration

#### 6.1 Configure Grafana Dashboards
1. Login to Grafana (http://your-pi-ip:3000)
2. Add Prometheus as data source (http://localhost:9090)
3. Import or create dashboards for:
   - Temperature monitoring
   - System status
   - Historical trends

#### 6.2 Network Configuration
Update your router/firewall to allow access to:
- Grafana: Port 3000
- Envirozen Web UI: Port 5000
- Prometheus (optional): Port 9090

#### 6.3 Backup Configuration
```bash
# Create backup of working configuration
sudo tar -czf envirozen-backup-$(date +%Y%m%d).tar.gz \
  /opt/envirozen \
  /etc/systemd/system/envirozen.service \
  /var/snap/prometheus/current/prometheus.yml
```

## Verification

### Test All Components
1. **Sensors**: Verify all sensors report data to Prometheus
2. **Control**: Test manual control modes via web interface
3. **Automation**: Monitor automatic mode transitions
4. **Logging**: Check system logs for proper operation

```bash
# Check Envirozen logs
sudo journalctl -u envirozen -f

# Check system logs
sudo tail -f /var/log/syslog | grep envirozen
```

### Performance Monitoring
- Monitor CPU and memory usage
- Check network connectivity to sensors
- Verify GPIO control operations
- Monitor temperature thresholds and responses

## Troubleshooting

### Common Issues

#### Sensor Connection Problems
```bash
# Test network connectivity
ping SENSOR_IP

# Check sensor metrics endpoint
curl http://SENSOR_IP/metrics
```

#### GPIO Control Issues
```bash
# Check GPIO permissions
sudo usermod -a -G gpio $USER

# Test GPIO manually
python3 -c "import RPi.GPIO as GPIO; GPIO.setmode(GPIO.BCM); GPIO.setup(22, GPIO.OUT); GPIO.output(22, GPIO.HIGH)"
```

#### Service Startup Problems
```bash
# Check service logs
sudo journalctl -u envirozen --no-pager

# Check Python path and dependencies
cd /opt/envirozen/envirozen/controller
source venv/bin/activate
python3 -c "import actions, config, prometheus"
```

### Support

For additional support:
1. Check system logs: `sudo journalctl -u envirozen`
2. Verify hardware connections
3. Test individual components separately
4. Review configuration files for typos
5. Ensure all dependencies are installed

## Security Considerations

1. **Network Isolation**: Run on isolated VLAN if possible
2. **Access Control**: Limit web interface access to authorized users
3. **Regular Updates**: Keep system and dependencies updated
4. **Backup**: Regular configuration backups
5. **Monitoring**: Monitor for unauthorized access attempts