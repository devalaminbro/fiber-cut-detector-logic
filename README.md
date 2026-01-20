# ✂️ Optical Fiber Cut Detector & Alert System

![Language](https://img.shields.io/badge/Language-Python%203-blue)
![Network](https://img.shields.io/badge/Network-ICMP%20Monitoring-green)
![Alert](https://img.shields.io/badge/Alert-Telegram%20%2F%20SMS-orange)

## 📖 Overview
In FTTH (Fiber to the Home) networks, fiber cuts are frequent due to road construction or storms. Identifying the **exact location** of the cut manually causes long downtimes.

This repository contains a **Logic Script** that continuously monitors key network nodes (Switches/OLTs) in a sequential topology. By analyzing which nodes are unreachable, it pinpoints the specific segment where the fiber cut occurred.

## 🛠 Features
- 📍 **Precise Fault Isolation:** Determines if the cut is at the Backbone, Distribution, or Last Mile level.
- 🤖 **Telegram Integration:** Sends instant alerts to the Support Team Group.
- 📉 **False Alarm Prevention:** Uses a "Retry Threshold" (e.g., 3 failed pings) before declaring a cut.
- 📝 **Uptime Logging:** Logs outage start and end times for SLA reporting.

## ⚙️ Logic Explanation
Imagine a network topology: `Server -> Node A -> Node B -> Node C`
- If **Node A** is reachable, but **Node B** is NOT:
  - **Verdict:** Fiber cut between Node A and Node B.
- If **Node A** is unreachable:
  - **Verdict:** Fiber cut at the Backbone (Source).

## 🚀 Usage Guide

### 1. Configuration
Edit `monitor.py` to define your network nodes and Telegram credentials.
```python
NODES = [
    {"name": "Zone-1-Switch", "ip": "192.168.10.2"},
    {"name": "Zone-2-Switch", "ip": "192.168.10.3"},
]
BOT_TOKEN = "your-telegram-bot-token"
CHAT_ID = "-100123456789"

2. Run the Monitor
Run the script as a background service (daemon):
python3 monitor.py

3. Receive Alerts
When a cut is detected, you receive:

🚨 CRITICAL ALERT: Fiber Cut Detected! Location: Between Zone-1-Switch and Zone-2-Switch. Time: 2026-01-22 14:30:00

Author: Sheikh Alamin Santo
Cloud Infrastructure Specialist & Network Engineer
