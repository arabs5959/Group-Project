import time
from machine import Pin, UART, PWM
# import and run pwm_out.py to initialize the pwm object
import pwm_out as x 
# import adc reader (removed the .py from the import statement)
import ADC_readings as adc_reader 

# Extract the duty cycle value that x.py set
current_u16 = x.pwm.duty_u16()
calculated_percent = (current_u16 / 65535) * 100

# Fetch the current ADC reading from your imported module
# Note: Replace 'get_reading()' with the actual function name inside your ADC_readings.py
adc_value = adc_reader.adc.read_u16() 

# Setup UART Serial for the cable (TX=GPIO0, RX=GPIO1 based on your pin mapping)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

print(f"Duty cycle: {calculated_percent:.1f}% ({current_u16})")
print(f"Sending ADC Value: {adc_value}")

# Transmit the ADC data across the cable
# Send multiple times with a small delay to guarantee arrival on boot
for _ in range(12):
    uart.write(f"{adc_value}\n")
    time.sleep(0.2)

print("Packet sent successfully.")

while True:
    if uart.any():
        # Read the incoming line of data and clean it up
        raw_data = uart.readline()
        try:
            # Decode bytes to string and remove newline characters
            decoded_str = raw_data.decode('utf-8').strip()
            print(f"Received confirmation: {decoded_str}")
        except Exception as e:
            print(f"Error processing received data: {e}")
