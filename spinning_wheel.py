import board
import time
import digitalio
import pwmio

# ---------------- SETUP -------------------

# Motor direction control
in1 = digitalio.DigitalInOut(board.D2)
in1.direction = digitalio.Direction.OUTPUT

in2 = digitalio.DigitalInOut(board.D3)
in2.direction = digitalio.Direction.OUTPUT

# PWM for motor speed
pwm = pwmio.PWMOut(board.D6, frequency=1000)

# Buttons
touch_button = digitalio.DigitalInOut(board.D7)
touch_button.direction = digitalio.Direction.INPUT

roulette_button = digitalio.DigitalInOut(board.D4)
roulette_button.direction = digitalio.Direction.INPUT

# Hall sensor
hall_sensor = digitalio.DigitalInOut(board.D8)
hall_sensor.direction = digitalio.Direction.INPUT
hall_sensor.pull = digitalio.Pull.UP

# LEDs
led_red = digitalio.DigitalInOut(board.D9)
led_red.direction = digitalio.Direction.OUTPUT

led_green = digitalio.DigitalInOut(board.D10)
led_green.direction = digitalio.Direction.OUTPUT

# Motor direction setup
in1.value = True
in2.value = False

# ---------------- FUNCTIONS -------------------

def set_led_color(color):
    if color == "green":
        led_red.value = False
        led_green.value = True
    elif color == "red":
        led_red.value = True
        led_green.value = False
    else:
        led_red.value = False
        led_green.value = False

def spin_motor_and_decelerate():
    speed = 65535
    pwm.duty_cycle = speed
    print("Wheel spinning...")

    while speed > 7500:
        pwm.duty_cycle = speed
        time.sleep(0.2)
        speed = int(speed * 0.95)

    pwm.duty_cycle = 0
    print("Wheel stopped.")

# ---------------- MAIN LOOP -------------------

while True:
    if touch_button.value:  # Normal mode
        spin_motor_and_decelerate()

        # Wait for release
        while touch_button.value:
            time.sleep(0.1)

        time.sleep(1) 

    elif roulette_button.value:  # Roulette mode
        spin_motor_and_decelerate()

        # Check Hall sensor
        aligned = hall_sensor.value == 0
        if aligned:
            set_led_color("green")
        else:
            set_led_color("red")

        time.sleep(3)  # Show result

        # Wait for release
        while roulette_button.value:
            time.sleep(0.1)

        time.sleep(1)  # Cooldown
