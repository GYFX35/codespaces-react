# Wi-Fi Analyzer CLI (Linux)

This Python-based command-line tool helps you analyze your Wi-Fi environment on Linux systems. It can scan for nearby networks, show channel usage, and monitor the signal strength of your current connection.

## Features

*   **Wi-Fi Network Scan:**
    *   Lists available Wi-Fi networks (SSIDs).
    *   Displays signal strength (quality percentage), channel, frequency (band), and security protocols.
*   **Channel Usage Analysis:**
    *   Shows how many networks are operating on each channel in both 2.4 GHz and 5 GHz bands.
    *   Includes a simple text-based bar graph for 2.4 GHz channel congestion.
*   **Current Connection Monitoring:**
    *   Displays the signal strength of your currently connected Wi-Fi network.
    *   Can use `nmcli` (shows quality %) or `iw` (shows dBm).
    *   Updates periodically for a specified duration.
*   **Auto-detection of Wi-Fi Interface:** Attempts to find your Wi-Fi interface automatically.

## Prerequisites

*   **Linux Operating System:** This tool is designed primarily for Linux and relies on Linux-specific command-line utilities.
*   **Python 3.6+**
*   **NetworkManager (`nmcli` command):** Required for most functionality. This is standard on most modern Linux desktop distributions.
*   **Wireless Tools (`iw` command):** Required if you want to use the `--use_iw` option for signal monitoring (provides dBm values). Often available by default or can be installed (e.g., `sudo apt install iw`).
*   **Wi-Fi Adapter:** A functional Wi-Fi adapter on your Linux machine.

## Installation

1.  **Ensure Prerequisites are Met:**
    *   Verify `python3` is installed.
    *   Check if `nmcli` and `iw` are available by typing them in your terminal. If not, install them using your distribution's package manager (e.g., `sudo apt install network-manager iw`).

2.  **Download the Code:**
    *   Place the `wifi_analyzer` directory (containing `scanner.py`, `analyzer.py`, `monitor.py`, `__init__.py`) and the `wifi_main.py` script in your desired project location.
    *   No external Python libraries (from PyPI) are required by the script itself; it uses standard libraries and calls system utilities.

## How to Run

1.  Open your terminal.
2.  Navigate to the directory where you saved `wifi_main.py` and the `wifi_analyzer` folder.
3.  Run the application using `python3`:

    ```bash
    python3 wifi_main.py [options]
    ```

## Usage & Options

You must specify at least one action: `--scan`, `--channels`, or `--monitor`.

*   `-h, --help`: Show help message and exit.
*   `--interface INTERFACE`: Specify the Wi-Fi interface (e.g., `wlan0`). If not provided, the tool will attempt to auto-detect it.
*   `--scan`: Scan for available Wi-Fi networks and display their details.
*   `--channels`: Display Wi-Fi channel usage analysis. This action automatically performs a scan if scan data isn't already available from a `--scan` action in the same command.
*   `--monitor`: Monitor the signal strength of the current Wi-Fi connection.
*   `--duration DURATION`: (Used with `--monitor`) Duration for monitoring in seconds (default: 10 seconds).
*   `--interval INTERVAL`: (Used with `--monitor`) Interval for signal strength updates in seconds (default: 2 seconds).
*   `--use_iw`: (Used with `--monitor`) Use the `iw` command for signal monitoring. This typically provides signal strength in dBm and might require `sudo` or specific permissions on some systems if `iw dev <iface> link` is restricted. `nmcli` (default) usually provides a quality percentage and often doesn't require `sudo` for this information.

### Examples

1.  **Scan for Wi-Fi networks and show channel usage on auto-detected interface:**
    ```bash
    python3 wifi_main.py --scan --channels
    ```

2.  **Scan networks on a specific interface (`wlp2s0`):**
    ```bash
    python3 wifi_main.py --interface wlp2s0 --scan
    ```

3.  **Monitor current connection's signal strength for 30 seconds (using `nmcli`):**
    ```bash
    python3 wifi_main.py --monitor --duration 30
    ```

4.  **Monitor current connection's signal strength using `iw` (dBm values):**
    ```bash
    python3 wifi_main.py --monitor --use_iw
    ```

## Interpreting the Output

*   **Signal Strength:**
    *   `nmcli` (default for scan and monitor): Shows as a percentage (0-100%). Higher is better.
    *   `iw` (for `--monitor --use_iw`): Shows in dBm (e.g., -50 dBm). This is a negative value. Closer to 0 is better (e.g., -40 dBm is stronger than -70 dBm).
*   **Channels (2.4 GHz Band):** Channels 1, 6, and 11 are generally recommended as they do not overlap. If you see many networks on other channels or heavily concentrated on one channel, it might indicate interference.
*   **Security:** Prefer networks using WPA2 or WPA3. Avoid WEP or Open (unsecured) networks if possible.

## Limitations

*   **Linux Only:** Relies on Linux-specific commands (`nmcli`, `iw`). It will not work on Windows or macOS without significant modifications.
*   **`nmcli` / `iw` Availability:** These tools must be installed and accessible in the system's PATH.
*   **Permissions:** While basic `nmcli dev wifi list` often works without `sudo`, `nmcli dev wifi rescan` (used by the script) or `iw dev <iface> scan` (an alternative not currently used as primary) might require `sudo` on some systems for full functionality or to get the freshest results. The script attempts a rescan; if it fails due to permissions, it may proceed with cached scan data. Monitoring with `iw` might also have permission sensitivities.
*   **Accuracy:** Signal strength values can fluctuate and are dependent on your hardware and environment.
*   **Parsing Robustness:** The parsing of `nmcli` and `iw` output is based on common formats but might break if the output format of these tools changes significantly in future versions or on highly customized systems.

## File Structure
```
.
├── wifi_analyzer/
│   ├── __init__.py     # Makes 'wifi_analyzer' a Python package
│   ├── scanner.py      # Logic for scanning networks and parsing nmcli output
│   ├── analyzer.py     # Logic for channel usage analysis
│   └── monitor.py      # Logic for monitoring current connection signal
└── wifi_main.py          # CLI entry point script
└── README_wifi_analyzer.md # This documentation file
```
```
