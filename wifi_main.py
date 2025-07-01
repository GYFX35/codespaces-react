import argparse
import time
from wifi_analyzer import (
    get_wifi_interface,
    scan_wifi_networks,
    get_channel_usage,
    display_channel_usage_text,
    monitor_current_connection_signal,
    # Individual fetchers can also be used if needed, but monitor is more user-facing
    get_current_connection_info_nmcli,
    get_current_signal_strength_iw
)

def main():
    parser = argparse.ArgumentParser(description="Wi-Fi Analyzer Tool for Linux.")
    parser.add_argument(
        "--interface",
        help="Specify the Wi-Fi interface (e.g., wlan0). Auto-detected if not provided."
    )
    parser.add_argument(
        "--scan",
        action="store_true",
        help="Scan for available Wi-Fi networks and display their details."
    )
    parser.add_argument(
        "--channels",
        action="store_true",
        help="Display Wi-Fi channel usage analysis (requires a scan)."
    )
    parser.add_argument(
        "--monitor",
        action="store_true",
        help="Monitor the signal strength of the current Wi-Fi connection."
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=10,
        help="Duration for monitoring in seconds (default: 10s)."
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=2,
        help="Interval for signal strength updates in seconds (default: 2s)."
    )
    parser.add_argument(
        "--use_iw",
        action="store_true",
        help="Use 'iw' command for signal monitoring (provides dBm, may need sudo or specific permissions)."
    )

    args = parser.parse_args()

    if not args.scan and not args.channels and not args.monitor:
        parser.print_help()
        print("\nError: No action specified. Please use --scan, --channels, or --monitor.")
        return

    target_interface = args.interface
    if not target_interface:
        print("Auto-detecting Wi-Fi interface...")
        target_interface = get_wifi_interface()
        if not target_interface:
            print("Could not auto-detect Wi-Fi interface. Please specify one using --interface.")
            return
        print(f"Using interface: {target_interface}")

    networks_data = None # To store scan results if needed by multiple actions

    if args.scan or args.channels: # Scan is needed for both options
        print(f"\nScanning Wi-Fi networks on interface {target_interface}...")
        networks_data = scan_wifi_networks(interface=target_interface)
        if not networks_data:
            print("No networks found or an error occurred during scan.")
            # If --channels was the only flag, we can't proceed.
            # If --scan was also there, it will just show no networks.

        if args.scan:
            if networks_data:
                print(f"\n--- Found {len(networks_data)} Wi-Fi Networks ---")
                for net in networks_data:
                    print(f"  SSID: {net['ssid']}")
                    print(f"    Signal: {net['signal']}%")
                    print(f"    Channel: {net['channel']} (Band: {net['band']}, Freq: {net['frequency']})")
                    print(f"    Security: {net['security']}")
                    print("-" * 20)
            else:
                print("No Wi-Fi networks detected or scan failed.")

    if args.channels:
        if networks_data is None: # Should have been populated if --scan wasn't also specified
             print("\nChannel analysis requires a network scan. Run with --scan or ensure scan succeeds.")
        elif not networks_data: # Scan ran but found nothing
            print("\nNo network data available to analyze for channel usage.")
        else:
            usage_2_4, usage_5 = get_channel_usage(networks_data)
            display_channel_usage_text(usage_2_4, usage_5)

    if args.monitor:
        monitor_current_connection_signal(
            interface=target_interface,
            duration=args.duration,
            interval=args.interval,
            use_iw=args.use_iw
        )

if __name__ == "__main__":
    main()
