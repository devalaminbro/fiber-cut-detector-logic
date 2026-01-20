```python
import os
import time
import requests
from datetime import datetime

# ============================================================
# Fiber Cut Detection Logic
# Author: Sheikh Alamin Santo
# Description: Monitors sequential nodes to find cut location
# ============================================================

# --- Configuration ---
# List nodes in order of physical connection (Server -> Node A -> Node B)
NETWORK_TOPOLOGY = [
    {"name": "Core-Router",     "ip": "192.168.88.1"},
    {"name": "Distribution-SW", "ip": "192.168.88.2"},
    {"name": "Zone-A-OLT",      "ip": "192.168.88.3"},
    {"name": "Zone-B-Splitter", "ip": "192.168.88.4"}
]

# Telegram Settings (Leave empty if testing locally)
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

# Ping Settings
RETRY_COUNT = 3  # How many fails before alert
CHECK_INTERVAL = 10 # Seconds

def send_telegram_alert(message):
    """Sends notification to Telegram Channel"""
    if TELEGRAM_TOKEN == "YOUR_BOT_TOKEN":
        print(f"[Simulation] Telegram Alert: {message}")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        print(f"[-] Failed to send alert: {e}")

def check_ping(ip):
    """Returns True if IP is reachable, False otherwise"""
    response = os.system(f"ping -c 1 -W 1 {ip} > /dev/null 2>&1")
    return response == 0

def monitor_network():
    print(f"[+] Starting Fiber Monitor Logic...")
    
    # Store previous state to avoid spamming alerts
    node_status = {node["ip"]: True for node in NETWORK_TOPOLOGY}

    while True:
        previous_node_name = "Server Room"
        
        for node in NETWORK_TOPOLOGY:
            name = node["name"]
            ip = node["ip"]
            
            is_alive = False
            
            # Retry Logic to confirm downtime
            for _ in range(RETRY_COUNT):
                if check_ping(ip):
                    is_alive = True
                    break
                time.sleep(1)
            
            # Logic: If Current Node is DOWN
            if not is_alive:
                if node_status[ip]: # If it was previously UP (State Change)
                    
                    # Logic: Determine Cut Location
                    # Since we loop in order, if this node is down, the cut is 
                    # between the 'previous_node' (which was up) and 'this node'.
                    
                    alert_msg = (
                        f"🚨 **FIBER CUT DETECTED!**\n"
                        f"📍 **Location:** Between [{previous_node_name}] and [{name}]\n"
                        f"❌ **Unreachable Node:** {name} ({ip})\n"
                        f"⏰ **Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                    )
                    
                    print(alert_msg)
                    send_telegram_alert(alert_msg)
                    node_status[ip] = False # Update state to DOWN
                
                # If a parent node is down, child nodes will obviously be down.
                # We stop checking further nodes to pinpoint the exact cut location.
                break 
            
            else:
                # If Node is UP
                if not node_status[ip]: # If it was previously DOWN
                    print(f"[+] Connection Restored: {name}")
                    send_telegram_alert(f"✅ **RESTORED:** Connection to {name} is back online.")
                    node_status[ip] = True # Update state to UP
                
                # Set this node as the "Previous Node" for the next iteration
                previous_node_name = name

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_network()
