import RPi.GPIO as GPIO
import time

# Pin configuration
SERVO_PIN = 12      # GPIO pin connected to the servo motor
BUTTON_PIN_1 = 16   # GPIO pin connected to button 1
BUTTON_PIN_2 = 23   # GPIO pin connected to button 2
BUTTON_PIN_3 = 24   # GPIO pin connected to button 3
GREEN_LED_PIN = 17  # GPIO pin connected to the green LED
RED_LED_PIN = 27    # GPIO pin connected to the red LED
BLUE_LED_PIN = 22   # GPIO pin connected to the blue LED

def init_servo():
    """
    Initializes the servo motor by setting up the GPIO pin as output
    and starting PWM with a frequency of 50Hz.
    Returns:
        pwm (GPIO.PWM): The PWM instance for controlling the servo.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz frequency
    pwm.start(0)  # Start with a duty cycle of 0%
    return pwm

def control_servo(pwm, angle):
    """
    Moves the servo motor to the specified angle (0 or 180 degrees).
    Parameters:
        pwm (GPIO.PWM): The PWM instance controlling the servo.
        angle (int): The target angle (0 or 180 degrees).
    """
    if angle == 0:
        duty_cycle = 2.5  # Corresponds to 0 degrees
    elif angle == 180:
        duty_cycle = 12.5  # Corresponds to 180 degrees
    else:
        print('Invalid Angle')
        return
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)  # Wait for the servo to move
    pwm.ChangeDutyCycle(0)  # Stop sending PWM signal

def init_button():
    """
    Configures the GPIO pins connected to the buttons as input
    with pull-up resistors enabled.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_PIN_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(BUTTON_PIN_3, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def wait_for_button():
    """
    Waits for one of the three buttons to be pressed.
    Returns:
        int: The button index (0 for BUTTON_PIN_1, 1 for BUTTON_PIN_2, 2 for BUTTON_PIN_3).
    """
    try:
        while True:
            if GPIO.input(BUTTON_PIN_1) == GPIO.LOW:
                time.sleep(0.2)  # Debounce delay
                return 0
            if GPIO.input(BUTTON_PIN_2) == GPIO.LOW:
                time.sleep(0.2)  # Debounce delay
                return 1
            if GPIO.input(BUTTON_PIN_3) == GPIO.LOW:
                time.sleep(0.2)  # Debounce delay
                return 2
    except KeyboardInterrupt:
        print("Exiting program")

def init_LED():
    """
    Configures the GPIO pins connected to the LEDs as output.
    """
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
    GPIO.setup(RED_LED_PIN, GPIO.OUT)
    GPIO.setup(BLUE_LED_PIN, GPIO.OUT)

def set_LED(led_pin, en):
    """
    Turns an LED on or off based on the enable flag.
    Parameters:
        led_pin (int): The GPIO pin connected to the LED.
        en (bool): True to turn the LED on, False to turn it off.
    """
    if en:
        GPIO.output(led_pin, GPIO.LOW)  # Active low: turn LED on
    else:
        GPIO.output(led_pin, GPIO.HIGH)  # Active low: turn LED off

def shutdown(pwm):
    """
    Cleans up GPIO resources and stops PWM for safe shutdown.
    Parameters:
        pwm (GPIO.PWM): The PWM instance controlling the servo.
    """
    pwm.stop()  # Stop the PWM signal
    GPIO.cleanup()  # Reset GPIO settings to default state
