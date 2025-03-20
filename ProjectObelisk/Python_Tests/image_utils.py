import serial
from PIL import Image
import numpy as np
import time
import os

def display_rgb565_image(rgb888_data, width, height, filename):
    """Convert the list of RGB888 tuples to an image and save it."""
    pixels = np.array(rgb888_data, dtype=np.uint8).reshape((height, width, 3))
    img = Image.fromarray(pixels, 'RGB')
    img.show()
    img.save(filename)

def clean(data, num_pixels):
    rgb_888 = []
    for i in range(0, num_pixels):
        red = int(data[3*i])
        green = int(data[3*i+1])
        blue = int(data[3*i+2])
        rgb = [red, green, blue]
        rgb_888.append(rgb)
    test_rgb888(rgb_888)
    return rgb_888

# def clean(data, num_pixels):
#     raw_data = []
#     for i in range(0, num_pixels):
#         byte0 = data[2*i]
#         byte1 = data[2*i+1]
#         pixel = [byte0, byte1]
#         raw_data.append(pixel)
#     return raw_data

def test_rgb888(image):
    for pixel in image:
        if pixel[0] > 255 or pixel[0] < 0:
            print("ERROR RED")
        if pixel[1] > 255 or pixel[1] < 0:
            print("ERROR GREEN")
        if pixel[2] > 255 or pixel[2] < 0:
            print("ERROR BLUE")

# Replace 'COMx' with your port and set your baud rate
ser = serial.Serial('/dev/ttyUSB0', 3000000, timeout=3)
# Ensure the directory for results exists
output_directory = "test_results"
os.makedirs(output_directory, exist_ok=True)

width = 176
height = 144
num_bytes_to_read = width * height * 3
#num_bytes_to_read = width * height * 2

while True:
    # Prompt user for test input
    ser.reset_input_buffer()   # Clears the input buffer
    ser.reset_output_buffer()  # Clears the output buffer
    test_number = input("Enter the test number to run (or 'q' to quit): ")
    if test_number.lower() == 'q':
        print("Exiting program.")
        break

    if not test_number.isdigit():
        print("Please enter a valid number.")
        continue

    # Generate filenames for the image and text output in the test_results directory
    image_filename = os.path.join(output_directory, f"image_test_{test_number}.png")
    text_filename = os.path.join(output_directory, f"raw_rgb565_test_{test_number}.txt")

    # Send the test number to the MCU
    ser.write(int(test_number).to_bytes(1, 'little') + b'\n')  # Send test number followed by newline

    print("Waiting for start character ('S') from MCU...") 
    time.sleep(.1)  # Allow time MCU
    while True:
        byte = ser.read(1).decode('utf-8', errors='ignore')
        if byte == 'S':
            break  # Start character detected, exit loop
            
    print("Snapshot in progress...")
    # Now read the specified number of bytes
    data = ser.read(num_bytes_to_read)
    print(f"Received {len(data)} bytes, test number: {test_number}.")
    #print(data)
    if len(data) != num_bytes_to_read:
        print(data[1:5])    # Prints b'Fail', indicates invalid number
        print('UART ERROR')
    else:
        # Process the received data
        image = clean(data, num_bytes_to_read // 3)
        #image = clean(data, num_bytes_to_read // 2)
        print(f"Cleaned image size: {len(image)} = {width}x{height}, test number: {test_number}")

        # Write image data to text file
        with open(text_filename, 'w') as f:
            for row in range(height):
                row_string = ''
                for col in range(width):  # Process exactly 320 pixels per row
                    pixel = image[row * width + col]  # Get the pixel
                    r, g, b = pixel  # Unpack the RGB values
                    row_string += f"({r},{g},{b}) "  # Add the formatted pixel to the row string
                    # byte0, byte1 = pixel
                    # row_string += f'(0x{byte0:02X}{byte1:02X})'
                f.write(row_string.strip() + '\n')  # Write the row to file, stripping any trailing space

        print(f"Saved RGB data to {text_filename}.")

        # Display and save the image
        display_rgb565_image(image, width, height, image_filename)
        print(f"Saved image as {image_filename}.")
    
