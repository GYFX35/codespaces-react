# Network Infrastructure Mapping Tool (NetMap CLI)

NetMap CLI is a Python tool that generates network topology diagrams and graph data files from a simple CSV input. It's designed to quickly visualize device connectivity.

## Features

*   **CSV Input:** Reads network links from a CSV file with 'SourceDevice' and 'TargetDevice' columns.
*   **Graph Visualization:** Generates a PNG image of the network map using `matplotlib` and `networkx`.
    *   Supports multiple layout algorithms: `spring` (default), `kamada_kawai`, `circular`, `random`, `shell`, `spectral`.
*   **Graph Data Export:** Can export the network graph to:
    *   GEXF format (for use in Gephi or other graph analysis tools).
    *   GraphML format (another common format for graph tools).
*   **Command-Line Interface:** Easy-to-use CLI for specifying input and output options.

## Prerequisites

*   Python 3.6+
*   Libraries: `networkx`, `matplotlib`, `scipy` (SciPy is a dependency for some `networkx` layout algorithms).

## Installation

1.  **Clone the repository or download the files.**
    Ensure you have the `netmap_tool` directory (containing `main.py`, `mapper.py`, `__init__.py`) and the `requirements.txt` file.

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    Navigate to the directory containing `requirements.txt` and run:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The tool is run from the command line using `python -m netmap_tool.main`.

### Command-Line Arguments

*   `--input_csv INPUT_CSV`: **(Required)** Path to the input CSV file.
    *   The CSV file must contain 'SourceDevice' and 'TargetDevice' headers.
    *   Each row defines a link between the two specified devices.
*   `--output_png OUTPUT_PNG`: (Optional) Path to save the output PNG image (e.g., `mymap.png`).
*   `--layout {spring,kamada_kawai,circular,random,shell,spectral}`: (Optional) Layout algorithm for the PNG map. Defaults to `spring`.
*   `--output_gexf OUTPUT_GEXF`: (Optional) Path to save the graph in GEXF format (e.g., `mymap.gexf`).
*   `--output_graphml OUTPUT_GRAPHML`: (Optional) Path to save the graph in GraphML format (e.g., `mymap.graphml`).
*   `-h, --help`: Show help message and exit.

### Examples

1.  **Generate a PNG map with the default spring layout:**
    ```bash
    python -m netmap_tool.main --input_csv path/to/your/links.csv --output_png network_diagram.png
    ```

2.  **Generate a PNG map with the Kamada-Kawai layout:**
    ```bash
    python -m netmap_tool.main --input_csv links.csv --output_png map_kk.png --layout kamada_kawai
    ```

3.  **Export the graph to GEXF format:**
    ```bash
    python -m netmap_tool.main --input_csv links.csv --output_gexf my_network.gexf
    ```

4.  **Generate a PNG and also export to GraphML:**
    ```bash
    python -m netmap_tool.main --input_csv links.csv --output_png visual_map.png --output_graphml data_map.graphml
    ```

5.  **Only build the graph and print info (no file output):**
    ```bash
    python -m netmap_tool.main --input_csv links.csv
    ```
    *(The tool will inform you that no output options were specified)*

### CSV File Format

Your input CSV file must have a header row with `SourceDevice` and `TargetDevice`.

**Example `links.csv`:**
```csv
SourceDevice,TargetDevice
RouterA,Switch1
RouterB,Switch1
RouterA,RouterB
Firewall,RouterA
Switch1,ServerX
```

## File Structure
```
.
├── netmap_tool/
│   ├── __init__.py     # Makes 'netmap_tool' a Python package
│   ├── main.py         # CLI entry point
│   └── mapper.py       # Core logic for graph building, drawing, and exporting
├── requirements.txt      # Python dependencies
└── README_netmap.md      # This documentation file
```

## Limitations

*   **Simplicity:** This tool is designed for simple, direct device-to-device connectivity visualization. It does not parse complex configurations or infer relationships beyond what's explicitly in the CSV.
*   **Layouts:** Graph layout can be challenging for large or complex networks. The default layouts are good for small to medium-sized graphs. For very large networks, using the GEXF/GraphML export with a dedicated tool like Gephi is recommended for better layout control and exploration.
*   **No Device Details:** The map does not include interface names, IP addresses, VLANs, or other detailed device information. It only shows device names and their connections.
*   **Error Handling:** Basic error handling for file operations and CSV parsing is included. More complex CSV issues might require manual data cleaning.

## Future Enhancements (Potential)

*   Support for other input formats (e.g., JSON, YAML).
*   Ability to add attributes to nodes/edges via CSV (e.g., device type, link speed) and visualize them.
*   More sophisticated layout options or interactivity (would likely require different libraries e.g., web-based).
*   Basic parsing of simplified device configuration snippets (e.g., `show cdp neighbor` output).
```
