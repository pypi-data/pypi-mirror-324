import glob
from datetime import datetime
import json
from pathlib import Path
from wiggle_sensors.write import write_to_csv, write_to_json

HOME_FOLDER = Path.home()
BASE_FOLDER = HOME_FOLDER / "WiggleBin"
SETTINGS_FILE = BASE_FOLDER / "settings.json"

with open(SETTINGS_FILE, "r") as f:
    settings = json.load(f)

def get_sensor_name_by_id(sensor_id, sensors = settings.get("temperature", [])):
    """Retrieve a sensor configuration by its ID."""
    sensor = next((sensor for sensor in sensors if sensor.get("id") == sensor_id), None)
    return sensor.get("name") if sensor else None

def read_DS18B20(sensor_path, decimals=1):
    """Reads the temperature from a 1-wire device"""

    with open(sensor_path, "r") as f:
        lines = f.readlines()
    equals_pos = lines[1].find("t=")
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2 :]
        temp = round(float(temp_string) / 1000.0, decimals)

    return temp

def write_DS18B20(decimals=1):
    """Write the temperature from multiple 1-wire devices"""

    sensors_data = {}

    devices = glob.glob("/sys/bus/w1/devices/28*")
    if not devices:
        print("No temperature sensors found.")
        return

    for device in devices:
        sensor_id = device.split("/")[-1]  # Extract the unique sensor ID
        sensor_path = device + "/w1_slave"
        sensor_name = get_sensor_name_by_id(sensor_id)

        try:
            temp = read_DS18B20(sensor_path, decimals)
            sensor_data = {
                "time": datetime.now().isoformat(),
                "id": sensor_id,
                "temperature": temp,
                "name": sensor_name
            }
            field_names = ["time", "id", "temperature", "name"]
            write_to_csv(sensor_data, "temperature", field_names)
            sensors_data[sensor_name] = temp

            print(f"Sensor {sensor_id} {sensor_name} temperature: {temp:.{decimals}f} C")
        except Exception as e:
            print(f"Error reading sensor {sensor_id}: {e}")

    if len(sensors_data) > 0:
        write_to_json(sensors_data, "temperature")

if __name__ == "__main__":
    write_DS18B20()
