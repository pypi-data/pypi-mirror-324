# WiggleSensors

## Preparing Raspberry Pi

### For soil temperature - ds18b20

You will need to enable the Raspberry PI to gather ds18b20 data

https://raspberrytips.nl/ds18b20-raspberry-pi/

### For soil moisture sensor

To calibrate a soil moisture sensor using the ADS1115, you need to determine the sensor's output values for both dry and wet soil conditions. These values will help you map the raw ADC readings to meaningful soil moisture percentages.

Step-by-Step Plan:
1. Measure the sensor output in dry soil: Record the ADC value when the sensor is in completely dry soil.
2. Measure the sensor output in wet soil: Record the ADC value when the sensor is in completely saturated soil.
3. Map the ADC values to moisture percentages: Use the recorded dry and wet values to create a function that converts ADC readings to soil moisture percentages.

## Via CLI

Run `wiggle-sensors -h` to see options for viewing sensor data such as temperature, gas, pressure and humidity from bme680 and DS18B20 sensor.

```
wiggle-sensors -h
```

## Installation for development

Installing package
```
pip3 install .
```

For installation without dev dependencies
```
pip install --no-dev -r requirements.txt
```