from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from PIL import ImageFilter
import matplotlib.lines as mlines
import sys

def apply_hough_transform(img, remove_noise=False):
    # input image is PIL image
    img_width, img_height = img.size
    height_cutoff = 0
    width_cutoff = 0


    # edge detection
    if remove_noise:
        img = img.filter(ImageFilter.GaussianBlur(radius = 1))

    edge_img = img.filter(ImageFilter.FIND_EDGES)
    edge_np = np.array(edge_img)

    # Thresholding image to 0 or 255
    edge_np[edge_np<125]=0
    edge_np[edge_np>125]=255

    # Outer edges of the edge image is 255. Making it 0
    edge_np[0] = 0
    edge_np[-1] = 0
    edge_np[:,0] = 0
    edge_np[:,-1] = 0

    # rho and theta parameters definition
    # Going to consider right angles as near horizontal and vertical lines are to be detected.
    req_angles = np.concatenate([np.arange(-95, -85), np.arange(-5,5),np.arange(85,95)])
    # req_angles = np.arange(-90, 90, 1)
    theta_radians = np.radians(req_angles)
    diag = np.ceil(np.sqrt(np.square(img_width) + np.square(img_height)))
    rho_list = np.arange(-diag, diag+1)
    cos_theta = np.cos(theta_radians)
    sin_theta = np.sin(theta_radians)

    # Accumulator array. size = (2 * no_of_rhos, number of thetas)
    hough_accumulator = np.zeros((len(rho_list), len(theta_radians)))
    # Iterate over image
    for y in range(height_cutoff, img_height):
        for x in range(width_cutoff, img_width):
            if edge_np[y][x] != 0:
                for theta_index in range(len(theta_radians)):
                    # rho = x.cos(theta) + y.sin(theta)
                    rho = int(x * cos_theta[theta_index] + y * sin_theta[theta_index] + diag)
                    hough_accumulator[rho][theta_index] += 1
    
    return hough_accumulator, rho_list, theta_radians


def draw_hough_vertical_lines(img, hough_accumulator, rho_list, theta_radians, vertical_line_indices, threshold=500):
    ''' references used to draw lines onto image:
        1. https://docs.opencv.org/3.4/d6/d10/tutorial_py_houghlines.html
        2. https://towardsdatascience.com/lines-detection-with-hough-transform-84020b3b1549
    '''
    figure = plt.figure(figsize=(15, 15))
    subplot1 = figure.add_subplot(1, 2, 1)
    subplot1.set_facecolor((0, 0, 0))
    subplot2 = figure.add_subplot(1, 2, 2)
    subplot2.imshow(img)

    for y in range(hough_accumulator.shape[0]):
        for x in vertical_line_indices:
            # accumulator without blur = 500, 300, 200
            if hough_accumulator[y][x] > threshold:
                rho = rho_list[y]
                theta = theta_radians[x]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = (a * rho) #+ img_width
                y0 = (b * rho) #+ img_height
                x1 = int(x0 + 10000 * (-b))
                y1 = int(y0 + 10000 * (a))
                x2 = int(x0 - 10000 * (-b))
                y2 = int(y0 - 10000 * (a))
                subplot1.plot([theta], [rho], marker='o')
                subplot2.add_line(mlines.Line2D([x1, x2], [y1, y2]))
    plt.savefig("vertical_hough_lines.jpg")
    plt.show()



def draw_hough_horizontal_lines(img, hough_accumulator, rho_list, theta_radians, horizontal_line_indices, threshold=240):
    ''' references:
        1. https://docs.opencv.org/3.4/d6/d10/tutorial_py_houghlines.html
        2. https://towardsdatascience.com/lines-detection-with-hough-transform-84020b3b1549
    '''
    figure = plt.figure(figsize=(15, 15))
    subplot1 = figure.add_subplot(1, 2, 1)
    subplot1.set_facecolor((0, 0, 0))
    subplot2 = figure.add_subplot(1, 2, 2)
    subplot2.imshow(img)

    for y in range(hough_accumulator.shape[0]):
        for x in horizontal_line_indices:
            # accumulator without blur = 230, 145
            if hough_accumulator[y][x] > threshold:
                rho = rho_list[y]
                theta = theta_radians[x]
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = (a * rho) #+ img_width
                y0 = (b * rho) #+ img_height
                x1 = int(x0 + 10000 * (-b))
                y1 = int(y0 + 10000 * (a))
                x2 = int(x0 - 10000 * (-b))
                y2 = int(y0 - 10000 * (a))
                subplot1.plot([theta], [rho], marker='o')
                # print([x1,x2])
                # print([y1, y2])
                subplot2.add_line(mlines.Line2D([x1, x2], [y1, y2]))
    plt.savefig("horizontal_hough_lines.jpg")
    plt.show()


    def rotate_image_by_tilt(img, hough_accumulator, req_angles):
        max_value_angle = np.where(hough_accumulator==hough_accumulator.max())[1]
        rotate_angle = req_angles[max_value_angle]
        rotate_img = img.rotate(rotate_angle)
        rotate_img.save("corrected.jpg")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('Incorrect number of arguments have been specified.')

    horizontal_line_indices = [0,1,2,3,4,5,6,7,8,9,20,21,22,23,24,25,26,27,28,29]
    vertical_line_indices = [10,11,12,13,14,15,16,17,18,19]
    req_angles = np.concatenate([np.arange(-95, -85), np.arange(-5,5),np.arange(85,95)])

    # img = Image.open("a-3.jpg")
    input_img_name = sys.argv[1]
    img = Image.open(input_img_name)
    img = img.convert("L")
    print("Image size: ", img.size)

    width, height = img.size

    left_segment = [0, width/3, 1.8 * width/3]
    top_segment = [0.3 * height, 0.3 * height, 0.3 * height]
    right_segment = [width/3, 1.8 * width/3, width]
    bottom_segment = [height, height, height]
    img_segments = []

    for i in range(len(left_segment)):
        im1 = img.crop((left_segment[i], top_segment[i], right_segment[i], bottom_segment[i]))
        img_segments.append(im1)

    # Capture and show first segment
    hough_accumulator, rho_list, theta_radians = apply_hough_transform(img_segments[0])

    draw_hough_vertical_lines(img_segments[0], hough_accumulator, rho_list, theta_radians, vertical_line_indices)

    draw_hough_horizontal_lines(img_segments[0], hough_accumulator, rho_list, theta_radians, horizontal_line_indices,threshold=100)