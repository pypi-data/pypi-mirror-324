from wiggle_sensors.environment import write_bme680
from wiggle_sensors.soil_temperature import write_DS18B20
# from wiggle_sensors.soil_moisture import write_soil_moisture

def main():
    write_bme680()
    write_DS18B20()
    # write_soil_moisture()

if __name__ == "__main__":
    main()