import csv
import networkx as nx
import matplotlib.pyplot as plt
import os # <-- Import the os module

def build_graph_from_csv(csv_filepath):
    """
    Reads a CSV file defining network links and builds a networkx graph.

    The CSV file should have two columns: 'SourceDevice' and 'TargetDevice'.
    Each row represents a direct link between two devices.

    Args:
        csv_filepath (str): The path to the input CSV file.

    Returns:
        nx.Graph: A networkx graph object representing the network, or None if an error occurs.
    """
    graph = nx.Graph()
    nodes = set()  # Keep track of all unique nodes explicitly mentioned

    try:
        with open(csv_filepath, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            if not reader.fieldnames:
                print(f"Error: CSV file at {csv_filepath} appears to be empty or has no header row.")
                return None

            # Check for required headers
            if 'SourceDevice' not in reader.fieldnames or 'TargetDevice' not in reader.fieldnames:
                print(f"Error: CSV file must contain 'SourceDevice' and 'TargetDevice' columns. Found: {reader.fieldnames}")
                return None

            for row in reader:
                source = row['SourceDevice'].strip()
                target = row['TargetDevice'].strip()

                if not source or not target:
                    print(f"Warning: Skipping row with empty source or target device: {row}")
                    continue

                nodes.add(source)
                nodes.add(target)
                graph.add_edge(source, target)

        # Ensure all nodes mentioned (even if isolated after some links are skipped) are in the graph
        # Networkx add_edge automatically adds nodes, but if a node was only mentioned
        # in a row that had an empty counterpart, it might be missed.
        # This explicit add ensures all devices from valid parts of rows are included.
        for node in nodes:
            if not graph.has_node(node): # Though add_edge should handle this if source/target were valid
                 graph.add_node(node)

        if not graph.nodes():
            print("Warning: No nodes found in the graph. The CSV might be empty or all rows were invalid.")

        return graph

    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_filepath}")
        return None
    except Exception as e:
        print(f"An error occurred while reading or parsing the CSV file: {e}")
        return None

def draw_network_graph(graph, output_filepath, layout_type='spring'):
    """
    Draws the given networkx graph using matplotlib and saves it to a file.

    Args:
        graph (nx.Graph): The networkx graph to draw.
        output_filepath (str): The path to save the output PNG image.
        layout_type (str): The layout algorithm to use ('spring', 'kamada_kawai', 'circular', 'random', 'shell', 'spectral').

    Returns:
        bool: True if drawing and saving was successful, False otherwise.
    """
    if not graph or not graph.nodes():
        print("Graph is empty or has no nodes. Cannot draw.")
        return False

    plt.figure(figsize=(12, 10)) # Adjust figure size as needed

    # Choose layout algorithm
    if layout_type == 'spring':
        pos = nx.spring_layout(graph, k=0.15, iterations=20) # k adjusts spacing, iterations for convergence
    elif layout_type == 'kamada_kawai':
        pos = nx.kamada_kawai_layout(graph)
    elif layout_type == 'circular':
        pos = nx.circular_layout(graph)
    elif layout_type == 'random':
        pos = nx.random_layout(graph)
    elif layout_type == 'shell':
        pos = nx.shell_layout(graph)
    elif layout_type == 'spectral':
        pos = nx.spectral_layout(graph)
    else:
        print(f"Warning: Unknown layout type '{layout_type}'. Defaulting to spring layout.")
        pos = nx.spring_layout(graph, k=0.15, iterations=20)

    try:
        nx.draw(graph, pos,
                with_labels=True,
                node_color='skyblue',
                node_size=2000, # Increased node size
                edge_color='gray',
                font_size=10,    # Adjusted font size
                font_weight='bold',
                width=1.5,       # Edge width
                alpha=0.9)       # Node/edge transparency

        plt.title(f"Network Map ({layout_type.capitalize()} Layout)", size=15)
        plt.savefig(output_filepath, format="PNG", dpi=150) # Save as PNG with decent DPI
        plt.close() # Close the figure to free memory
        return True
    except Exception as e:
        print(f"An error occurred while drawing or saving the graph: {e}")
        plt.close() # Ensure figure is closed even if error occurs
        return False

def export_graph_gexf(graph, output_filepath):
    """Exports the given networkx graph to GEXF format."""
    if not graph: # Check if graph is None or empty (no nodes might still be valid for an empty file)
        print("Graph is None. Cannot export.")
        return False
    try:
        nx.write_gexf(graph, output_filepath)
        return True
    except Exception as e:
        print(f"An error occurred while exporting graph to GEXF: {e}")
        return False

def export_graph_graphml(graph, output_filepath):
    """Exports the given networkx graph to GraphML format."""
    if not graph:
        print("Graph is None. Cannot export.")
        return False
    try:
        nx.write_graphml(graph, output_filepath, infer_numeric_types=True) # infer_numeric_types can be useful
        return True
    except Exception as e:
        print(f"An error occurred while exporting graph to GraphML: {e}")
        return False

