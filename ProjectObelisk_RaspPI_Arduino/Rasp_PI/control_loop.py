from PIL import Image
import scipy.signal as sg
import sys
import numpy as np
import serial
import os
from cameraAI import *  # Import custom AI-related functions
from gpio import *  # Import custom GPIO control functions
from uart import *  # Import custom UART-related functions

def main():
    """
    Main function to control a servo and LED system based on button inputs and AI decisions.
    It initializes devices, enters an infinite loop to handle button events, and controls
    LEDs and servo movements according to the logic.
    """
    GPIO.cleanup()  # Ensure clean GPIO state before starting
    
    # Initialize devices
    pwm = init_servo()  # Initialize servo motor
    control_servo(pwm, 0)  # Ensure servo starts in the locked position
    init_button()  # Set up buttons
    init_LED()  # Set up LEDs
    
    # Flash all LEDs for initialization indication
    set_LED(GREEN_LED_PIN, 1)
    set_LED(RED_LED_PIN, 1)
    set_LED(BLUE_LED_PIN, 1)
    time.sleep(2)
    set_LED(GREEN_LED_PIN, 0)
    set_LED(RED_LED_PIN, 0)
    set_LED(BLUE_LED_PIN, 0)
    
    # Main loop to process button inputs and control devices
    while True:
        try:
            # Wait for a button press and get the button index
            button_key = wait_for_button()
            print("Button pressed:", button_key)
            
            if button_key == 0:  # Run AI model on captured image
                set_LED(GREEN_LED_PIN, 0)
                set_LED(RED_LED_PIN, 0)
                set_LED(BLUE_LED_PIN, 1)  # Indicate capture in progress
                capture = request_capture()  # Capture an image
                
                if decide(capture):  # Use AI model to decide on the capture
                    # Capture accepted: Unlock and indicate success
                    set_LED(GREEN_LED_PIN, 1)
                    set_LED(RED_LED_PIN, 0)
                    control_servo(pwm, 180)  # Unlock position
                    time.sleep(5)
                    control_servo(pwm, 0)  # Lock position
                    set_LED(GREEN_LED_PIN, 0)
                    set_LED(RED_LED_PIN, 1)
                else:
                    # Capture rejected: Indicate failure with blinking red LED
                    set_LED(RED_LED_PIN, 1)
                    set_LED(GREEN_LED_PIN, 0)
                    for _ in range(3):
                        time.sleep(0.5)
                        set_LED(RED_LED_PIN, 0)
                        time.sleep(0.5)
                        set_LED(RED_LED_PIN, 1)
                    control_servo(pwm, 0)  # Ensure servo remains locked
                
                set_LED(BLUE_LED_PIN, 0)  # Turn off blue LED
            
            elif button_key == 1:  # Retrain training image 1
                set_LED(GREEN_LED_PIN, 0)
                set_LED(RED_LED_PIN, 0)
                set_LED(BLUE_LED_PIN, 1)  # Indicate capture in progress
                capture = request_capture()  # Capture an image
                capture.save("/home/bnigg17/Documents/ECE395/Obelisk_RaspPI/training_1.png")  # Save image
                set_LED(GREEN_LED_PIN, 0)
                set_LED(RED_LED_PIN, 1)  # Indicate success
                set_LED(BLUE_LED_PIN, 0)
            
            elif button_key == 2:  # Retrain training image 2
                set_LED(GREEN_LED_PIN, 0)
                set_LED(RED_LED_PIN, 0)
                set_LED(BLUE_LED_PIN, 1)  # Indicate capture in progress
                capture = request_capture()  # Capture an image
                capture.save("/home/bnigg17/Documents/ECE395/Obelisk_RaspPI/training_2.png")  # Save image
                set_LED(GREEN_LED_PIN, 0)
                set_LED(RED_LED_PIN, 1)  # Indicate success
                set_LED(BLUE_LED_PIN, 0)
        
        except KeyboardInterrupt:
            # Handle keyboard interrupt (Ctrl+C) to exit the program
            print("Keyboard interrupt detected. Exiting...")
            pwm.stop()  # Stop the PWM signal
            GPIO.cleanup()  # Reset GPIO settings to default state
            break


if __name__ == "__main__":
    """
    Entry point for the script. Calls the main function to start the program.
    """
    main()
