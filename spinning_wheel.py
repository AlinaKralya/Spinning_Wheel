# --------------- LIBRARIES ----------------
import board
import time
import digitalio
import pwmio

# ---------------- SETUP -------------------

# Motor Pins to control direction (IN1 and IN2)
in1 = digitalio.DigitalInOut(board.D2)
in1.direction = digitalio.Direction.OUTPUT

in2 = digitalio.DigitalInOut(board.D3)
in2.direction = digitalio.Direction.OUTPUT

# PWM on ENA pin to control the speed
pwm = pwmio.PWMOut(board.D6, frequency=1000)

# Touch Sensor for digital input
touch = digitalio.DigitalInOut(board.D7)
touch.direction = digitalio.Direction.INPUT

'''
    Set direction:
    IN1 and IN2 == False           --> Motor OFF
    IN1 == True and IN2 == False   --> Forward
    IN1 == False and IN2 == True   --> Backwards
    IN1 and IN2 == True            --> Motor OFF
'''
in1.value = True
in2.value = False

# --------------- MAIN LOOP ----------------
while True:
    if touch.value:  # Sensor outputs HIGH when touched

        # Start at the full speed
        speed = 65535
        pwm.duty_cycle = speed

        # Speed can be changed, but my motor doesn't move after ~7500
        while speed > 7500:
            pwm.duty_cycle = speed
            time.sleep(0.2) # For smooth slow down
            speed = int(speed * 0.95) # Motor loses 5% of it's speed every loop

        # Full Stop
        pwm.duty_cycle = 0

        # Wait until sensor is released
        while touch.value:
            time.sleep(0.1)

        time.sleep(1)  # Cooldown before next touch