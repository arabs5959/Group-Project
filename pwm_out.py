from machine import Pin, PWM

pwm = PWM(Pin(15))  # Create a PWM object on pin 15
pwm.freq(1000)  # Set the frequency to 1 kHz
pwm.duty_u16(32768)  # Set the duty cycle to 50% (32768 out of 65535)
stop()
