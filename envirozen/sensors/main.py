import network
import socket
import time
import machine
import sensor_readings
  
from machine import Pin
 
intled = machine.Pin("LED", machine.Pin.OUT)
  
ssid = '**ZSENPOD**'
password = 'allchildrenexceptonegrowup'
 
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# Board location, this will be used in the Prometheus metrics to identify the sensor
# it can be a location or a name
location = 'hot'

# This will be replaced with the actual metric values
metrics_template = """
# HELP Temperature recorded in celcius
# TYPE temperature gauge
temperature{{location="{location}"}} {temperature}

# HELP Humidity recorded in percent
# TYPE humidity gauge
humidity{{location="{location}"}} {humidity}

# HELP Air pressure recorded in hectopascals hPA
# TYPE pressure gauge
pressure{{location="{location}"}} {pressure}

# Luminance recorded as lux
# TYPE luminance gauge
luminance{{location="{location}"}} {luminance}

# Color temperature recorded in kelvin
# TYPE color_temperature gauge
color_temperature{{location="{location}"}} {color_temperature}
"""
def initialize_connection():
    # Wait for connect or fail
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )
    
    # Open socket
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)
    return s

stateis = ""
 
def main_loop(s):
    # Listen for connections
    while True:
        try:
            cl, addr = s.accept()
            print('client connected from', addr)

            request = cl.recv(1024)
            print(request)

            # Split the request into lines
            request_lines = request.split(b'\r\n')

            # Extract the request method and path from the first line
            # Typical first line: 'GET /metrics HTTP/1.1'
            method, path, _ = request_lines[0].split(b' ', 2)

            if method == b'GET' and path == b'/metrics':
                # Handle the metric response here

                readings = sensor_readings.get_sensor_readings()

                response = metrics_template.format(
                    location=location,
                    temperature=readings["temperature"],
                    humidity=readings["humidity"],
                    pressure=readings["pressure"],
                    luminance=readings["luminance"],
                    color_temperature=readings["color_temperature"]
                )


                cl.send(b'HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
                cl.send(response.encode())
            else:
                # You can send an error message or some other response here if needed.
                cl.send(b'HTTP/1.0 404 Not Found\r\nContent-type: text/plain\r\n\r\nNot Found')

            cl.close()
    
        except OSError as e:
            cl.close()
            print('connection closed')

# Main execution
try:
    s = initialize_connection()
    main_loop(s)
except Exception as e:
    print('Critical error encountered:', e)
    print('Rebooting...')
    machine.reset()