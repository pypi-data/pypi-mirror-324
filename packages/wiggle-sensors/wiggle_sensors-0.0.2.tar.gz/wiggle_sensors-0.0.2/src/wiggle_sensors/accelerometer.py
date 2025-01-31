import time
import os
from datetime import datetime
import csv
from pathlib import Path
import time
import board
import busio
import adafruit_adxl34x

BASE_FOLDER = Path.home() / "WiggleBin"
DATA_FOLDER = BASE_FOLDER / "sensor-data"
DATA_FILE = DATA_FOLDER / "motion.csv"

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize ADXL345 accelerometer
accelerometer = adafruit_adxl34x.ADXL345(i2c)


def main():
    while True:
        try:
            # Read acceleration data
            x, y, z = accelerometer.acceleration

            # Output the acceleration values
            print("X-axis: {:.2f}   Y-axis: {:.2f}   Z-axis: {:.2f}".format(x, y, z))

            sensor_data = [{"time": datetime.now().isoformat(), "x": x, "y": y, "z": z}]

            with open(DATA_FILE, "a", newline="") as csvfile:
                # Specify the field names
                fieldnames = ["time", "x", "y", "z"]

                # Create a CSV writer object
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Write the header
                if os.stat(DATA_FILE).st_size == 0:
                    writer.writeheader()

                # Write the sensor data
                for data in sensor_data:
                    writer.writerow(data)

            time.sleep(1)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
