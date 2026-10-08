import time
from machine import Pin, UART, PWM

# 1. Setup UART Serial to match the sender (TX=Pin 0, RX=Pin 1)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# 2. Setup local PWM output on Pin 15 at 1kHz to replicate the signal
pwm = PWM(Pin(15))
pwm.freq(1000)

print("Receiver is online, waiting for ADC data...")

while True:
    if uart.any():
        # Read the incoming line of data and clean it up
        raw_data = uart.readline()
        try:
            # Decode bytes to string and remove newline characters
            decoded_str = raw_data.decode('utf-8').strip()
            
            # Convert the incoming string directly to a 16-bit integer ADC value
            received_adc = int(decoded_str)
            print(f"Received target ADC value: {received_adc}")
            
            # 3. Apply the 16-bit value directly to the hardware register
            pwm.duty_u16(received_adc) 
            
            # Read back the applied value for confirmation
            applied_val = pwm.duty_u16()
            new_duty = (applied_val / 65535) * 100  
            print(f"Applied hardware register value: {applied_val}")
            print(f"Equivalent duty cycle: {new_duty:.1f}%")

            # 4. Send back a confirmation result to the sender
            time.sleep(0.1) # Small pause to let UART clear
            confirmation_msg = f"SUCCESS: Applied ADC value {received_adc}\n"
            uart.write(confirmation_msg)
            print("Sent confirmation back to sender.")
            
        except Exception as e:
            print(f"Error processing received data: {e}")
            uart.write(f"ERROR: Invalid data received\n")                
    time.sleep(0.1)
