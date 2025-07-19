# Envirozen

*Intelligent Environmental Monitoring and Control System for Server Room Cooling*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi-red.svg)](https://www.raspberrypi.org/)

## Overview

Envirozen is an intelligent environmental monitoring and control system designed to optimize server room cooling while minimizing energy consumption. The system automatically switches between different cooling modes based on real-time temperature readings from multiple sensors, prioritizing ambient air cooling when possible to reduce reliance on expensive air conditioning.

### Key Features

- **Automatic Cooling Mode Selection**: Intelligently switches between passive, free cooling, turbo, and AC modes
- **Multi-Sensor Monitoring**: Monitors ambient, cold aisle, hot aisle, and under-floor temperatures
- **Energy Optimization**: Prioritizes ambient air cooling to reduce energy costs
- **Emergency Protection**: Automatic emergency mode for critical temperature conditions
- **Web Interface**: Real-time monitoring and manual control via web dashboard
- **Historical Data**: Integration with Prometheus and Grafana for long-term analysis
- **Fail-Safe Design**: Designed to default to safe cooling mode in case of system failure

### Project History

**Started**: October 2022  
**Motivation**: Rising electricity costs and environmental concerns  
**Evolution**: Originally Arduino-based, evolved to Python on Raspberry Pi for enhanced capabilities  
**Author**: Nic Kilby

## System Components

### Hardware Requirements

| Component | Quantity | Purpose |
|-----------|----------|---------|
| [Raspberry Pi 4][1] | 1 | Central controller |
| [Enviro Indoor (Pico W)][2] | 4+ | Environmental sensors for each monitoring zone |
| [Weatherproof Enclosures][9] | As needed | Outdoor sensor protection |
| [1.5kW Fans][3] | 2 | Air circulation |
| [TUNE-S-600x600-M1 Damper][4] | 1 | Mechanical damper with M1 actuator |

### System Architecture

![System Flow Diagram](docs/images/freeair.webp)

The system creates positive pressure by introducing external ambient air when temperature conditions are favorable, expelling warmer air through specialized vents while minimizing AC usage.


## Quick Start

### 📋 Prerequisites
- Raspberry Pi 4 with Ubuntu 22.04 Server
- Python 3.8+
- Network connectivity for all components

### 🚀 Installation

**For detailed installation instructions, see [docs/INSTALLATION.md](docs/INSTALLATION.md)**

```bash
# Clone repository
git clone https://github.com/your-org/envirozen.git
cd envirozen

# Install dependencies
cd envirozen/controller
pip install -r requirements.txt

# Configure system
cp config.py.example config.py
nano config.py  # Update with your settings

# Start services
sudo systemctl enable envirozen
sudo systemctl start envirozen
```

### 🌐 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| **Main Dashboard** | `http://your-pi:5000` | Control interface and real-time status |
| **Grafana** | `http://your-pi:3000` | Historical data and analytics |
| **Prometheus** | `http://your-pi:9090` | Metrics storage (optional access) |
| **Sensor Metrics** | `http://sensor-ip/metrics` | Individual sensor data |

### 🔧 Configuration

#### Sensor Setup
Update each Pico W sensor with your network credentials:

```python
# In envirozen/sensors/main.py
ssid = 'YOUR_WIFI_NETWORK'
password = 'YOUR_WIFI_PASSWORD'  
location = 'SENSOR_LOCATION'  # 'ambient', 'cold', 'hot', 'floor'
```

#### Temperature Thresholds
Customize in `config.py`:

```python
METRIC_THRESHOLDS = {
    'temperature_ambient': 25,      # Max ambient for free cooling
    'temperature_cold': 20,         # Target cold aisle temp
    'temperature_hot': 31,          # Max hot aisle before AC
    'temperature_emergency': 36,    # Emergency threshold
}
```

## How It Works

### Cooling Modes

| Mode | Trigger | Fans | Damper | AC | Purpose |
|------|---------|------|--------|----|---------|
| **Passive** | Cold < 10°C | OFF | Open | OFF | Natural circulation |
| **Free Cooling** | Cold 10-20°C | Fan 1 ON | Open | OFF | Basic air circulation |
| **Turbo** | Cold 20-25°C | Both ON | Open | OFF | Maximum air circulation |
| **AC Mode** | Hot > 31°C or Cold > 25°C | OFF | Closed | ON | Mechanical cooling |
| **Emergency** | Hot > 36°C | Both ON | Open | ON | Maximum cooling |

### System Operation

1. **Continuous Monitoring**: Sensors collect temperature, humidity, and pressure data every few seconds
2. **Data Storage**: Prometheus stores all metrics for historical analysis
3. **Intelligent Control**: Main controller evaluates conditions every 10 seconds
4. **Automatic Switching**: System selects optimal cooling mode based on current conditions
5. **Manual Override**: Web interface allows manual control when needed
6. **Emergency Response**: Automatic emergency cooling when critical thresholds exceeded

## Documentation

- 📖 [Installation Guide](docs/INSTALLATION.md) - Step-by-step setup instructions
- 🏗️ [System Architecture](docs/ARCHITECTURE.md) - Detailed system design and components  
- 🔌 [API Documentation](docs/API.md) - Interface specifications and endpoints
- 🛠️ [Troubleshooting Guide](docs/TROUBLESHOOTING.md) - Common issues and solutions

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on:
- Code style and standards
- Testing requirements  
- Pull request process
- Issue reporting

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/your-org/envirozen/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/your-org/envirozen/discussions)
- 📧 **Email**: support@yourorg.com

## Acknowledgments

- Original concept and development by Nic Kilby
- Inspired by rising energy costs and environmental concerns
- Thanks to the Raspberry Pi and MicroPython communities

---

**⚡ Energy Efficient • 🌡️ Temperature Controlled • 🔧 Open Source**

[1]: https://www.raspberrypi.com/products/raspberry-pi-4-model-b/
[2]: https://shop.pimoroni.com/products/enviro-indoor?variant=40055644717139
[3]: https://www.plugandcool.co.uk/product/1-5-grain-store-fan/
[4]: https://www.puravent.co.uk/tune-s-600x600-m1.html
[9]: https://shop.pimoroni.com/products/weatherproof-cover-for-outdoor-sensors?variant=40047884468307
