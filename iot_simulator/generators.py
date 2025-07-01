import random
import datetime
import uuid

# --- Configuration for sensor data ranges/values ---
DEFAULT_TEMP_RANGE_CELSIUS = (-10.0, 40.0)
DEFAULT_HUMIDITY_RANGE_PERCENT = (20.0, 80.0)

# Base GPS coordinates (e.g., a central point for random walks)
# For more realism, this could be configurable per device.
BASE_LATITUDE = 34.0522  # Los Angeles
BASE_LONGITUDE = -118.2437
# Max random walk step for GPS per update
GPS_MAX_STEP = 0.0005 # Approx 50 meters

# --- Generator Functions ---

def generate_temperature(min_temp=DEFAULT_TEMP_RANGE_CELSIUS[0], max_temp=DEFAULT_TEMP_RANGE_CELSIUS[1]):
    """Generates a random temperature reading."""
    return round(random.uniform(min_temp, max_temp), 2)

def generate_humidity(min_humidity=DEFAULT_HUMIDITY_RANGE_PERCENT[0], max_humidity=DEFAULT_HUMIDITY_RANGE_PERCENT[1]):
    """Generates a random humidity reading."""
    return round(random.uniform(min_humidity, max_humidity), 2)

def generate_gps_coordinates(current_lat=None, current_lon=None):
    """
    Generates GPS coordinates, optionally performing a random walk from previous coordinates.
    If no current coordinates are provided, starts from BASE_LATITUDE, BASE_LONGITUDE.
    """
    if current_lat is None or current_lon is None:
        lat = BASE_LATITUDE
        lon = BASE_LONGITUDE
    else:
        lat = current_lat + random.uniform(-GPS_MAX_STEP, GPS_MAX_STEP)
        lon = current_lon + random.uniform(-GPS_MAX_STEP, GPS_MAX_STEP)

    # Clamp to valid GPS ranges
    lat = max(min(lat, 90.0), -90.0)
    lon = max(min(lon, 180.0), -180.0)

    return {"latitude": round(lat, 6), "longitude": round(lon, 6)}

def generate_boolean_status():
    """Generates a random boolean status (True/False)."""
    return random.choice([True, False])

def generate_counter_value(current_value=0):
    """Increments a counter value."""
    return current_value + 1

def generate_timestamp():
    """Generates an ISO 8601 formatted timestamp in UTC."""
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def generate_device_id(prefix="sim"):
    """Generates a unique device ID."""
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


# --- Main Data Generation Orchestrator (per device state) ---

# Store last known values for sensors that evolve (like GPS, counter)
# This would typically be managed per device instance in the main simulator loop.
# For testing here, we can use a global-like dictionary.
DEVICE_STATES = {} # Key: device_id, Value: dict of sensor states (e.g., last_lat, last_lon, last_count)

def generate_sensor_data(device_id, sensor_type_config):
    """
    Generates data for a specific sensor type, maintaining state if necessary.

    Args:
        device_id (str): The ID of the device for which to generate data.
        sensor_type_config (str or dict):
            If str: 'temperature', 'humidity', 'gps', 'status', 'counter'.
            If dict: Can provide specific params, e.g., {'type': 'temperature', 'range': [0, 30]}
                     (Not fully implemented for MVP, uses defaults for now).

    Returns:
        dict: A dictionary containing the sensor type as key and generated value.
              e.g., {'temperature_celsius': 25.5} or {'gps': {'latitude': ..., 'longitude': ...}}
              Returns None if sensor type is unknown.
    """
    if device_id not in DEVICE_STATES:
        DEVICE_STATES[device_id] = {
            "counter": 0,
            "latitude": None, # Start GPS from base if no prior state
            "longitude": None
        }

    sensor_type = sensor_type_config
    # TODO: Add parsing for sensor_type_config if it's a dict for custom ranges in future.

    if sensor_type == 'temperature':
        return {'temperature_celsius': generate_temperature()}
    elif sensor_type == 'humidity':
        return {'humidity_percent': generate_humidity()}
    elif sensor_type == 'gps':
        coords = generate_gps_coordinates(
            DEVICE_STATES[device_id].get('latitude'),
            DEVICE_STATES[device_id].get('longitude')
        )
        DEVICE_STATES[device_id]['latitude'] = coords['latitude']
        DEVICE_STATES[device_id]['longitude'] = coords['longitude']
        return {'location': coords}
    elif sensor_type == 'status':
        # Example: could be named based on config, e.g., "door_status"
        return {'active_status': generate_boolean_status()}
    elif sensor_type == 'counter':
        DEVICE_STATES[device_id]['counter'] = generate_counter_value(DEVICE_STATES[device_id]['counter'])
        return {'event_count': DEVICE_STATES[device_id]['counter']}
    else:
        print(f"Warning: Unknown sensor type '{sensor_type}' requested for device '{device_id}'.")
        return None

