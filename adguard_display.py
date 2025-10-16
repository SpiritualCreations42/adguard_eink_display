 #!/usr/bin/env python3
import sys
sys.path.append("/home/admin/e-Paper/RaspberryPi_JetsonNano/python/lib")
from waveshare_epd import epd2in13_V4
import sys
import time
import requests
import socket
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Add Waveshare driver path (adjust if your folder is elsewhere)
sys.path.append("/home/admin/e-Paper/RaspberryPi_JetsonNano/python/lib")
from waveshare_epd import epd2in13_V4

# -------- CONFIG --------
ADGUARD_API = "http://127.0.0.1/control/stats"
AUTH = ("admin", "administrator")  # <-- Replace with your admin username/password
REFRESH_INTERVAL = 300  # seconds
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# -------- FUNCTIONS --------
def get_ip_address():
    """Get the Pi's local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "N/A"

def fetch_stats():
    """Fetch AdGuard stats via API"""
    try:
        r = requests.get(ADGUARD_API, auth=AUTH, timeout=5)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("Failed to fetch stats:", e)
        return None

def format_stats(data):
    """Prepare stats for display"""
    ip = get_ip_address()
    clients_online = len(data.get("clients", []))  # Adjust if your version uses "top_clients"
    last_updated = datetime.now().strftime("%H:%M:%S")
    
    return [
        f"AdGuard IP: {ip}",
        f"DNS Queries: {data.get('dns_queries', 'N/A')}",
        f"Blocked: {data.get('blocked_filtering', 'N/A')} ({data.get('blocked_percent', 'N/A')}%)",
        f"Domains Filtered: {data.get('num_blocked_filtering', 'N/A')}",
        f"Avg Processing: {round(data.get('avg_processing_time', 0), 2)} ms",
        f"Clients: {clients_online} | Updated: {last_updated}"
    ]

def display_stats(lines):
    """Render stats to Waveshare e-ink"""
    epd = epd2in13_V4.EPD()
    epd.init()
    epd.Clear(0xFF)

    # Create image
    font = ImageFont.truetype(FONT_PATH, 16)
    image = Image.new('1', (epd.height, epd.width), 255)  # 1-bit white background
    draw = ImageDraw.Draw(image)

    # Draw each line
    y = 0
    for line in lines:
        draw.text((0, y), line, font=font, fill=0)
        y += 20  # line spacing

    # rotate the full image 90 counter clockwise
    image = image.rotate(90,expand=True)
    # Display on e-ink
    epd.display(epd.getbuffer(image))
    # Don't sleep yet — allow future refreshes

# -------- MAIN LOOP --------
def main():
    while True:
        stats = fetch_stats()
        if stats:
            lines = format_stats(stats)
            display_stats(lines)
        else:
            print("No stats to display.")
        time.sleep(REFRESH_INTERVAL)

# -------- RUN --------
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit()

