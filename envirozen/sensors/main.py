import network
import socket
import time
import machine
import sensor_readings
  
from machine import Pin
 
intled = machine.Pin("LED", machine.Pin.OUT)
  
ssid = 'This is for Me!!!'
password = 'Simply13579'
 
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

# This will be replaced with the actual metric values
metrics_template = """
# TYPE temperature gauge
temperature {}

# TYPE humidity gauge
humidity {}

# TYPE pressure gauge
pressure {}

# TYPE luminance gauge
luminance {}

# TYPE color_temperature gauge
color_temperature {}
"""

 
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
s.bind(addr)
s.listen(1)
 
print('listening on', addr)

stateis = ""
 
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
            response = metrics_template.format(readings["temperature"], readings["humidity"], readings["pressure"], readings["luminance"], readings["color_temperature"])
                
            cl.send(b'HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
            cl.send(response.encode())
        else:
            # You can send an error message or some other response here if needed.
            cl.send(b'HTTP/1.0 404 Not Found\r\nContent-type: text/plain\r\n\r\nNot Found')

        cl.close()
 
    except OSError as e:
        cl.close()
        print('connection closed')
