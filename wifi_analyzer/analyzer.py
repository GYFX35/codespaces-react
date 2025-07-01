from collections import Counter

def get_channel_usage(networks_data):
    """
    Analyzes scanned Wi-Fi networks to determine channel usage.

    Args:
        networks_data (list): A list of dictionaries, where each dictionary
                              represents a Wi-Fi network and must contain
                              'channel' and 'band' keys.

    Returns:
        tuple: A tuple containing two dictionaries:
               - channel_usage_2_4ghz (dict): Channel counts for 2.4 GHz band.
               - channel_usage_5ghz (dict): Channel counts for 5 GHz band.
    """
    channels_2_4ghz = []
    channels_5ghz = []

    for net in networks_data:
        channel = net.get('channel')
        band = net.get('band')

        if not channel or not band: # Skip if essential data is missing
            continue

        if band == "2.4 GHz":
            channels_2_4ghz.append(channel)
        elif band == "5 GHz":
            channels_5ghz.append(channel)

    # Count occurrences of each channel
    channel_usage_2_4ghz = Counter(channels_2_4ghz)
    channel_usage_5ghz = Counter(channels_5ghz)

    return dict(sorted(channel_usage_2_4ghz.items())), dict(sorted(channel_usage_5ghz.items()))

def display_channel_usage_text(channel_usage_2_4ghz, channel_usage_5ghz):
    """
    Displays channel usage information in a text-based format.
    Includes a simple text-based bar graph for 2.4 GHz.
    """
    print("\n--- Wi-Fi Channel Usage ---")

    if not channel_usage_2_4ghz and not channel_usage_5ghz:
        print("No channel data to display.")
        return

    if channel_usage_2_4ghz:
        print("\n[2.4 GHz Band]")
        max_count_2_4 = 0
        if channel_usage_2_4ghz.values(): # Check if there are any counts
             max_count_2_4 = max(channel_usage_2_4ghz.values(), default=0)

        # Determine max bar length for scaling the simple text graph
        # Max bar length can be, e.g., 50 characters
        max_bar_len = 40

        for channel in range(1, 15): # Common 2.4 GHz channels (1-14)
            count = channel_usage_2_4ghz.get(channel, 0)
            if count > 0 : # Only print channels in use or if we want to show all, then remove this if
                bar = ""
                if max_count_2_4 > 0: # Avoid division by zero
                    bar_len = int((count / max_count_2_4) * max_bar_len) if max_count_2_4 > 0 else 0
                    bar = '█' * bar_len
                print(f"Channel {channel:2d}: {count:2d} network(s) {bar}")
            elif channel_usage_2_4ghz and channel in channel_usage_2_4ghz: # Explicitly show if 0 but was in data
                 print(f"Channel {channel:2d}: {count:2d} network(s)")


    if channel_usage_5ghz:
        print("\n[5 GHz Band]")
        # For 5GHz, channels are numerous and less prone to overlap in the same way.
        # A simple list format is probably clearer than a text bar graph covering all possible channels.
        for channel, count in channel_usage_5ghz.items():
            print(f"Channel {channel:3d}: {count:2d} network(s)")

    print("\nNote: Channel overlap in the 2.4 GHz band means networks on adjacent channels can interfere.")
    print("Aim for channels 1, 6, or 11 where possible in crowded 2.4 GHz environments.")


if __name__ == '__main__':
    # Mock data for testing get_channel_usage and display
    mock_networks = [
        {'ssid': 'NetA', 'signal': 70, 'channel': 1, 'band': '2.4 GHz', 'security': 'WPA2'},
        {'ssid': 'NetB', 'signal': 60, 'channel': 1, 'band': '2.4 GHz', 'security': 'WPA2'},
        {'ssid': 'NetC', 'signal': 80, 'channel': 6, 'band': '2.4 GHz', 'security': 'WPA2'},
        {'ssid': 'NetD', 'signal': 50, 'channel': 6, 'band': '2.4 GHz', 'security': 'WPA2'},
        {'ssid': 'NetE', 'signal': 75, 'channel': 6, 'band': '2.4 GHz', 'security': 'WPA2'},
        {'ssid': 'NetF', 'signal': 65, 'channel': 11, 'band': '2.4 GHz', 'security': 'WPA2'},
        {'ssid': 'NetG', 'signal': 85, 'channel': 36, 'band': '5 GHz', 'security': 'WPA2'},
        {'ssid': 'NetH', 'signal': 90, 'channel': 36, 'band': '5 GHz', 'security': 'WPA2'},
        {'ssid': 'NetI', 'signal': 70, 'channel': 40, 'band': '5 GHz', 'security': 'WPA2'},
        {'ssid': 'NetJ', 'signal': 60, 'channel': 149, 'band': '5 GHz', 'security': 'WPA2'},
        {'ssid': 'NetK', 'signal': 50, 'channel': 14, 'band': '2.4 GHz', 'security': 'WPA2'}, # Channel 14 (Japan)
        {'ssid': 'NetL', 'signal': 0, 'channel': 0, 'band': 'Unknown', 'security': 'WPA2'}, # Invalid data
        {'ssid': 'NetM', 'signal': 50, 'channel': 6, 'band': '2.4 GHz', 'security': 'WPA2'},
    ]

    usage_2_4, usage_5 = get_channel_usage(mock_networks)

    print("--- Mock Data Test ---")
    print("2.4 GHz Usage:", usage_2_4)
    print("5 GHz Usage:", usage_5)

    assert usage_2_4.get(1) == 2
    assert usage_2_4.get(6) == 4
    assert usage_2_4.get(11) == 1
    assert usage_2_4.get(14) == 1
    assert usage_5.get(36) == 2
    assert usage_5.get(40) == 1
    assert usage_5.get(149) == 1
    print("get_channel_usage assertions passed.")

    display_channel_usage_text(usage_2_4, usage_5)

    print("\n--- Test with Empty Data ---")
    empty_usage_2_4, empty_usage_5 = get_channel_usage([])
    display_channel_usage_text(empty_usage_2_4, empty_usage_5)
    assert not empty_usage_2_4
    assert not empty_usage_5
    print("Empty data test passed.")

    print("\n--- Test with Only 2.4 GHz Data ---")
    only_2_4_data = [net for net in mock_networks if net['band'] == '2.4 GHz']
    usage_2_4_only, usage_5_only = get_channel_usage(only_2_4_data)
    display_channel_usage_text(usage_2_4_only, usage_5_only)
    assert usage_2_4_only
    assert not usage_5_only
    print("Only 2.4 GHz data test passed.")

    print("\n--- Test with Only 5 GHz Data ---")
    only_5_data = [net for net in mock_networks if net['band'] == '5 GHz']
    usage_2_4_only_5, usage_5_only_5 = get_channel_usage(only_5_data)
    display_channel_usage_text(usage_2_4_only_5, usage_5_only_5)
    assert not usage_2_4_only_5
    assert usage_5_only_5
    print("Only 5 GHz data test passed.")
