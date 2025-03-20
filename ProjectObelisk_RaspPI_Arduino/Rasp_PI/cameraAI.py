from PIL import Image
import scipy.signal as sg
import sys
import numpy as np

def color_test(average, c_averages, cur_off_count, avg, c_avgs, off_count, o_ep, c_ep, oc_ep):
    if average < avg + o_ep and average > avg - o_ep:
        if c_averages[0] < c_avgs[0] + c_ep and c_averages[0] > c_avgs[0] - c_ep and c_averages[1] < c_avgs[1] + c_ep and c_averages[1] > c_avgs[1] - c_ep and c_averages[2] < c_avgs[2] + c_ep and c_averages[2] > c_avgs[2] - c_ep and cur_off_count < off_count + oc_ep and cur_off_count > off_count - oc_ep:
            return True
        else:
            return False
    else:
        return False

def identify_whites(img):
    # Resize image and format it properly
    # print("Filename:", os.path.basename(img.filename), " RGB: ", end=" ")
    modded_img = img.rotate(90, Image.NEAREST, expand = 1)
    modded_img = modded_img.resize((320, 240))
    pixels = np.array(modded_img)

    # OLD WHITESPACE DETECTION METHOD
    for i in range(240):
        for j in range(320):
            if pixels[i][j][0] > 170 and pixels[i][j][1] > 170 and pixels[i][j][2] > 170:
                pixels[i][j] = [0,0,0]


    #building filters and convolving the image
    conv_pixels = pixels[:, :, 0]
    conv_pixels = conv_pixels.astype(np.int16)
    noise_filter = np.array([[2,4,5,4,2],[4,9,12,9,4],[5,12,15,12,5],[4,9,12,9,4],[2,4,5,4,2]])
    edge = np.array([
        [-1, -1, -1], 
        [-1, 32, -1], 
        [-1, -1, -1]])
    results =  sg.convolve(conv_pixels, noise_filter, mode='same')
    results = sg.convolve(results, edge, mode='same')
    results[results > 255] = 255
    results[results < 0] = 0
    results = results.astype(np.uint8)

    # repackage results to highlight detected edges
    new_img = np.zeros((240, 320, 3))
    off_count = 0
    for row in range(240):
        for col in range(320):
            if(results[row][col] == 0):
                new_img[row][col][0] = 255
                new_img[row][col][1] = 0
                new_img[row][col][2] = 255
                off_count+=1
            else:
                new_img[row][col][0] = pixels[row][col][0]
                new_img[row][col][1] = pixels[row][col][1]
                new_img[row][col][2] = pixels[row][col][2]
    
    # Obtain the average colors
    object_pixel_count = 320*240 - off_count
    r_avg = 0.0
    g_avg = 0.0
    b_avg = 0.0
    for row in new_img:
        for pixel in row:
            if not (pixel[0] == 255 and pixel[1] == 0 and pixel[2] == 255):
                r_avg+= float(pixel[0])/object_pixel_count
                g_avg+= float(pixel[1])/object_pixel_count
                b_avg+= float(pixel[2])/object_pixel_count
    # print(r_avg, " ", g_avg, " ", b_avg, end= "-->")
    # print((r_avg+g_avg+b_avg))

    return (r_avg + g_avg + b_avg), [r_avg, g_avg, b_avg], off_count

def unpackage_images():
    training_one = Image.open('/home/bnigg17/Documents/ECE395/Obelisk_RaspPI/training_1.png')
    training_two = Image.open('/home/bnigg17/Documents/ECE395/Obelisk_RaspPI/training_2.png')

    training_pictures = [training_one, training_two]

    return training_pictures


def decide(capture):
    training_pictures = unpackage_images()
    
    color_avg1, color_avgs1, off_count1= identify_whites(training_pictures[0])
    color_avg2, color_avgs2, off_count2= identify_whites(training_pictures[1])
    color_avg, color_avgs, off_count = (color_avg1+color_avg2)/2, [(color_avgs1[0]+color_avgs2[0])/2, (color_avgs1[1]+color_avgs2[1])/2, (color_avgs1[2]+color_avgs2[2])/2], (off_count1 + off_count2)/2
    color_epsilon = max([abs(color_avgs1[0]-color_avgs2[0]), abs(color_avgs1[1]-color_avgs2[1]), abs(color_avgs1[2]-color_avgs2[2])]) + 5
    overall_epsilon = abs(color_avg1 - color_avg2) + 5
    off_count_epsilon = abs(off_count1 - off_count2) + 5000
    print("color_avg :", color_avg)
    print("color_avgs :", color_avgs)
    print("off_count :", off_count)
    print("color_ep :", color_epsilon)
    print("overall_ep :", overall_epsilon)
    print("off_cnt_ep :", off_count_epsilon)
   
    # identify color averages for the current capture, with some protection
    average, c_averages, cur_off_count = 0, [0,0,0], 0
    try:
        average, c_averages, cur_off_count = identify_whites(capture)
    except Exception as e:
        if e == KeyboardInterrupt:
            sys.exit(1)
        print("Edge detection and color average capture failed")
    
    print("avg :", average)
    print("c_avgs :", c_averages)
    print("cur_off_counts :", cur_off_count)
    
    # test the captured image
    if color_test(average, c_averages, cur_off_count, color_avg, color_avgs, off_count, overall_epsilon, color_epsilon, off_count_epsilon):
        return True
    else:
        return False
        
