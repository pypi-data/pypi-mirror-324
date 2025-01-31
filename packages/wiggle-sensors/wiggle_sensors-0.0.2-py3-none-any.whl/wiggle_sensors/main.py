import argparse
from wiggle_sensors.environment import write_bme680
from wiggle_sensors.soil_temperature import write_DS18B20
from wiggle_sensors.soil_moisture import write_soil_moisture

def main():
    parser = argparse.ArgumentParser(
        prog="WiggleSensors", description="Control the sensors on WiggleBin"
    )

    parser.add_argument(
        "--write",
        nargs="+",
        help="Read sensor data for specified environment and sensor type",
        choices=["environment", "soil-temperature", "soil-moisture"]
    )

    args = parser.parse_args()

    if args.write:
        if len(args.write) == 0:
            write_bme680()
            write_DS18B20()
            write_soil_moisture()
        else:
            for sensor in args.write:
                if sensor == "environment":
                    write_bme680()
                if sensor == "soil-temperature":
                    write_DS18B20()
                if sensor == "soil-moisture":
                    write_soil_moisture()

if __name__ == "__main__":
    main()
