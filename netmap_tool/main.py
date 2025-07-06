import argparse
import os
from .mapper import (
    build_graph_from_csv,
    draw_network_graph,
    export_graph_gexf,
    export_graph_graphml,
)


def main():
    parser = argparse.ArgumentParser(
        description="Network Infrastructure Mapping Tool from CSV data."
    )
    parser.add_argument(
        "--input_csv",
        required=True,
        help="Path to the input CSV file (e.g., links.csv). Must contain 'SourceDevice' and 'TargetDevice' columns.",
    )
    parser.add_argument(
        "--output_png",
        help="Path to save the output PNG image (e.g., network_map.png).",
    )
    parser.add_argument(
        "--layout",
        default="spring",
        choices=["spring", "kamada_kawai", "circular", "random", "shell", "spectral"],
        help="Layout algorithm for the PNG map (default: spring).",
    )
    parser.add_argument(
        "--output_gexf",
        help="Path to save the graph in GEXF format (e.g., network_map.gexf).",
    )
    parser.add_argument(
        "--output_graphml",
        help="Path to save the graph in GraphML format (e.g., network_map.graphml).",
    )

    args = parser.parse_args()

    # --- 1. Build graph from CSV ---
    print(f"Attempting to build graph from: {args.input_csv}")
    network_graph = build_graph_from_csv(args.input_csv)

    if network_graph is None:
        print("Failed to build graph. Exiting.")
        return

    if not network_graph.nodes():
        print(
            "Graph built successfully, but it contains no nodes (CSV might be empty or all rows invalid). No output will be generated."
        )
        return

    print(
        f"Graph built successfully: {network_graph.number_of_nodes()} nodes, {network_graph.number_of_edges()} edges."
    )

    # --- 2. Generate PNG output if path specified ---
    if args.output_png:
        print(
            f"Attempting to generate PNG map: {args.output_png} using {args.layout} layout..."
        )
        success_png = draw_network_graph(
            network_graph, args.output_png, layout_type=args.layout
        )
        if success_png:
            print(f"PNG map successfully generated: {args.output_png}")
        else:
            print(f"Failed to generate PNG map.")

    # --- 3. Export GEXF if path specified ---
    if args.output_gexf:
        print(f"Attempting to export graph to GEXF: {args.output_gexf}...")
        success_gexf = export_graph_gexf(network_graph, args.output_gexf)
        if success_gexf:
            print(f"Graph successfully exported to GEXF: {args.output_gexf}")
        else:
            print(f"Failed to export graph to GEXF.")

    # --- 4. Export GraphML if path specified ---
    if args.output_graphml:
        print(f"Attempting to export graph to GraphML: {args.output_graphml}...")
        success_graphml = export_graph_graphml(network_graph, args.output_graphml)
        if success_graphml:
            print(f"Graph successfully exported to GraphML: {args.output_graphml}")
        else:
            print(f"Failed to export graph to GraphML.")

    if not args.output_png and not args.output_gexf and not args.output_graphml:
        print(
            "No output options specified. Graph was built but no files were generated."
        )
        print("Use --output_png, --output_gexf, or --output_graphml to save the map.")


if __name__ == "__main__":
    main()
