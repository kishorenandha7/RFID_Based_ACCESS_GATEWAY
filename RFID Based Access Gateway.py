import network
import socket
from mfrc522 import MFRC522
import time
from machine import Pin
intled=Pin(1,Pin.OUT)
redled=Pin(12,Pin.OUT)
greenled=Pin(14,Pin.OUT)
buzzer=Pin(27,Pin.OUT)
button_pin = Pin(4, Pin.IN, Pin.PULL_UP)

# Wi-Fi credentials 
ssid = 'KING👑'
password = 'kishore@08'

# Connect to WiFi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected():
    time.sleep(1)

print('Connected, IP:', wlan.ifconfig()[0])
intled.value(1)

# Initialize RFID
rdr = MFRC522(sck=33, mosi=23, miso=19, rst=13, cs=25)

right_card_uid = (0x03, 0x0C, 0x3A, 0x16)  

rfid_status = "No card detected"

def buzzery():
    buzzer.on()
    time.sleep(0.5)
    buzzer.off()

def buzzery2():
    buzzer.on()
    time.sleep(0.2)
    buzzer.off()
    time.sleep(0.1)
    buzzer.on()
    time.sleep(0.2)
    buzzer.off()

def buzzery3():
    for _ in range(3):
        buzzer.on()
        time.sleep_ms(100)
        buzzer.off()
    
def blinky():
    greenled.value(1)
    redled.value(0)
    time.sleep(0.1)
    greenled.value(0)
    redled.value(1)
    time.sleep(0.1)
    
def button_pressed(pin):
    global rfid_status
    #print("Button pressed, resetting...")
    rfid_status="No card detected"
    buzzery3()

def scan_rfid():
    global rfid_status
    stat, tag_type = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        stat, raw_uid = rdr.anticoll()
        if stat == rdr.OK:
            uid = tuple(raw_uid[:4])
            if uid == right_card_uid:
                buzzery2()
                rfid_status = "Valid Card Detected"
                greenled.value(1)
                redled.value(0)
                time.sleep(1)
                
            else:
                buzzery()
                rfid_status = "Invalid Card Detected"
                greenled.value(0)
                redled.value(1)
                time.sleep(1)
    '''else:
        time.sleep(1)
        rfid_status = "No card detected"'''
    #print(rfid_status)

def web_page():
    global rfid_status
    if rfid_status == "No card detected":
        return """<!DOCTYPE html>
<html>
<head>
    <title>Place Your RFID Card</title>
    <meta http-equiv="refresh" content="2" />
    <style>
        body {
            background: linear-gradient(135deg, #6d9df6 0%, #f6f7fb 100%);
            min-height: 100vh;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
        }
        .container {
            background: rgba(255, 255, 255, 0.85);
            padding: 40px 60px;
            border-radius: 18px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.09);
            text-align: center;
        }
        h1 {
            color: #234ca2;
            font-size: 2.3em;
            margin-bottom: 18px;
            letter-spacing: 0.5px;
        }
        .icon {
            font-size: 4em;
            color: #4e7ed0;
            margin-bottom: 20px;
        }
        p {
            color: #444;
            font-size: 1.15em;
            margin: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">RFID ACCESS GATEWAY</div>
        <h1>Please place your RFID card near the reader</h1>
        <p>Keep your card within range. The page will automatically update when a card is detected.</p>
    </div>
</body>
</html>
"""
    elif rfid_status == "Valid Card Detected":
        return """<!DOCTYPE html>
<html>
<head>
    <title>Card Detected</title>
    <meta http-equiv="refresh" content="3;url=https://youtu.be/Llss1aRo8tw?si=gEalpnn1ndKgv1jO" />
    <style>
        body {
            background: linear-gradient(135deg, #8fd19e 0%, #f6fff7 100%);
            min-height: 100vh;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
        }
        .container {
            background: rgba(255,255,255,0.95);
            padding: 40px 60px;
            border-radius: 18px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.09);
            text-align: center;
        }
        h1 {
            color: #338a4b;
            font-size: 2.2em;
            margin-bottom: 18px;
            letter-spacing: 0.5px;
        }
        .icon {
            font-size: 4em;
            color: #4e9b4e;
            margin-bottom: 20px;
        }
        p {
            color: #444;
            font-size: 1.15em;
            margin: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">:)</div>
        <h1>Valid Card Detected</h1>
        <p>Redirecting... Thank you!</p>
    </div>
</body>
</html>
"""
    elif rfid_status == "Invalid Card Detected":
        return """<!DOCTYPE html>
<html>
<head>
    <title>Invalid Card</title>
    <meta http-equiv="refresh" content="3;url=/" />
    <style>
        body {
            background: linear-gradient(135deg, #f19a9a 0%, #fff6f6 100%);
            min-height: 100vh;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
        }
        .container {
            background: rgba(255,255,255,0.95);
            padding: 40px 60px;
            border-radius: 18px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.09);
            text-align: center;
        }
        h1 {
            color: #cf3232;
            font-size: 2.2em;
            margin-bottom: 18px;
            letter-spacing: 0.5px;
        }
        .icon {
            font-size: 4em;
            color: #ea6060;
            margin-bottom: 20px;
        }
        p {
            color: #444;
            font-size: 1.15em;
            margin: 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">:(</div>
        <h1>Invalid Card Detected</h1>
        <p>This card is not authorized. Please try again.</p>
    </div>
</body>
</html>
"""
    else:
        return """<!DOCTYPE html><html><head><title>Error</title></head><body><h1>Unexpected Status</h1></body></html>"""


# Setup socket and listen
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)

button_pin.irq(trigger=Pin.IRQ_RISING, handler=button_pressed)

while True:
    scan_rfid()
    if rfid_status == "No card detected":
        blinky()
    try:
        cl, addr = s.accept()
        print('Client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        request_line = cl_file.readline()

        # Read HTTP headers
        while True:
            header_line = cl_file.readline()
            if header_line == b'' or header_line == b'\r\n':
                break

        # Serve content based on requested path
        request = request_line.decode()
        if 'GET /status' in request:
            response = web_page()
            cl.send('HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\n')
            cl.send(response)
        else:
            response = web_page()
            cl.send('HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n')
            cl.send(response)
        cl.close()

    except Exception as e:
        print('Error:', e)
