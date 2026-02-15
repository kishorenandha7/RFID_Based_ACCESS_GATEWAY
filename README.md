**RFID-Based Access Gateway**

This repository contains the design and implementation of an automated attendance and access control system developed at the Coimbatore Institute of Technology. The system is specifically designed for examination scenarios to replace manual roll calls with a secure, IoT-based verification method.

**Project Overview**
The system uses an ESP32 microcontroller and an MFRC522 RFID reader to authenticate students via pre-assigned RFID cards. Upon successful verification, the system provides immediate hardware feedback (LEDs and Buzzer) and redirects the student to a Google Form to log their attendance digitally.

**Key Features**

Automated Authentication: Extracts UIDs from RFID cards and compares them against a local database.
Real-time Feedback: Includes visual (Red/Green LEDs) and auditory (Buzzer) indicators for access status.
Dynamic Web Interface: Hosts a local web server on the ESP32 that serves HTML pages for "Idle," "Success," and "Invalid" states.
Google Form Integration: Automatically redirects authorized users to an online form for time-stamped attendance logging.
Manual System Reset: Features a physical push button to reset the scanning sequence for the next user.

**System Architecture**

**Hardware Components**

Microcontroller: ESP32.
RFID Module: MFRC522 Reader.
Indicators: Red LED, Green LED, and a Buzzer.
Input: Physical Push Button.

**PIN Configuration (MicroPython)**
The system is configured with the following GPIO mappings:
SPI SCK: Pin 33 
SPI MOSI: Pin 23 
SPI MISO: Pin 19 
RST: Pin 13 
CS: Pin 25 

**Technical Implementation**
The system is programmed in MicroPython. Its logic follows these states:
Idle State: The system blinks an LED to show readiness.
Card Detection: The MFRC522 scans for a UID.

**Validation:**
Valid Card: The Green LED lights up, the buzzer sounds a success tone, and the web page redirects to the Google Form within 3 seconds .
Invalid Card: The Red LED lights up, a failure tone sounds, and the user is notified of rejection .
Redirection: Students access the hosted web page via Wi-Fi to be automatically routed to the attendance URL.

**Advantages and Limitations**
**Advantages**
Eliminates manual errors and reduces processing time during exams.
Low-cost and easy-to-deploy hardware.
Provides digital, transparent records with time-stamped entries.

**Limitations**
Dependent on stable Wi-Fi connectivity for the redirection to function.
Requires secure management of physical RFID cards.

**Future Enhancements**
Integration with centralized institutional databases for real-time data management.
Enhanced security measures for the Google Form link
