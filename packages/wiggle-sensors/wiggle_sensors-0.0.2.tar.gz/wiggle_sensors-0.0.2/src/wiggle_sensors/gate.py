import time
from gpiozero import Button
from datetime import datetime
from .write import write_to_csv

SENSOR_PIN = 17

def listen_and_write_gate():
    sensor = Button(SENSOR_PIN)

    try:
        while True:
            reading = not sensor.is_pressed
            sensor_data = {
                "time": datetime.now().isoformat(),
                "status": reading
            }
            fieldnames = ["time", "status"]

            if reading:
                write_to_csv(sensor_data, 'wiggle-gate', fieldnames)

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    listen_and_write_gate()
