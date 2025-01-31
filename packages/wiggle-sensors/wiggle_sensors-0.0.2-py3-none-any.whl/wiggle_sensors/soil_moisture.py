import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from datetime import datetime
from wiggle_sensors.write import write_to_csv

# Initialize the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create an ADS1115 instance
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Calibration values (replace these with your actual measurements)
dry_value = 16700  # ADC value for dry soil
wet_value = 6270  # ADC value for wet soil

def get_soil_moisture_percentage(adc_value):
    # Map the ADC value to a percentage
    if adc_value > dry_value:
        adc_value = dry_value
    if adc_value < wet_value:
        adc_value = wet_value
    moisture_percentage = 100 * (dry_value - adc_value) / (dry_value - wet_value)

    return round(moisture_percentage, 2)

def read_soil_moisture():
    """Reads the soil moisture"""

    # Read the ADC value
    adc_value = chan.value

    # Calculate the soil moisture percentage
    moisture_percentage = get_soil_moisture_percentage(adc_value)
        
    # Print the results
    print(f'ADC Value: {adc_value}')
    print(f'Soil Moisture: {moisture_percentage:.2f}%')

    return {
        "time": datetime.now().isoformat(),
        "percentage": moisture_percentage,
        "adc": adc_value,
        "dry_value": dry_value,
        "wet_value": wet_value
    }

def write_soil_moisture():
    """Write the soil moisture to CSV"""
    sensor_data = read_soil_moisture()
    fieldnames = ["time", "percentage", "adc", "dry_value", "wet_value"]
    write_to_csv(sensor_data, "soil-moisture", fieldnames)

if __name__ == "__main__":
    read_soil_moisture()
