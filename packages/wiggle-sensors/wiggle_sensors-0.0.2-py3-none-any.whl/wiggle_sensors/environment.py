import time
import board
import adafruit_bme680
from datetime import datetime
from wiggle_sensors.write import write_to_csv

def read_bme680():
    i2c = board.I2C()
    bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)
    
    # change this to match the location's pressure (hPa) at sea level
    bme680.sea_level_pressure = 997

    # You will usually have to add an offset to account for the temperature of
    # the sensor. This is usually around 5 degrees but varies by use. Use a
    # separate temperature sensor to calibrate this one.
    temperature_offset = 0

    # Take an initial reading and discard it
    initial_temperature = bme680.temperature
    initial_humidity = bme680.humidity
    initial_pressure = bme680.pressure
    initial_gas = bme680.gas

    print("Starting sensor...")

    time.sleep(2)

    print("\nTemperature: %0.1f C" % (bme680.temperature + temperature_offset))
    print("Gas: %d ohm" % bme680.gas)
    print("Humidity: %0.1f %%" % bme680.relative_humidity)
    print("Pressure: %0.3f hPa" % bme680.pressure)
    print("Altitude = %0.2f meters" % bme680.altitude)

    return {
        "time": datetime.now().isoformat(),
        "temperature": bme680.temperature + temperature_offset, 
        "humidity": bme680.relative_humidity,
        "pressure": bme680.pressure,
        "altitude": bme680.altitude,
    }

def write_bme680():
    sensor_data = read_bme680()
    fieldnames = ["time", "temperature", "humidity", "pressure", "altitude"]
    write_to_csv(sensor_data, "bme680", fieldnames)

if __name__ == "__main__":
    write_bme680()