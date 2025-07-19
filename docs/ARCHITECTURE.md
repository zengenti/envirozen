# Envirozen System Architecture

## Overview

Envirozen is an intelligent environmental monitoring and control system designed for server room cooling optimization. The system automatically switches between different cooling modes based on temperature readings from multiple sensors, prioritizing energy efficiency by using ambient air cooling when possible.

## System Components

### 1. Hardware Components

#### Sensors
- **Enviro Indoor (Pico W)** - Environmental sensors for temperature, humidity, pressure, and light monitoring
- **Multiple sensor locations**: ambient, cold aisle, hot aisle, under floor
- **Weatherproof enclosures** for outdoor sensors

#### Control Hardware
- **Raspberry Pi 4** - Central controller running the main application
- **GPIO-controlled devices**:
  - 2x 1.5Kw fans for air circulation
  - TUNE-S-600x600-M1 mechanical damper with M1 actuator
  - AC unit control relay
  - Status indicators

#### Network Infrastructure
- **Prometheus** - Metrics collection and storage
- **Grafana** - Visualization and dashboards
- **Flask web server** - Manual control interface

### 2. Software Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Envirozen Controller                     │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   Web UI    │  │ Main Loop   │  │   GPIO Control      │  │
│  │ (Flask)     │  │ (envirozen) │  │   (actions)         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                           │                    │             │
│  ┌─────────────────────────┼────────────────────┼───────────┐ │
│  │         Data Layer      │                    │           │ │
│  │  ┌─────────────┐       │       ┌─────────────────────┐  │ │
│  │  │ Prometheus  │ ◄─────┘       │    Configuration    │  │ │
│  │  │   Client    │               │     (config.py)     │  │ │
│  │  └─────────────┘               └─────────────────────┘  │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
            │                                    ▲
            ▼                                    │
┌─────────────────────┐                 ┌──────────────────┐
│   Prometheus        │                 │   Sensor Network │
│   ┌─────────────┐   │                 │  ┌─────────────┐ │
│   │  Metrics    │   │                 │  │   Pico W    │ │
│   │  Storage    │   │ ◄───────────────┼─ │  Sensors    │ │
│   └─────────────┘   │                 │  └─────────────┘ │
│   ┌─────────────┐   │                 │  ┌─────────────┐ │
│   │   Grafana   │   │                 │  │   Pico W    │ │
│   │ Dashboards  │   │                 │  │  Sensors    │ │
│   └─────────────┘   │                 │  └─────────────┘ │
└─────────────────────┘                 └──────────────────┘
```

### 3. Cooling Modes

The system operates in several distinct modes based on temperature thresholds:

#### Passive Cooling
- **Trigger**: Cold aisle temperature < 10°C
- **Actions**: Open damper, turn off fans and AC
- **Purpose**: Natural air circulation when ambient is very cool

#### Free Cooling
- **Trigger**: Cold aisle temperature 10-20°C
- **Actions**: Open damper, turn on Fan 1, turn off Fan 2 and AC
- **Purpose**: Active air circulation using ambient air

#### Free Cooling Turbo
- **Trigger**: Cold aisle temperature 20-25°C
- **Actions**: Open damper, turn on both fans, turn off AC
- **Purpose**: Maximum air circulation before switching to AC

#### AC Mode
- **Trigger**: Hot aisle > 31°C OR Cold aisle > 25°C OR Ambient > 25°C
- **Actions**: Close damper, turn off fans, turn on AC
- **Purpose**: Mechanical cooling when ambient air insufficient

#### Emergency Mode
- **Trigger**: Hot aisle > 36°C
- **Actions**: Open damper, turn on all fans and AC
- **Purpose**: Maximum cooling when system is overheating

### 4. Data Flow

1. **Sensor Data Collection**
   - Pico W sensors collect environmental data
   - Data exposed via HTTP `/metrics` endpoint in Prometheus format
   - Prometheus scrapes sensor data at regular intervals

2. **Decision Making**
   - Main controller queries Prometheus for current readings
   - Compares readings against configured thresholds
   - Determines appropriate cooling mode

3. **Control Actions**
   - GPIO pins control physical hardware
   - Actions logged to syslog for monitoring
   - Status tracked in local file system

4. **User Interface**
   - Flask web server provides manual override capabilities
   - Real-time status display with GPIO pin states
   - Embedded Grafana dashboard for historical data

### 5. Configuration

Key configuration parameters in `config.py`:

- **Evaluation interval**: 10 seconds (how often to check conditions)
- **Minimum AC runtime**: 5 minutes (prevents rapid cycling)
- **Temperature thresholds**: Configurable for all modes
- **Prometheus URL**: Data source configuration
- **GPIO pin mappings**: Hardware interface definitions

### 6. Monitoring and Alerting

- **Metrics collection**: All temperature readings stored in Prometheus
- **Visualization**: Grafana dashboards for real-time and historical data
- **Logging**: System actions logged to syslog
- **Web interface**: Real-time status monitoring

## Security Considerations

- System runs on isolated network segment
- No external internet access required for operation
- GPIO control provides fail-safe AC operation (default AC on)
- Emergency mode provides redundant cooling capabilities

## Deployment Architecture

```
Internet ─┐
          │
          ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Monitoring    │    │    Controller    │    │     Sensors     │
│   ┌─────────┐   │    │  ┌─────────────┐ │    │ ┌─────────────┐ │
│   │Prometheus│   │    │  │ Envirozen   │ │    │ │   Pico W    │ │
│   │:9090     │   │    │  │ Flask :5000 │ │    │ │   :80       │ │
│   └─────────┘   │    │  └─────────────┘ │    │ └─────────────┘ │
│   ┌─────────┐   │    │  ┌─────────────┐ │    │ ┌─────────────┐ │
│   │ Grafana │   │◄───┼──┤   GPIO      │ │    │ │   Pico W    │ │
│   │ :3000   │   │    │  │   Control   │ │    │ │   :80       │ │
│   └─────────┘   │    │  └─────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                        │                       │
        └────────────────────────┼───────────────────────┘
                                 │
                          ┌─────────────┐
                          │  Physical   │
                          │  Hardware   │
                          │ ┌─────────┐ │
                          │ │  Fans   │ │
                          │ │ Damper  │ │
                          │ │   AC    │ │
                          │ └─────────┘ │
                          └─────────────┘
```