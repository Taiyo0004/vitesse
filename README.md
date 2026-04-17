# 📊 Industrial ROS2 Inspector & Performance Monitor

A comprehensive graphical diagnostic tool designed for real-time monitoring and performance analysis of **ROS2 ecosystems**. Engineered for industrial debugging, this tool tracks system-wide throughput and message latencies through an intuitive hierarchical interface.

---

## 📝 Overview

Unlike standard command-line tools, the **Industrial ROS2 Inspector** provides a centralized dashboard to maintain precise cycle times and monitor multi-node communication.

It is specifically built to help engineers identify:
- Communication bottlenecks  
- Sensor data drops  
- Timing irregularities  

in complex robotic deployments.

---

## ✨ Key Features

- 🌳 **Hierarchical Telemetry Tree**  
  Organized topic view with detailed lists of:
  - Publishers  
  - Subscribers  
  - Live message content  

- ⚡ **Real-time Performance Monitoring**  
  Automatically calculates:
  - Publishing Rate (**Hz**)  
  - Cycle Time (**ms**)  

- 📊 **Global Performance Dashboard**  
  Displays:
  - Total System Throughput  
  - Global Average Period  

- 🎯 **Selective Analytics**  
  - Enable/disable topics using checkboxes  
  - Customize global metric calculations  

- 🔄 **Dynamic Topic Discovery**  
  - Scans ROS2 network every **2 seconds**  
  - Automatically integrates new topics  

---

## 🛠 System Architecture

The application follows a **modular architecture**, separating backend logic from the UI.

### 1️⃣ Backend Logic (`inspector_logic.py`)

- 🚀 **Node Management**  
  Initializes the `industrial_detailed_inspector` ROS2 node  

- 🔍 **Discovery Engine**  
  Filters internal topics like:
  - `/rosout`  
  - `/tf`  

- 🔄 **Data Conversion**  
  Converts messages into **formatted JSON** for visualization  

---

### 2️⃣ Frontend UI (`main.py`)

- 🖥 **PyQt5 Framework**  
  Provides a fast and responsive GUI  

- 🧵 **Asynchronous Processing**  
  - Keeps UI smooth  
  - Uses threading with `rclpy`  

- 📡 **Telemetry Engine**  
  Calculates:
  - Frequency (Hz)  
  - Latency (ms)  

---

## 🚀 Getting Started

### 🔧 1. Prerequisites

- OS: Ubuntu 22.04 (or compatible Linux)
- ROS2: Humble / Foxy / Galactic
- Python Libraries:
  ```bash
  pip install PyQt5
  ```

---

### ▶️ 2. Execution

Make sure your ROS2 environment is sourced:

```bash
source /opt/ros/humble/setup.bash
source ~/your_ws/install/setup.bash
python3 main.py
```

---

## 🖥️ Using the Interface

- 📊 **Dashboard Panels**  
  View system-wide performance metrics  

- 🌳 **Topic Tree**  
  - Expand topics  
  - View metadata  
  - Inspect live message data  

- ✅ **Active Selection** 

  Use checkboxes to include/exclude topics in:
  - Combined Total  
  - Combined Average  

---

## ⚙️ Technical Specifications

- 📈 **Frequency (Hz) Calculation**
  ```
  Frequency = 1 / Δt
  ```

- ⏱ **Period (ms) Calculation**
  ```
  Period = 1000 / Hz
  ```

- 🔄 **UI Refresh Rate**
  - Updates every **1 second**

---

## 📌 Notes

> This tool is designed to assist engineers in identifying:
> - Communication bottlenecks  
> - Sensor drops  
> - Timing inconsistencies  
> in complex robotic systems.

---



 
