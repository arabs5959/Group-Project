from machine import ADC, Pin
import time

# Create an ADC object on pin 26
adc = ADC(Pin(26))  

def get_reading():
    raw_value = 0  # Initialize the variable to 0 first!
    
    for _ in range(12):
        raw_value = adc.read_u16()  # Accumulate the raw 16-bit values (0-65535)
        time.sleep(0.05)             # Shorter sleep so taking an average doesn't take 6 full seconds
        
    average = int(raw_value / 12)    # Calculate the average and convert to a whole integer
    print("Calculated Average ADC Reading:", average)
    return average

    