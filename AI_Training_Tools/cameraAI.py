from PIL import Image
import scipy.signal as sg
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

def color_test(average, c_averages, cur_off_count, avg, c_avgs, off_count, o_ep, c_ep, oc_ep):
    if average < avg + o_ep and average > avg - o_ep:
        if c_averages[0] < c_avgs[0] + c_ep and c_averages[0] > c_avgs[0] - c_ep and c_averages[1] < c_avgs[1] + c_ep and c_averages[1] > c_avgs[1] - c_ep and c_averages[2] < c_avgs[2] + c_ep and c_averages[2] > c_avgs[2] - c_ep and cur_off_count < off_count + oc_ep and cur_off_count > off_count - oc_ep:
            return True
        else:
            return False
    else:
        return False

def identify_whites(img, p_flag):
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
    
    # Recreate modified image and show it
    if(p_flag):
        new_img = Image.fromarray(new_img.astype('uint8'), 'RGB')
        # new_img.show()

    return (r_avg + g_avg + b_avg), [r_avg, g_avg, b_avg], off_count

def unpackage_images():
    horiz_iphone_img = Image.open('C:\\Users\\bebom\\Desktop\\ECE395\\camera_AI\\data\\iphone_horiz.jpg')
    diag_iphone_img = Image.open('C:\\Users\\bebom\\Desktop\\ECE395\\camera_AI\\data\\iphone_diag.jpg')  
    otterbox_img = Image.open('C:\\Users\\bebom\\Desktop\\ECE395\\camera_AI\\data\\otterbox.jpg')
    servo_box_img = Image.open('C:\\Users\\bebom\\Desktop\\ECE395\\camera_AI\\data\\servo_box.jpg')
    ct_tool_img = Image.open('C:\\Users\\bebom\\Desktop\\ECE395\\camera_AI\\data\\ct_tool.jpeg')
    diag_ben_phone_img = Image.open('C:\\Users\\bebom\\Desktop\\ECE395\\camera_AI\\data\\diag_ben_phone.jpeg')
    hand_img = Image.open('C:\\Users\\bebom\\Desktop\\ECE395\\camera_AI\\data\\hand.jpeg')
    horiz_ben_phone_img = Image.open('C:\\Users\\bebom\\Desktop\\ECE395\\camera_AI\\data\\horiz_ben_phone.jpeg')
    orange_img = Image.open('C:\\Users\\bebom\\Desktop\\ECE395\\camera_AI\\data\\orange.jpeg')
    new_braden_iphone = Image.open('C:\\Users\\bebom\\Desktop\\ECE395\\camera_AI\\data\\new_braden_iphone.jpg')
    blue_cube_training_one = Image.open('C:\\Users\\bebom\\Desktop\\ECE395\\camera_AI\\data\\blue_cube_1.png')
    blue_cube_training_two = Image.open('C:\\Users\\bebom\\Desktop\\ECE395\\camera_AI\\data\\blue_cube_2.png')
    blue_cube_test = Image.open('C:\\Users\\bebom\\Desktop\\ECE395\\camera_AI\\data\\blue_cube_test.png')

    training_pictures = [blue_cube_training_one, blue_cube_training_two]
    pictures = [
                blue_cube_training_one,
                blue_cube_training_two,
                blue_cube_test,
                horiz_iphone_img, 
                diag_iphone_img, 
                new_braden_iphone,
                horiz_ben_phone_img,
                diag_ben_phone_img,
                otterbox_img, 
                servo_box_img,
                ct_tool_img,
                hand_img,
                orange_img
    ]

    rootdir = "C:/Users/bebom/Desktop/ECE395/camera_AI/white_background_fakes"
    for subdir, dir, files in os.walk(rootdir):
        for file in files:
            pictures.append(Image.open(os.path.join(subdir, file)))

    return pictures, training_pictures



