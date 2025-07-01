import json
import requests
import time
import random # <--- Import random

def format_payload(device_id, timestamp, sensor_data_list):
    """
    Formats the final JSON payload.
    Sensor_data_list is a list of dicts, e.g., [{'temperature_celsius': 22.5}, {'humidity_percent': 45}]
    These will be merged into a single data object.
    """
    payload = {
        "deviceId": device_id,
        "timestamp": timestamp
    }
    # Merge all sensor data dictionaries into the main payload
    for sensor_dict in sensor_data_list:
        if sensor_dict: # Ensure it's not None (e.g., from an unknown sensor type)
            payload.update(sensor_dict)
    return payload

def print_to_console(payload):
    """Prints the JSON payload to the console."""
    try:
        print(json.dumps(payload, indent=2))
        return True
    except Exception as e:
        print(f"Error printing to console: {e}")
        return False

def send_http_post(url, payload, timeout=10):
    """
    Sends the JSON payload via HTTP POST to the specified URL.

    Args:
        url (str): The target URL.
        payload (dict): The data payload to send.
        timeout (int): Request timeout in seconds.

    Returns:
        bool: True if the request was successful (e.g., 2xx status code), False otherwise.
    """
    if not url:
        print("Error: HTTP target URL not specified.")
        return False

    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=timeout)
        response.raise_for_status() # Raises an HTTPError for bad responses (4XX or 5XX)
        print(f"Data successfully sent to {url}. Status: {response.status_code}")
        return True
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error sending data to {url}: {e.response.status_code} {e.response.reason}")
        print(f"Response body: {e.response.text}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error sending data to {url}: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout sending data to {url}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"An unexpected error occurred sending data to {url}: {e}")
    return False

if __name__ == '__main__':
    # Test data (mimicking what the main simulator loop would provide)
    test_device_id = "simTestDevice001"

    # Simulate what generate_timestamp() would do
    from datetime import datetime, timezone
    test_timestamp = datetime.now(timezone.utc).isoformat()

    # Simulate what generate_sensor_data() would produce for a list of sensors
    test_sensor_data_temp = {'temperature_celsius': 25.5}
    test_sensor_data_humidity = {'humidity_percent': 55.2}
    test_sensor_data_gps = {'location': {'latitude': 34.05, 'longitude': -118.24}}
    test_sensor_data_list = [test_sensor_data_temp, test_sensor_data_humidity, test_sensor_data_gps]

    # --- Test format_payload ---
    print("--- Testing Payload Formatting ---")
    formatted_payload = format_payload(test_device_id, test_timestamp, test_sensor_data_list)
    print("Formatted Payload:")
    print_to_console(formatted_payload) # Also tests print_to_console
    assert formatted_payload["deviceId"] == test_device_id
    assert "temperature_celsius" in formatted_payload
    assert "location" in formatted_payload
    assert isinstance(formatted_payload["location"], dict)
    print("Payload formatting test passed.")

    # --- Test print_to_console (implicitly tested above) ---
    print("\n--- Testing Console Output (already seen above) ---")
    success_print = print_to_console({"message": "Test console print"})
    assert success_print
    print("Console output test passed (check output above).")


    # --- Test send_http_post ---
    # For this test to actually send, you need a local server listening
    # or use a service like https://beeceptor.com or https://requestbin.com
    # Example: python -m http.server 8080 (will show POST requests in its log)

    print("\n--- Testing HTTP POST ---")
    # test_http_url = "http://localhost:8080" # For local testing with `python -m http.server 8080`
    # test_http_url = "https://httpbin.org/post" # A public endpoint that echoes requests
    test_http_url_beeceptor = "https://jules-iot-test.free.beeceptor.com/mydata" # My temporary Beeceptor endpoint

    print(f"Attempting to send data to: {test_http_url_beeceptor}")
    print("If this URL is active, you should see the request there.")
    print("This test will likely print success if the endpoint is reachable and returns 2xx.")

    http_payload = {
        "deviceId": "httpTestDevice",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "test_value": random.randint(1, 100),
        "message": "Hello from IoT Simulator Test"
    }

    # Note: In a sandbox without internet, this will likely fail with ConnectionError.
    # The goal here is to ensure the function structure is correct.
    success_http = send_http_post(test_http_url_beeceptor, http_payload)
    if success_http:
        print("HTTP POST test reported success (check Beeceptor or your test endpoint).")
    else:
        print("HTTP POST test reported failure (this is expected if no internet/server).")

    print("\n--- Testing HTTP POST with invalid URL ---")
    success_http_invalid = send_http_post("http://nonexistentfakedomain123abc.com/api", http_payload)
    assert not success_http_invalid # Should fail
    print("HTTP POST to invalid URL test passed (expected failure).")

    print("\n--- Testing HTTP POST with no URL ---")
    success_http_no_url = send_http_post("", http_payload)
    assert not success_http_no_url
    print("HTTP POST with no URL test passed (expected failure).")

    print("\nPublisher tests complete.")
