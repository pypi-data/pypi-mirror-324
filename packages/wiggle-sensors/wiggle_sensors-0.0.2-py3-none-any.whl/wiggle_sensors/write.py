import json
import os
import csv
from pathlib import Path

BASE_FOLDER = Path.home() / "WiggleBin"
DATA_FOLDER = BASE_FOLDER / "sensor-data"

def create_directory():
    os.makedirs(DATA_FOLDER, exist_ok=True)

def write_to_csv(sensor_data, filename, fieldnames):
    """Write data to a CSV file"""
    DATA_FILE = DATA_FOLDER / f"{filename}.csv"

    create_directory()

    with open(DATA_FILE, "a", newline="") as csvfile:
        # Create a CSV writer object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        if os.stat(DATA_FILE).st_size == 0:
            writer.writeheader()

        # Write the sensor data
        writer.writerow(sensor_data)

def write_to_json(sensor_data, filename):
    """Write data to a JSON file"""
    DATA_FILE = DATA_FOLDER / f"{filename}.json"

    create_directory()

    # Append to the existing JSON file or create a new one
    if DATA_FILE.exists():
        with open(DATA_FILE, "r") as jsonfile:
            try:
                data = json.load(jsonfile)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(sensor_data)

    with open(DATA_FILE, "w") as jsonfile:
        json.dump(data, jsonfile, indent=4)