if __name__ == '__main__':
    print("--- Testing Individual Generators ---")
    print(f"Temperature: {generate_temperature()} °C")
    print(f"Humidity: {generate_humidity()} %")

    gps_coords1 = generate_gps_coordinates()
    print(f"Initial GPS: {gps_coords1}")
    gps_coords2 = generate_gps_coordinates(gps_coords1['latitude'], gps_coords1['longitude'])
    print(f"Next GPS (walk): {gps_coords2}")

    print(f"Boolean Status: {generate_boolean_status()}")
    print(f"Counter (start 0): {generate_counter_value(0)}")
    print(f"Counter (start 10): {generate_counter_value(10)}")
    print(f"Timestamp: {generate_timestamp()}")
    print(f"Device ID: {generate_device_id()}")
    print(f"Device ID (prefix 'dev'): {generate_device_id(prefix='health_sensor')}")

    print("\n--- Testing generate_sensor_data (stateful) ---")
    dev1 = "simDeviceTest001"
    print(f"\nDevice: {dev1}")

    sensor_reading = generate_sensor_data(dev1, 'temperature')
    print(f"Sensor data: {sensor_reading}")
    assert 'temperature_celsius' in sensor_reading

    sensor_reading = generate_sensor_data(dev1, 'gps')
    print(f"Sensor data: {sensor_reading}")
    assert 'location' in sensor_reading

    sensor_reading = generate_sensor_data(dev1, 'gps') # Second GPS reading for same device
    print(f"Sensor data (GPS again): {sensor_reading}")
    assert sensor_reading['location']['latitude'] != BASE_LATITUDE or sensor_reading['location']['longitude'] != BASE_LONGITUDE

    sensor_reading = generate_sensor_data(dev1, 'counter')
    print(f"Sensor data: {sensor_reading}")
    assert sensor_reading['event_count'] == 1

    sensor_reading = generate_sensor_data(dev1, 'counter')
    print(f"Sensor data (Counter again): {sensor_reading}")
    assert sensor_reading['event_count'] == 2

    sensor_reading = generate_sensor_data(dev1, 'status')
    print(f"Sensor data: {sensor_reading}")
    assert 'active_status' in sensor_reading

    sensor_reading = generate_sensor_data(dev1, 'unknown_sensor')
    assert sensor_reading is None

    # Test state for a different device
    dev2 = "simDeviceTest002"
    print(f"\nDevice: {dev2}")
    sensor_reading = generate_sensor_data(dev2, 'counter')
    print(f"Sensor data: {sensor_reading}")
    assert sensor_reading['event_count'] == 1
    sensor_reading = generate_sensor_data(dev1, 'counter') # dev1 counter should be unaffected
    print(f"Sensor data (dev1 Counter check): {sensor_reading}")
    assert sensor_reading['event_count'] == 3

    print("\nAll basic generator tests seem to pass.")
