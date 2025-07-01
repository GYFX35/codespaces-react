import argparse
import time
import json # For parsing device_profiles if given as JSON string
import uuid
from iot_simulator.generators import generate_sensor_data, generate_timestamp, DEVICE_STATES
from iot_simulator.publishers import format_payload, print_to_console, send_http_post

def parse_device_profiles(profiles_str_list):
    """
    Parses device profile strings.
    Each string can be "device_id:sensor1,sensor2" or just "sensor1,sensor2" (auto-gen ID).
    Or, it can be a JSON string representing a list of more complex profiles.
    """
    profiles = []
    if not profiles_str_list:
        return profiles

    # Check if the input is a single string that might be JSON
    if len(profiles_str_list) == 1 and (profiles_str_list[0].startswith('[') or profiles_str_list[0].startswith('{')):
        try:
            parsed_json = json.loads(profiles_str_list[0])
            if isinstance(parsed_json, list):
                # Expecting list of {"id": "dev1", "sensors": ["temp", "hum"]}
                for p_item in parsed_json:
                    if isinstance(p_item, dict) and "id" in p_item and "sensors" in p_item:
                        profiles.append({"id": p_item["id"], "sensors": p_item["sensors"]})
                    else:
                        print(f"Warning: Invalid JSON profile item format: {p_item}. Skipping.")
                return profiles
            elif isinstance(parsed_json, dict): # Single profile as JSON object
                 if "id" in parsed_json and "sensors" in parsed_json:
                    profiles.append({"id": parsed_json["id"], "sensors": parsed_json["sensors"]})
                    return profiles
                 else:
                    print(f"Warning: Invalid JSON profile object format: {parsed_json}. Skipping.")
                    return [] # Or handle as error
        except json.JSONDecodeError as e:
            print(f"Warning: Could not parse profile string as JSON '{profiles_str_list[0]}': {e}. Proceeding with string parsing.")
            # Fall through to string parsing if JSON attempt fails for a single ambiguous string

    # String parsing for "device_id:sensor1,sensor2" or "sensor1,sensor2"
    for profile_str in profiles_str_list:
        parts = profile_str.split(':', 1)
        device_id = ""
        sensors_str = ""

        if len(parts) == 2:
            device_id = parts[0].strip()
            sensors_str = parts[1].strip()
        elif len(parts) == 1:
            sensors_str = parts[0].strip()
            # No device_id provided, will auto-generate
        else:
            print(f"Warning: Invalid profile string format '{profile_str}'. Skipping.")
            continue

        if not device_id:
            device_id = f"sim-{uuid.uuid4().hex[:8]}"
            print(f"Auto-generated device ID: {device_id} for sensors: {sensors_str}")

        sensor_types = [s.strip() for s in sensors_str.split(',') if s.strip()]
        if not sensor_types:
            print(f"Warning: No sensor types specified for device ID '{device_id}' in profile '{profile_str}'. Skipping.")
            continue

        profiles.append({"id": device_id, "sensors": sensor_types})

    return profiles


def main_loop(profiles, interval_seconds, num_messages, output_target, http_url=None):
    """
    Main simulation loop.
    """
    if not profiles:
        print("No valid device profiles configured. Exiting.")
        return

    print(f"\nStarting IoT simulation...")
    print(f"Device Profiles: {profiles}")
    print(f"Interval: {interval_seconds}s")
    print(f"Messages per run (per profile): {num_messages if num_messages > 0 else 'Infinite'}")
    print(f"Output Target: {output_target}")
    if output_target == 'http' and http_url:
        print(f"HTTP Target URL: {http_url}")

    # Reset global device states for a fresh run if needed, or manage them per profile run.
    # For simplicity, DEVICE_STATES in generators.py is global.
    # If we want truly independent runs for counters/GPS per main_loop call, clear it here.
    # DEVICE_STATES.clear() # Uncomment if each run of main_loop should reset all device states

    try:
        msg_count = 0
        while True:
            if num_messages > 0 and msg_count >= num_messages:
                print(f"\nReached target message count ({num_messages}). Simulation finished for this run.")
                break

            current_ts = generate_timestamp()

            for profile in profiles:
                device_id = profile["id"]
                sensor_types = profile["sensors"]

                # This list will hold data from multiple sensors for this device for this timestamp
                all_sensor_readings_for_device = []

                for sensor_type in sensor_types:
                    # generate_sensor_data from generators.py manages state per device_id
                    reading = generate_sensor_data(device_id, sensor_type)
                    if reading:
                        all_sensor_readings_for_device.append(reading)

                if not all_sensor_readings_for_device:
                    print(f"Warning: No sensor data generated for device {device_id} at {current_ts}. Skipping.")
                    continue

                # Format the payload with all readings for this device
                payload = format_payload(device_id, current_ts, all_sensor_readings_for_device)

                if output_target == 'console':
                    print_to_console(payload)
                elif output_target == 'http':
                    if http_url:
                        send_http_post(http_url, payload)
                    else:
                        print("Error: HTTP output specified but no URL provided. Skipping send.")

            msg_count += 1
            if num_messages == 0 or msg_count < num_messages : # Only sleep if not the last message of a finite run
                print(f"--- Sent message batch #{msg_count}. Waiting {interval_seconds}s... ---")
                time.sleep(interval_seconds)

    except KeyboardInterrupt:
        print("\nSimulation stopped by user (Ctrl+C).")
    except Exception as e:
        print(f"\nAn unexpected error occurred during simulation: {e}")
    finally:
        print("IoT Simulation ended.")


def main():
    parser = argparse.ArgumentParser(description="Generic IoT Data Simulator.")

    parser.add_argument(
        "-p", "--profiles",
        nargs='+',
        required=True,
        help='Device profiles. Each profile as "device_id:sensor1,sensor2,..." or "sensor1,sensor2" (ID auto-generated). '
             'Alternatively, a single argument which is a JSON string: \'[{"id":"dev1","sensors":["temp","hum"]}]\' '
             'Supported sensors: temperature, humidity, gps, status, counter.'
    )
    parser.add_argument(
        "-i", "--interval",
        type=float,
        default=5.0,
        help="Interval in seconds between sending messages (default: 5.0s)."
    )
    parser.add_argument(
        "-n", "--num_messages",
        type=int,
        default=10,
        help="Number of messages to send per simulation run (0 for infinite) (default: 10)."
    )
    parser.add_argument(
        "-o", "--output",
        choices=['console', 'http'],
        default='console',
        help="Output target: 'console' or 'http' (default: console)."
    )
    parser.add_argument(
        "--http_url",
        help="Target URL for HTTP POST output (required if --output=http)."
    )

    args = parser.parse_args()

    if args.output == 'http' and not args.http_url:
        parser.error("--http_url is required when --output is 'http'.")

    parsed_profiles = parse_device_profiles(args.profiles)
    if not parsed_profiles:
        print("Error: No valid device profiles could be parsed. Please check your --profiles argument.")
        print("Examples: --profiles \"myDevice:temperature,humidity\" \"another:gps,counter\"")
        print("      or: --profiles '[{\"id\":\"dev1\",\"sensors\":[\"temperature\",\"status\"]}, {\"id\":\"dev2\",\"sensors\":[\"gps\"]}]'")
        return

    main_loop(
        profiles=parsed_profiles,
        interval_seconds=args.interval,
        num_messages=args.num_messages,
        output_target=args.output,
        http_url=args.http_url
    )

if __name__ == "__main__":
    main()
