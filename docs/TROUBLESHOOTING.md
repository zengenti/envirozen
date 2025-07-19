# Envirozen Troubleshooting Guide

## Quick Diagnostics

### System Status Check
```bash
# Check service status
sudo systemctl status envirozen

# Check recent logs
sudo journalctl -u envirozen --since "1 hour ago"

# Check system resources
htop
df -h
```

### Network Connectivity Test
```bash
# Test sensor connectivity
ping SENSOR_IP

# Test Prometheus connectivity  
curl http://prometheus-ip:9090/api/v1/query?query=up

# Test sensor metrics
curl http://sensor-ip/metrics
```

## Common Issues

### 1. Service Won't Start

#### Symptoms
- `sudo systemctl status envirozen` shows "failed"
- Error messages in systemctl output

#### Possible Causes & Solutions

**Python Import Errors**
```bash
# Check Python path and dependencies
cd /opt/envirozen/envirozen/controller
source venv/bin/activate
python3 -c "import actions, config, prometheus, RPi.GPIO"
```

**Permission Issues**
```bash
# Add user to GPIO group
sudo usermod -a -G gpio $USER

# Check file permissions
sudo chown -R pi:pi /opt/envirozen
chmod +x envirozen.py
```

**Configuration Errors**
```bash
# Validate config.py syntax
python3 -c "import config; print('Config loaded successfully')"

# Check for missing files
ls -la status.txt config.py requirements.txt
```

### 2. GPIO Control Not Working

#### Symptoms
- Web interface shows wrong pin states
- Hardware doesn't respond to commands
- GPIO errors in logs

#### Solutions

**Check GPIO Permissions**
```bash
# Verify user is in gpio group
groups $USER

# Test GPIO manually
python3 << EOF
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.HIGH)
print("Fan 1 should be ON")
GPIO.cleanup()
EOF
```

**Hardware Verification**
```bash
# Check GPIO pin status
gpio readall

# Test with simple LED
# Connect LED to GPIO 22 and test
```

**Wiring Issues**
- Verify all connections match pin definitions in `actions.py`
- Check for loose connections
- Ensure proper relay module wiring
- Verify power supply to relays

### 3. Sensor Connection Problems

#### Symptoms
- Temperature readings show "N/A"
- Sensors not appearing in Prometheus
- Network timeouts

#### Solutions

**Network Connectivity**
```bash
# Check sensor network
nmap -sP 192.168.1.0/24 | grep "Raspberry\|Pico"

# Test specific sensor
curl -v http://SENSOR_IP/metrics
```

**Sensor Configuration**
- Verify WiFi credentials in `main.py`
- Check network DHCP settings
- Ensure sensors are on same network as controller

**Prometheus Configuration**
```bash
# Check Prometheus targets
curl http://prometheus-ip:9090/api/v1/targets

# Validate prometheus.yml
sudo nano /var/snap/prometheus/current/prometheus.yml
```

### 4. Temperature Reading Issues

#### Symptoms
- Inconsistent temperature readings
- Sensors reporting extreme values
- Missing data points

#### Solutions

**Sensor Calibration**
```python
# Check sensor readings directly
curl http://sensor-ip/metrics | grep temperature

# Compare multiple sensors
for ip in 192.168.1.{10,11,12,13}; do
    echo "Sensor $ip:"
    curl -s http://$ip/metrics | grep temperature
done
```

**Data Validation**
```bash
# Check Prometheus data retention
curl 'http://prometheus-ip:9090/api/v1/query?query=temperature'

# Verify scrape intervals
curl http://prometheus-ip:9090/api/v1/targets
```

### 5. Web Interface Problems

#### Symptoms
- Web interface not accessible
- Page shows error 500
- Missing data in dashboard

#### Solutions

**Flask Service Issues**
```bash
# Check if Flask is running
netstat -tlnp | grep :5000

# Check Flask logs
sudo journalctl -u envirozen | grep Flask

# Test Flask manually
cd /opt/envirozen/envirozen/controller
python3 server.py
```

**Template Issues**
```bash
# Verify template files exist
ls -la templates/
cat templates/server.html
```

**Data Issues**
```bash
# Test Prometheus queries manually
curl 'http://prometheus-ip:9090/api/v1/query?query=temperature{location="cold"}'
```

### 6. System Performance Issues

#### Symptoms
- High CPU usage
- Memory leaks
- Slow response times

#### Solutions

**Resource Monitoring**
```bash
# Monitor system resources
top -p $(pidof python3)

# Check memory usage
free -h
cat /proc/meminfo

# Monitor disk space
df -h
du -sh /opt/envirozen
```

**Performance Optimization**
```bash
# Adjust evaluation interval in config.py
evaluation_interval = 30  # Increase from 10 seconds

# Check for memory leaks
sudo journalctl -u envirozen | grep -i memory
```

## Hardware-Specific Issues

### AC Control Problems

#### Relay Not Switching
- Check relay power supply (usually 5V or 12V)
- Verify relay coil ratings match GPIO output
- Test relay manually with multimeter
- Check AC control wiring to HVAC system