if __name__ == '__main__':
    # Create a dummy CSV for testing
    dummy_csv_content = """SourceDevice,TargetDevice
Router1,Switch1
Router2,Switch1
Router1,Router2
FirewallA,Router1
Switch1,Server1
Switch1,Server2
Router2,FirewallB
IsolatedDevice1,
,IsolatedDevice2
FirewallA,FirewallA
"""
    dummy_csv_filepath = "test_network_links.csv"
    with open(dummy_csv_filepath, 'w', newline='', encoding='utf-8') as f:
        f.write(dummy_csv_content)

    print(f"--- Testing with '{dummy_csv_filepath}' ---")
    network_graph = build_graph_from_csv(dummy_csv_filepath)

    if network_graph:
        print(f"Graph created successfully with {network_graph.number_of_nodes()} nodes and {network_graph.number_of_edges()} edges.")
        print("Nodes:", list(network_graph.nodes()))
        print("Edges:", list(network_graph.edges()))

        # --- Test PNG Generation ---
        output_png_path = "test_network_map.png"
        print(f"\n--- Attempting to generate PNG: {output_png_path} ---")
        success_png = draw_network_graph(network_graph, output_png_path, layout_type='spring')
        if success_png:
            print(f"PNG generated: {output_png_path} (Please check this file visually if running locally)")
            # In a typical environment, you'd open the file here or have the user do it.
            # For automated testing, we primarily check if the function ran without error.
            # To be more thorough in a local env, one might compare to a reference image or check file size.
            os.remove(output_png_path) # Clean up test file
        else:
            print(f"PNG generation failed for {output_png_path}")

        output_png_path_kk = "test_network_map_kk.png"
        print(f"\n--- Attempting to generate PNG with Kamada-Kawai layout: {output_png_path_kk} ---")
        success_png_kk = draw_network_graph(network_graph, output_png_path_kk, layout_type='kamada_kawai')
        if success_png_kk:
            print(f"PNG generated: {output_png_path_kk}")
            os.remove(output_png_path_kk)
        else:
            print(f"PNG generation failed for {output_png_path_kk}")


        # Test case: Non-existent file
        print("\n--- Testing with non-existent file ---")
        non_existent_graph = build_graph_from_csv("non_existent.csv")
        if non_existent_graph is None:
            print("Correctly handled non-existent file.") # Export functions will also be skipped as graph is None

        # --- Test GEXF Export ---
        output_gexf_path = "test_network_map.gexf"
        print(f"\n--- Attempting to export GEXF: {output_gexf_path} ---")
        if network_graph: # Only attempt if graph building was successful
            success_gexf = export_graph_gexf(network_graph, output_gexf_path)
            if success_gexf:
                print(f"GEXF exported: {output_gexf_path} (Verify with Gephi or similar tool if running locally)")
                os.remove(output_gexf_path) # Clean up
            else:
                print(f"GEXF export failed for {output_gexf_path}")
        else:
            print("Skipping GEXF export as graph building failed earlier.")

        # --- Test GraphML Export ---
        output_graphml_path = "test_network_map.graphml"
        print(f"\n--- Attempting to export GraphML: {output_graphml_path} ---")
        if network_graph: # Only attempt if graph building was successful
            success_graphml = export_graph_graphml(network_graph, output_graphml_path)
            if success_graphml:
                print(f"GraphML exported: {output_graphml_path} (Verify with Gephi or similar tool if running locally)")
                os.remove(output_graphml_path) # Clean up
            else:
                print(f"GraphML export failed for {output_graphml_path}")
        else:
            print("Skipping GraphML export as graph building failed earlier.")

        # Test case: CSV with wrong headers
        wrong_header_csv_content = "DeviceA,DeviceB\nRouterX,SwitchY"
        wrong_header_filepath = "wrong_headers.csv"
        with open(wrong_header_filepath, 'w', newline='', encoding='utf-8') as f:
            f.write(wrong_header_csv_content)
        print(f"\n--- Testing with '{wrong_header_filepath}' (wrong headers) ---")
        wrong_header_graph = build_graph_from_csv(wrong_header_filepath)
        if wrong_header_graph is None:
            print("Correctly handled CSV with wrong headers.")

        # Test case: Empty CSV
        empty_csv_content = "SourceDevice,TargetDevice\n"
        empty_csv_filepath = "empty.csv"
        with open(empty_csv_filepath, 'w', newline='', encoding='utf-8') as f:
            f.write(empty_csv_content)
        print(f"\n--- Testing with '{empty_csv_filepath}' (empty CSV) ---")
        empty_graph = build_graph_from_csv(empty_csv_filepath)
        if empty_graph and not empty_graph.nodes(): # Should create a graph, but it will be empty
            print(f"Handled empty CSV. Nodes: {empty_graph.number_of_nodes()}, Edges: {empty_graph.number_of_edges()}")


    # Clean up dummy files
    import os
    os.remove(dummy_csv_filepath)
    os.remove(wrong_header_filepath)
    os.remove(empty_csv_filepath)
