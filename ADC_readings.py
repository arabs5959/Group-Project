
from machine import ADC, Pin
import time
adc = ADC(Pin(26))  # Create an ADC object on pin 26
for adc_readings in range(12):
    raw_value += adc.read_u16()  # Read the raw ADC value (0-65535)
    average = raw_value / 12  # Calculate the average reading
    print("ADC Reading:", average)
    time.sleep(0.5)
    