def main():
    pictures, training_pictures = unpackage_images()
    
    color_avg1, color_avgs1, off_count1= identify_whites(training_pictures[0], True)
    color_avg2, color_avgs2, off_count2= identify_whites(training_pictures[1], True)
    color_avg, color_avgs, off_count = (color_avg1+color_avg2)/2, [(color_avgs1[0]+color_avgs2[0])/2, (color_avgs1[1]+color_avgs2[1])/2, (color_avgs1[2]+color_avgs2[2])/2], (off_count1 + off_count2)/2
    color_epsilon = max([abs(color_avgs1[0]-color_avgs2[0]), abs(color_avgs1[1]-color_avgs2[1]), abs(color_avgs1[2]-color_avgs2[2])]) + 0.1
    overall_epsilon = abs(color_avg1 - color_avg2) + 0.1
    off_count_epsilon = abs(off_count1 - off_count2) + 5000
    print("color_epsilon: ", color_epsilon)
    print("overall_ep: ", overall_epsilon)
    print("off_count_ep: ", off_count_epsilon)

    # Allows me to analyze the color average differences data after whitespace removal 
    figure, axis = plt.subplots(2, 2)
    picture_count = 0
    o_averages, r_averages, g_averages, b_averages = [], [], [], []
    accepted_images = []
   
    for picture in pictures:
        p_flag = True if picture_count % 100 == 0 else False
        # p_flag = False
        average, c_averages, cur_off_count = 0, [0,0,0], 0
        try:
            average, c_averages, cur_off_count = identify_whites(picture, p_flag)
        except Exception as e:
            if e == KeyboardInterrupt:
                sys.exit(1)
            print("Edge detection failed for ", str(picture))

        o_averages.append(average)
        r_averages.append(c_averages[0])
        g_averages.append(c_averages[1])
        b_averages.append(c_averages[2])

        if color_test(average, c_averages, cur_off_count, color_avg, color_avgs, off_count, overall_epsilon, color_epsilon, off_count_epsilon):
            print("Accepted Image Filename:", os.path.basename(picture.filename))
            accepted_images.append(picture)
        else:
            print("Denied Image Filename:", os.path.basename(picture.filename))
        picture_count += 1

    print(len(accepted_images), " accepted, out of ~1013 images, only 3 should be accepted.")
    for img in accepted_images:
        print("accepted image: ", str(img))

    # Naming the different color average plots
    axis[0,0].set_title("Overall Color Averages")
    axis[0,1].set_title("Red Color Averages")
    axis[1,0].set_title("Green Color Averages")
    axis[1,1].set_title("Blue Color Averages")

    # Fake pictures (should be rejected)
    axis[0,0].scatter(o_averages[3:], o_averages[3:], c="red")
    axis[0,1].scatter(r_averages[3:], r_averages[3:], c="red")
    axis[1,0].scatter(g_averages[3:], g_averages[3:], c="red")
    axis[1,1].scatter(b_averages[3:], b_averages[3:], c="red")

    # The 1st Training image
    axis[0,0].scatter(o_averages[0], o_averages[0], c="green")
    axis[0,1].scatter(r_averages[0], r_averages[0], c="green")
    axis[1,0].scatter(g_averages[0], g_averages[0], c="green")
    axis[1,1].scatter(b_averages[0], b_averages[0], c="green")

    # The 2nd Training image
    axis[0,0].scatter(o_averages[1], o_averages[1], c="green")
    axis[0,1].scatter(r_averages[1], r_averages[1], c="green")
    axis[1,0].scatter(g_averages[1], g_averages[1], c="green")
    axis[1,1].scatter(b_averages[1], b_averages[1], c="green")

    # The Training object in Non-Training images
    axis[0,0].scatter(o_averages[2], o_averages[2], c="blue")
    axis[0,1].scatter(r_averages[2], r_averages[2], c="blue")
    axis[1,0].scatter(g_averages[2], g_averages[2], c="blue")
    axis[1,1].scatter(b_averages[2], b_averages[2], c="blue")

    plt.show()

    return


if __name__ == "__main__":
    main()