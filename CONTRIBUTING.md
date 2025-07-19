# Contributing to Envirozen

We welcome contributions to the Envirozen project! This guide will help you get started with contributing code, documentation, or bug reports.

## Quick Links

- 🐛 [Report a Bug](https://github.com/your-org/envirozen/issues/new?template=bug_report.md)
- 💡 [Request a Feature](https://github.com/your-org/envirozen/issues/new?template=feature_request.md)
- 📖 [Documentation Issues](https://github.com/your-org/envirozen/issues/new?template=documentation.md)
- 💬 [Start a Discussion](https://github.com/your-org/envirozen/discussions)

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Ways to Contribute

- **Bug Reports**: Help us identify and fix issues
- **Feature Requests**: Suggest new functionality
- **Code Contributions**: Implement features or bug fixes
- **Documentation**: Improve guides, API docs, or examples
- **Testing**: Help test new features or edge cases
- **Hardware Testing**: Test with different hardware configurations

### Before You Start

1. Check existing [issues](https://github.com/your-org/envirozen/issues) and [discussions](https://github.com/your-org/envirozen/discussions)
2. Read our [documentation](docs/) to understand the system
3. Set up your development environment
4. Start with a small contribution to get familiar with the process

## How to Contribute

### Reporting Bugs

**Before submitting a bug report:**
- Check if the issue already exists
- Test with the latest version
- Gather system information and logs

**When submitting a bug report, include:**
- Clear, descriptive title
- Steps to reproduce the issue
- Expected vs. actual behavior
- System information (OS, Python version, hardware)
- Relevant log files
- Screenshots if applicable

### Suggesting Features

**Before suggesting a feature:**
- Check if it already exists or was discussed
- Consider if it fits the project's scope
- Think about implementation complexity

**When suggesting a feature, include:**
- Clear description of the problem it solves
- Detailed description of the proposed solution
- Alternative solutions considered
- Potential impact on existing functionality

### Contributing Code

1. **Fork the repository**
2. **Create a feature branch** from `main`
3. **Make your changes** following our code standards
4. **Test your changes** thoroughly
5. **Update documentation** if needed
6. **Submit a pull request**

## Development Setup

### Prerequisites

- Raspberry Pi 4 (recommended for testing)
- Python 3.8+
- Git
- Basic electronics knowledge for hardware testing

### Local Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/envirozen.git
cd envirozen

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
cd envirozen/controller
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies

# Create development configuration
cp config.py config-dev.py
# Edit config-dev.py with your development settings
```

### Development Environment

For development without actual hardware:

```bash
# Create mock GPIO library for development
cat > mock_gpio.py << EOF
class GPIO:
    BCM = "BCM"
    OUT = "OUT"
    HIGH = True
    LOW = False
    
    @staticmethod
    def setmode(mode): pass
    
    @staticmethod
    def setwarnings(enabled): pass
    
    @staticmethod
    def setup(pin, mode): pass
    
    @staticmethod
    def output(pin, state): 
        print(f"GPIO {pin} set to {state}")
    
    @staticmethod
    def input(pin):
        return GPIO.LOW
    
    @staticmethod
    def cleanup(): pass

sys.modules['RPi.GPIO'] = GPIO()
EOF
```

### Testing Environment

Set up Prometheus and test sensors:

```bash
# Start Prometheus in Docker for testing
docker run -d -p 9090:9090 \
  -v $(pwd)/envirozen/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# Create mock sensor endpoints for testing
python3 test/mock_sensors.py
```

## Code Standards

### Python Code Style

We follow [PEP 8](https://pep8.org/) with some project-specific conventions:

```python
# Use descriptive variable names
temperature_cold_aisle = get_temperature('cold')
# Not: temp_c = get_temp('cold')

# Add docstrings to all functions
def evaluate_cooling_mode(temp_readings):
    """
    Determine the appropriate cooling mode based on temperature readings.
    
    Args:
        temp_readings (dict): Temperature readings from all sensors
        
    Returns:
        str: Cooling mode ('passive', 'freecooling', 'ac', 'emergency')
    """
    pass

# Use type hints where beneficial
def query_prometheus(query: str) -> List[Dict]:
    """Query Prometheus API and return results."""
    pass

# Constants in UPPER_CASE
DEFAULT_EVALUATION_INTERVAL = 10
EMERGENCY_TEMPERATURE_THRESHOLD = 36.0
```

### Code Organization

```
envirozen/
├── controller/           # Main application
│   ├── actions.py       # GPIO control functions
│   ├── config.py        # Configuration management
│   ├── envirozen.py     # Main control loop
│   ├── prometheus.py    # Prometheus client
│   └── server.py        # Flask web interface
├── sensors/             # Sensor code (MicroPython)
│   ├── main.py         # Main sensor application
│   └── sensor_readings.py  # Sensor data collection
└── tests/              # Test files
    ├── test_actions.py
    ├── test_config.py
    └── mock_sensors.py
```

### Hardware Interface Standards

- All GPIO interactions should go through `actions.py`
- Include fail-safe defaults (AC on if control fails)
- Log all hardware state changes
- Validate hardware responses where possible

### Error Handling

```python
import logging
import syslog

# Use appropriate logging levels
syslog.syslog(syslog.LOG_INFO, "System switched to free cooling mode")
syslog.syslog(syslog.LOG_ERR, "Failed to read temperature sensor")
syslog.syslog(syslog.LOG_CRIT, "Emergency cooling activated")

# Handle specific exceptions
try:
    temperature = query_prometheus(query)
except requests.RequestException as e:
    syslog.syslog(syslog.LOG_ERR, f"Prometheus query failed: {e}")
    return None
except ValueError as e:
    syslog.syslog(syslog.LOG_ERR, f"Invalid temperature data: {e}")
    return None
```

## Testing

### Running Tests

```bash
# Run all tests
python3 -m pytest tests/

# Run specific test file
python3 -m pytest tests/test_actions.py

# Run with coverage
python3 -m pytest --cov=envirozen tests/
```

### Test Categories

**Unit Tests**: Test individual functions
```python
def test_temperature_threshold_logic():
    """Test cooling mode selection logic."""
    assert determine_cooling_mode(15.0) == 'freecooling'
    assert determine_cooling_mode(35.0) == 'emergency'
```

**Integration Tests**: Test component interactions
```python
def test_prometheus_query_integration():
    """Test actual Prometheus queries work."""
    # Requires running Prometheus instance
    pass
```

**Hardware Tests**: Test GPIO functionality
```python
def test_gpio_control():
    """Test GPIO pin control (requires hardware)."""
    # Only run on actual hardware
    pass
```

### Creating Tests

- Write tests for all new functionality
- Include edge cases and error conditions
- Mock external dependencies (network, hardware)
- Document test requirements clearly

## Documentation

### Documentation Standards

- Use clear, simple language
- Include code examples for complex concepts
- Keep documentation updated with code changes
- Follow the existing documentation structure

### Types of Documentation

**API Documentation**: Function and class documentation
```python
def query_prometheus(query: str, timeout: int = 30) -> List[Dict]:
    """
    Query the Prometheus API for metrics data.
    
    Args:
        query: PromQL query string
        timeout: Request timeout in seconds
        
    Returns:
        List of metric results from Prometheus
        
    Raises:
        RequestException: If the query request fails
        ValueError: If the query response is invalid
        
    Example:
        >>> results = query_prometheus('temperature{location="cold"}')
        >>> print(results[0]['value'][1])  # Temperature value
        22.5
    """
```

**User Documentation**: Installation, configuration, usage guides

**Developer Documentation**: Architecture, contributing, API references

### Documentation Updates

When making code changes that affect:
- **Configuration**: Update `docs/INSTALLATION.md` and `docs/API.md`
- **Features**: Update `README.md` and relevant documentation
- **Troubleshooting**: Update `docs/TROUBLESHOOTING.md`
- **Architecture**: Update `docs/ARCHITECTURE.md`

## Pull Request Process

### Before Submitting

1. **Test your changes** thoroughly
2. **Update documentation** if needed
3. **Check code style** with linting tools
4. **Rebase your branch** on the latest main
5. **Write clear commit messages**

### Commit Message Format

```
type(scope): brief description

Detailed description of changes if needed.

- Include relevant issue numbers
- Explain why the change was made
- Document any breaking changes

Fixes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```
feat(sensors): add humidity threshold monitoring

fix(gpio): resolve fan control reliability issue

docs(api): update sensor endpoint documentation  

refactor(config): simplify temperature threshold structure
```

### Pull Request Template

```markdown
## Description
Brief description of the changes.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass  
- [ ] Manual testing completed
- [ ] Hardware testing completed (if applicable)

## Documentation
- [ ] Documentation updated
- [ ] API documentation updated (if applicable)
- [ ] README updated (if applicable)

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] No new warnings introduced
```

### Review Process

1. **Automated checks** must pass (if configured)
2. **Peer review** by project maintainers
3. **Testing** on actual hardware (for hardware changes)
4. **Documentation review** for documentation changes
5. **Approval** by project maintainer
6. **Merge** to main branch

### After Merge

- Delete your feature branch
- Update your fork
- Consider helping with related issues

## Hardware Contributions

### Testing with Hardware

If you have hardware access:
- Test changes on actual Raspberry Pi
- Verify GPIO control functionality
- Test with real sensors and equipment
- Document hardware-specific findings

### Hardware Documentation

When contributing hardware-related changes:
- Document wiring diagrams
- Include parts lists and specifications
- Provide troubleshooting steps
- Test with different hardware configurations

## Getting Help

### During Development

- **Documentation**: Check `docs/` directory first
- **Discussions**: Use GitHub Discussions for questions
- **Discord/Slack**: Join our community chat (if available)
- **Pair Programming**: Ask for help in discussions

### Mentorship

New contributors can request mentorship:
- Comment on issues asking for guidance
- Tag maintainers in discussions
- Start with "good first issue" labels
- Participate in community discussions

## Recognition

Contributors will be recognized through:
- **Contributors section** in README
- **Release notes** for significant contributions
- **GitHub contributor graphs**
- **Community highlights** in discussions

Thank you for contributing to Envirozen! 🌡️⚡