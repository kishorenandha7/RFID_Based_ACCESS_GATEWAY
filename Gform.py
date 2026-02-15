import network
import socket
from mfrc522 import MFRC522
import time
from machine import Pin
intled=Pin(1,Pin.OUT)
redled=Pin(9,Pin.OUT)
greenled=Pin(14,Pin.OUT)
buzzer=Pin(4,Pin.OUT)
button_pin = Pin(32, Pin.IN, Pin.PULL_UP)

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


rfid_gforms = {
    (0x03, 0x0C, 0x3A, 0x16): "https://google.com",
    (0x81, 0x57, 0x6A, 0x02): "https://instagram.com",
}
redirect_url = ""
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
    time.sleep(0.5)
    greenled.value(0)
    redled.value(1)
    time.sleep(0.1)
    
def button_pressed(pin):
    global rfid_status
    #print("Button pressed, resetting...")
    rfid_status="No card detected"
    buzzery3()

def scan_rfid():
    global rfid_status, redirect_url
    stat, tag_type = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        stat, raw_uid = rdr.anticoll()
        if stat == rdr.OK:
            uid = tuple(raw_uid[:4])
            if uid in rfid_gforms:
                buzzery2()
                rfid_status = "Valid Card Detected"
                redirect_url = rfid_gforms[uid]
                greenled.value(1)
                redled.value(0)
                time.sleep(1)
            else:
                buzzery()
                rfid_status = "Invalid Card Detected"
                redirect_url = ""  # No redirect for invalid cards
                greenled.value(0)
                redled.value(1)
                time.sleep(1)


def web_page():
    global rfid_status, redirect_url
    if rfid_status == "No card detected":
        # [Same as original code for "No card detected"]
        return """ <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Place Your RFID Card</title>
    <meta http-equiv="refresh" content="2" />
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #e0eafc;
            background: linear-gradient(135deg, #6d9df6 0%, #f6f7fb 100%);
            margin: 0; min-height: 100vh;
            display: flex; justify-content: center; align-items: center;
            color: #234ca2;
        }
        .card {
            background: #ffffffdd;
            padding: 50px 60px;
            border-radius: 20px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 450px;
            width: 90%;
        }
        .icon {
            font-size: 70px;
            margin-bottom: 30px;
            color: #4e7ed0;
            user-select: none;
        }
        h1 {
            font-weight: 700;
            margin-bottom: 20px;
            font-size: 2.3em;
            letter-spacing: 0.7px;
        }
        p {
            font-size: 1.1em;
            margin: 0 auto;
            max-width: 320px;
            line-height: 1.5em;
            color: #444;
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="icon">📶</div>
        <h1>Place Your RFID Card</h1>
        <p>Please keep your card within range. The page will refresh automatically when a card is detected.</p>
    </div>
</body>
</html>
 """
    elif rfid_status == "Valid Card Detected" and redirect_url:
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Valid Card Detected</title>
    <meta http-equiv="refresh" content="3;url="{redirect_url}" />
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #d7f2c9;
            background: linear-gradient(135deg, #8fd19e 0%, #f6fff7 100%);
            margin: 0; min-height: 100vh;
            display: flex; justify-content: center; align-items: center;
            color: #338a4b;
        }
        .card {
            background: #ffffffee;
            padding: 50px 60px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
            text-align: center;
            max-width: 450px;
            width: 90%;
        }
        .icon {
            font-size: 70px;
            margin-bottom: 25px;
            color: #4e9b4e;
            user-select: none;
        }
        h1 {
            font-weight: 700;
            margin-bottom: 18px;
            font-size: 2.2em;
            letter-spacing: 0.6px;
        }
        p {
            font-size: 1.15em;
            margin: 0 auto;
            max-width: 320px;
            line-height: 1.4em;
            color: #2f6f37;
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="icon">✅</div>
        <h1>Valid Card Detected</h1>
        <p>Redirecting... Thank you for your access.</p>
    </div>
</body>
</html>

""",redirect_url
    elif rfid_status == "Invalid Card Detected":
        # [Same as original code for "Invalid Card Detected"]
        return """ <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Invalid Card Detected</title>
    <meta http-equiv="refresh" content="3;url=/" />
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #ffd4d4;
            background: linear-gradient(135deg, #f19a9a 0%, #fff6f6 100%);
            margin: 0; min-height: 100vh;
            display: flex; justify-content: center; align-items: center;
            color: #cf3232;
        }
        .card {
            background: #ffffffee;
            padding: 50px 60px;
            border-radius: 20px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
            text-align: center;
            max-width: 450px;
            width: 90%;
        }
        .icon {
            font-size: 70px;
            margin-bottom: 25px;
            color: #ea6060;
            user-select: none;
        }
        h1 {
            font-weight: 700;
            margin-bottom: 18px;
            font-size: 2.2em;
            letter-spacing: 0.6px;
        }
        p {
            font-size: 1.15em;
            margin: 0 auto;
            max-width: 320px;
            line-height: 1.4em;
            color: #ad2d2d;
        }
    </style>
</head>
<body>
    <div class="card">
        <div class="icon">❌</div>
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

#print('Listening on', addr)
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
            response,link = web_page()
            cl.send('HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\n')
            cl.send('Location: {}\r\n'.format(link))
            cl.send('Content-Type: text/html\r\n\r\n')
            cl.send('<html><body><h1>Redirecting...</h1></body></html>')
            cl.send(response)
        else:
            response = web_page()
            cl.send('HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n')
            cl.send(response)
        cl.close()

    except Exception as e:
        print('Error:', e)
