# AdGuard E-Ink Display on Raspberry Pi Zero 2 W

This guide walks through setting up a 2.13″ Waveshare HAT+ e-ink display to show AdGuard Home stats on a Raspberry Pi Zero 2 W running Debian Bookworm Lite.

---

## Hardware

- Raspberry Pi Zero 2 W  
- Waveshare 2.13″ e-Paper HAT+ (V4)  
- MicroSD card with Raspberry Pi OS Lite (64-bit)  
- Wi-Fi or Ethernet for AdGuard Home  

### Connection Diagram

```text
   ┌──────────────────────────────┐
   │     Waveshare 2.13" HAT+     │
   │     (epd2in13_V4 Display)    │
   │ ┌──────────────────────────┐ │
   │ │                          │ │
   │ │      e-Paper Screen      │ │
   │ │                          │ │
   │ └──────────────────────────┘ │
   └─────────────┬────────────────┘
                 │ SPI Interface
                 │ (via 40-pin GPIO)
   ┌─────────────┴────────────────┐
   │   Raspberry Pi Zero 2 W      │
   │ ┌──────────────────────────┐ │
   │ │ GPIO, SPI0, 3V3, GND     │ │
   │ │ MicroSD → OS + Script    │ │
   │ │ Wi-Fi → AdGuard Server   │ │
   │ └──────────────────────────┘ │
   └──────────────────────────────┘
Connect the e-Paper HAT+ directly to the 40-pin GPIO header of the Pi Zero 2 W.
Ensure the SPI interface is enabled in raspi-config.

Software Setup
1. Install dependencies
sudo apt update
sudo apt install python3-pip python3-pil python3-requests python3-pil.imagetk

2. Waveshare driver

Extract the Waveshare Python driver zip to:

~/e-Paper/RaspberryPi_JetsonNano/python/lib


Your display driver is: epd2in13_V4.py

AdGuard Home API Setup

Ensure AdGuard Home is installed and running.

Note your admin username/password for API authentication.

API endpoint for stats: http://127.0.0.1/control/stats

Python Script

Create ~/adguard_display.py with the full script (includes IP, clients online, last updated, and rotated 90° CCW).

(Full script as provided in the previous setup)

Running the Script Manually
python3 ~/adguard_display.py

Run on Boot Using systemd

Create service file:

sudo nano /etc/systemd/system/adguard_display.service


Paste:

[Unit]
Description=AdGuard E-Ink Display
After=network.target

[Service]
User=admin
WorkingDirectory=/home/admin
ExecStart=/usr/bin/python3 /home/admin/adguard_display.py
Restart=always

[Install]
WantedBy=multi-user.target


Enable and start:

sudo systemctl daemon-reload
sudo systemctl enable adguard_display.service
sudo systemctl start adguard_display.service
sudo systemctl status adguard_display.service

+-----------------------------+
| AdGuard IP: 192.0.2.42    |
| DNS Queries: 12345          |
| Blocked: 678 (5%)           |
| Domains Filtered: 890       |
| Avg Processing: 12.3 ms     |
| Clients: 4 | Updated: 14:32 |
+-----------------------------+
