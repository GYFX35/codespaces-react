# Generic IoT Data Simulator

This Python CLI tool simulates various types of IoT sensor data and sends it to configurable endpoints (console or HTTP POST). It's designed to help developers test IoT backends, data ingestion pipelines, dashboards, and other components without needing physical hardware.

## Features

*   **Multiple Sensor Types:** Simulate data for:
    *   Temperature (°C)
    *   Humidity (%)
    *   GPS Location (latitude, longitude - with random walk)
    *   Boolean Status (e.g., on/off, open/closed)
    *   Incrementing Counter
*   **Configurable Device Profiles:** Define multiple simulated devices, each with its own set of sensors. Device IDs can be specified or auto-generated.
*   **Flexible Output:**
    *   **Console:** Print generated data as structured JSON to the standard output.
    *   **HTTP POST:** Send data as a JSON payload to a specified HTTP(S) endpoint.
*   **Customizable Simulation:**
    *   Control the interval between messages.
    *   Set the total number of messages to send (or run indefinitely).
*   **Standardized Data Format:** Output includes `deviceId`, `timestamp` (ISO 8601 UTC), and sensor readings.
*   **Stateful Sensors:** GPS coordinates evolve with a random walk, and counters increment per device.

## Prerequisites

*   Python 3.6+
*   `requests` library (for HTTP output).

## Installation

1.  **Clone the repository or download the files.**
    Ensure you have `iot_sim_main.py`, the `iot_simulator` directory (containing `generators.py`, `publishers.py`, `__init__.py`), and the `iot_simulator_requirements.txt` file.

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    Navigate to the directory containing `iot_simulator_requirements.txt` and run:
    ```bash
    pip install -r iot_simulator_requirements.txt
    ```

## Usage

The tool is run from the command line using `python3 iot_sim_main.py`.

### Command-Line Arguments

*   `-p, --profiles PROFILES [PROFILES ...]`: **(Required)**
    *   Defines one or more device profiles.
    *   Each profile can be a string in the format `"device_id:sensor1,sensor2,..."`.
    *   If `device_id:` is omitted (e.g., `"sensor1,sensor2"`), a unique device ID will be auto-generated.
    *   Alternatively, you can provide a single argument which is a JSON string representing a list of profiles: `'[{"id":"dev1","sensors":["temp","hum"]}, {"id":"dev2","sensors":["gps"]}]'`
    *   **Supported sensor types:** `temperature`, `humidity`, `gps`, `status`, `counter`.
*   `-i, --interval INTERVAL`: (Optional) Interval in seconds between sending message batches (default: 5.0 seconds).
*   `-n, --num_messages NUM_MESSAGES`: (Optional) Number of message batches to send. A batch includes data from all defined profiles. Set to `0` for an infinite simulation (stop with Ctrl+C) (default: 10).
*   `-o, --output {console,http}`: (Optional) Output target. Defaults to `console`.
*   `--http_url HTTP_URL`: (Optional) Target URL for HTTP POST output. **Required if `--output=http` is chosen.**
*   `-h, --help`: Show help message and exit.

### JSON Payload Format

The data is sent/printed as a JSON object with the following structure:
```json
{
  "deviceId": "your_device_id",
  "timestamp": "YYYY-MM-DDTHH:MM:SS.ffffffZ", // ISO 8601 UTC
  // Sensor fields appear here based on profile
  "temperature_celsius": 23.7,
  "humidity_percent": 45.8,
  "location": {
    "latitude": 34.052200,
    "longitude": -118.243700
  },
  "active_status": true,
  "event_count": 123
}
```
*Note: Not all sensor fields will be present in every message; only those configured for the specific device profile.*

### Examples

1.  **Simulate one device with temperature and humidity, output to console (10 messages, 5s interval):**
    ```bash
    python3 iot_sim_main.py --profiles "device001:temperature,humidity"
    ```

2.  **Simulate two devices, 5 messages, 2s interval, output to console:**
    ```bash
    python3 iot_sim_main.py \
        --profiles "thermostat1:temperature" "gps_tracker:gps,counter" \
        --num_messages 5 \
        --interval 2
    ```

3.  **Simulate one device (auto-generated ID) with all sensor types, run indefinitely, output to console every 10s:**
    ```bash
    python3 iot_sim_main.py \
        --profiles "temperature,humidity,gps,status,counter" \
        --num_messages 0 \
        --interval 10
    ```

4.  **Simulate devices defined in a JSON string, output to an HTTP endpoint:**
    ```bash
    python3 iot_sim_main.py \
        --profiles '[{"id":"factory_sensor_A","sensors":["temperature","counter"]},{"id":"asset_tracker_B","sensors":["gps"]}]' \
        --output http \
        --http_url "http://localhost:8080/api/data" \
        --interval 2 \
        --num_messages 100
    ```
    *(Ensure you have an HTTP server listening at the specified `--http_url` if testing HTTP output.)*

## File Structure
```
.
├── iot_simulator/
│   ├── __init__.py     # Makes 'iot_simulator' a Python package
│   ├── generators.py   # Logic for generating sensor data
│   └── publishers.py   # Logic for formatting and sending data (console, HTTP)
├── iot_sim_main.py       # CLI entry point and main simulation loop
├── iot_simulator_requirements.txt # Python dependencies (requests)
└── README_iot_simulator.md        # This documentation file
```

## Sensor Details

*   **temperature:** Random float, default range -10.0 to 40.0 °C. Output key: `temperature_celsius`.
*   **humidity:** Random float, default range 20.0 to 80.0 %. Output key: `humidity_percent`.
*   **gps:** Simulates GPS coordinates (latitude, longitude) starting from a base point and performing a small random walk with each update. Output key: `location` (an object with `latitude` and `longitude`).
*   **status:** Random boolean (True/False). Output key: `active_status`.
*   **counter:** Integer that increments by 1 for each message from that specific device. Output key: `event_count`.

Sensor data generation (ranges, GPS step) is defined in `iot_simulator/generators.py` and can be customized there if needed.
```
