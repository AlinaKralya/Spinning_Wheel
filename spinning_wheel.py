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
touch_button = digitalio.DigitalInOut(board.D7)
touch_button.direction = digitalio.Direction.INPUT

# Hall Magnetic sensor
hall_sensor = digitalio.DigitalInOut(board.D8)
hall_sensor.direction = digitalio.Direction.INPUT
hall_sensor.pull = digitalio.Pull.UP

# LEDs
led_red = digitalio.DigitalInOut(board.D9)
led_red.direction = digitalio.Direction.OUTPUT

led_green = digitalio.DigitalInOut(board.D10)
led_green.direction = digitalio.Direction.OUTPUT

led_blue = digitalio.DigitalInOut(board.D11)
led_blue.direction = digitalio.Direction.OUTPUT

'''
    Set direction:
    IN1 and IN2 == False           --> Motor OFF
    IN1 == True and IN2 == False   --> Forward
    IN1 == False and IN2 == True   --> Backwards
    IN1 and IN2 == True            --> Motor OFF
'''
in1.value = True
in2.value = False

time_passed = time.monotonic()

# --------------- FUNCTIONS ----------------

def spin_motor_and_decelerate():
    speed = 65535
    pwm.duty_cycle = speed

    while speed > 7500:
        pwm.duty_cycle = speed
        time.sleep(0.2)
        speed = int(speed * 0.95)

    pwm.duty_cycle = 0

def set_led_color(color):
    if color == "green":
        led_green.value = True
        led_red.value = False
    elif color == "red":
        led_green.value = False
        led_red.value = True
    else:
        led_red.value = False
        led_green.value = False 


# --------------- MAIN LOOP ----------------
while True:
    if touch_button.value:
        press_start = time.monotonic()

        # Blink LED while holding the button
        while touch_button.value:
            led_blue.value = True
            time.sleep(0.25)
            led_blue.value = False
            time.sleep(0.25)

        press_duration = time.monotonic() - press_start

        if press_duration >= 1.0:
            # Roulette mode
            spin_motor_and_decelerate()

            time.sleep(1.0)  # give wheel time to settle

            aligned = hall_sensor.value == 0
            if aligned:
                set_led_color("green")
            else:
                set_led_color("red")

            time.sleep(3)  # Show result
        else:
            # Trivia
            spin_motor_and_decelerate()

        # Turn off LEDs and cooldown
        set_led_color("off")
        time.sleep(1)
