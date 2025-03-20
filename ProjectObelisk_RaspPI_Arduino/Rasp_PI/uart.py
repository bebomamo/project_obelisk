import serial
from PIL import Image
import numpy as np

# Converts a squashed array of bytes of image data into an array, and then a pillow image
# NOTE: bytes will be a flat array of size 153600<->FRAME_BUFFER_SIZE
def create_image_from_bytes(bytes):
    rgb = np.zeros((240,320,3), dtype=np.uint8)
    for i in range(320*240):
        byte_one = bytes[i*2][0]
        byte_two = bytes[i*2+1][0]

        r = (byte_one & 0xF8) >> 3 # top 5 bits
        g = ((byte_one & 0x07) << 3) | ((byte_two & 0xE0) >> 5) # middle 6 bits
        b = byte_two & 0x1F # last 5 bits

        r = (r<<3)|(r>>2)
        g = (g<<2)|(g>>4)
        b = (b<<3)|(b>>2)

        rgb[int(i/320)][i%320] = (r, g, b)

    img = Image.fromarray(rgb, 'RGB')
    return img

def request_capture():
    # Replace 'COMx' with your port and set your baud rate
    # '/dev/tyyXXXX' for linux
    ser = serial.Serial('/dev/ttyACM0', 500_000, timeout=1)

    FRAME_BUFFER_SIZE = 320*240*2
    IN_BETWEEN_SIZE = 18
    NUM_FRAMES_READ = 7  # change its size to see different results

    print("UART ready for transmition")

    byte_counter = 0
    current_frame = 0
    cur_frame_index = 0
    sync_counter = 0
    within_frame_flag = False
    vsync_buffer = []
    buffer = []
    frames = {}
    for i in range(NUM_FRAMES_READ):
        frames[i+1] = []

    while True:
        try:
            byte = ser.read(1)
            
            # Check if any data is received
            if byte:
                byte_counter+=1
                buffer.append(byte)
                if(byte_counter >= 7):
                    vsync_buffer = buffer[byte_counter-7:byte_counter]
                    # Synchronization Bytes to identify new frame
                    if(vsync_buffer[0] == b'\x00' 
                    and vsync_buffer[1] == b'\x04'
                    and vsync_buffer[2] == b'\x11'
                    and vsync_buffer[3] == b'\x40'
                    and vsync_buffer[4] == b'\xf0'
                    and vsync_buffer[5] == b'\x11'
                    and vsync_buffer[6] == b'\xb0'):
                        #vsync section found
                        within_frame_flag = True
                        current_frame += 1

                # Try to add to current frame buffer
                if(within_frame_flag):
                    if(sync_counter > 5):
                        cur_frame_index += 1
                        if(current_frame <= NUM_FRAMES_READ):
                            frames[current_frame].append(byte)
                        if(cur_frame_index >= 153600):
                            cur_frame_index = 0
                            within_frame_flag = False
                            sync_counter = 0
                    else:
                        sync_counter+=1
                
                if(byte_counter == (FRAME_BUFFER_SIZE + IN_BETWEEN_SIZE) * NUM_FRAMES_READ):
                    break
        
        except serial.SerialException as e:
            print(f"Serial error: {e}")
            break
        except KeyboardInterrupt:
            print("User interrupted.")
            break

    # Close the serial connection
    ser.close()

    new_img = create_image_from_bytes(frames[6]) #CAPTURE 6
    return new_img
    