#### AC Not Responding
- Verify HVAC system compatibility
- Check electrical connections
- Ensure proper grounding
- Verify control voltage requirements

### Fan Control Issues

#### Fans Not Starting
- Check fan power supply
- Verify relay ratings for fan current
- Test fan operation directly
- Check for mechanical obstructions

#### Inconsistent Fan Operation  
- Verify relay contact ratings
- Check for voltage drop under load
- Ensure adequate power supply capacity

### Damper Control Problems

#### Damper Not Moving
- Check actuator power supply
- Verify control signal requirements
- Test actuator manually
- Check for mechanical binding

#### Partial Movement
- Verify actuator torque ratings
- Check control signal voltage
- Ensure proper mounting

## Environmental Issues

### Sensor Accuracy Problems

#### Temperature Drift
- Check sensor placement away from heat sources
- Verify adequate ventilation around sensors
- Consider sensor aging and calibration
- Compare readings with reference thermometer

#### Humidity Issues
- Ensure sensors are not in direct airflow
- Check for condensation on sensors
- Verify sensor specifications for environment

### System Response Issues

#### Slow Response to Temperature Changes
- Check evaluation interval setting
- Verify sensor response times
- Review cooling mode thresholds
- Consider thermal mass of room

#### Oscillating Between Modes
- Increase hysteresis in temperature thresholds
- Extend minimum AC runtime
- Review threshold spacing

## Network and Connectivity

### WiFi Issues

#### Sensors Disconnecting
```bash
# Check WiFi signal strength
iwconfig wlan0

# Monitor WiFi stability
ping -c 100 SENSOR_IP

# Check for interference
iwlist scan | grep ESSID
```

#### Poor Signal Quality
- Relocate WiFi access point or sensors
- Use WiFi extenders if needed
- Consider 2.4GHz vs 5GHz frequency

### Prometheus Issues

#### Data Not Persisting
```bash
# Check Prometheus storage
sudo ls -la /var/snap/prometheus/common/

# Verify disk space
df -h /var/snap/prometheus

# Check Prometheus logs
sudo snap logs prometheus.prometheus
```

#### Query Performance
- Reduce retention period if needed
- Optimize query patterns
- Consider Prometheus resource limits

## Emergency Procedures

### System Failure Response

#### Complete System Failure
1. **Immediate Action**: Ensure AC system defaults to ON
2. **Manual Control**: Use physical switches if available
3. **Emergency Contact**: Alert facility management
4. **Restoration**: Follow recovery procedures

#### Partial System Failure
1. **Identify Failed Components**: Check logs and status
2. **Manual Override**: Use web interface to force safe mode
3. **Isolate Issues**: Disable problematic sensors/controls
4. **Monitor Manually**: Watch temperatures directly

### Recovery Procedures

#### Service Recovery
```bash
# Stop service
sudo systemctl stop envirozen

# Reset GPIO states
python3 << EOF
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
EOF

# Restart service
sudo systemctl start envirozen
```

#### Complete System Reset
```bash
# Reset to defaults
cd /opt/envirozen/envirozen/controller
echo "automatic" > status.txt

# Clear any locks
rm -f *.lock *.pid

# Restart all services
sudo systemctl restart envirozen
sudo snap restart prometheus.prometheus
sudo systemctl restart grafana-server
```

## Prevention and Monitoring

### Regular Maintenance

#### Daily Checks
- Verify all sensors are online
- Check system logs for errors  
- Monitor temperature trends
- Verify cooling mode transitions

#### Weekly Maintenance
```bash
# Update system
sudo apt update && sudo apt upgrade

# Check disk space
df -h

# Backup configuration
tar -czf backup-$(date +%Y%m%d).tar.gz /opt/envirozen
```

#### Monthly Tasks
- Clean sensors and equipment
- Verify calibration
- Test emergency procedures
- Review and update thresholds

### Monitoring Setup

#### Alerting Rules
Set up Grafana alerts for:
- Temperature exceeding emergency thresholds
- Sensor connectivity failures
- System mode stuck in emergency
- High AC usage indicating efficiency problems

#### Log Monitoring
```bash
# Set up log rotation
sudo logrotate -f /etc/logrotate.conf

# Monitor for error patterns
sudo tail -f /var/log/syslog | grep -E "ERROR|CRITICAL|envirozen"
```

## Getting Help

### Information to Collect

Before seeking help, gather:
```bash
# System information
uname -a
lsb_release -a

# Service status
sudo systemctl status envirozen
sudo journalctl -u envirozen --since "1 day ago" > envirozen.log

# Configuration
cp config.py config-debug.py
# Remove sensitive information before sharing

# Network status
ip addr show
netstat -tlnp | grep -E ":5000|:9090|:3000"
```

### Support Channels
- GitHub Issues: Technical problems and bugs
- GitHub Discussions: General questions and ideas  
- Documentation: Check all docs/ files first
- Community: Ask in relevant forums with full details

### Escalation Process
1. **Self-Service**: Check this troubleshooting guide
2. **Documentation**: Review all documentation files
3. **Community**: Post in discussions with details
4. **Issues**: Create GitHub issue for bugs
5. **Emergency**: Contact facility management for critical issues