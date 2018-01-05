"""
First convolution, that calculates the input for the neural net from one frame of the game.
"""

import numpy as np


def convolution(this_frame, max_pixel_value=1, convolute=True, convolution_type='proportion'):

    # Calculate width and height of the given frame.
    screen_width = this_frame.shape[0]
    screen_height = this_frame.shape[1]

    # Check if the data is 2 or 3 dimensional (e.g. RGB image would have a third dimension size of 3).
    screen_dim = this_frame.shape.__len__()
    # If there is a third dimension, get the screen depth, otherwise set screen depth to 1.
    if screen_dim < 3:
        screen_depth = 1
    else:
        screen_depth = this_frame.shape[2]
        # If the depth is bigger than 3, it is probably an RGBA image, where A is transparancy, which we do not need.
        # Thus the screen depth is set to 3
        if screen_depth > 3:
            screen_depth = 3
            this_frame = this_frame[:,:,:screen_depth]


    # Here the convolution kernel dimensions are defined. If no convolution is wanted, the output image will have the
    # same size like the input.
    if convolute:
        # Chech the type of convolution type. Square convolution will look at the whole screen and produce a squared
        # output. Proportion will keep the input screen proportion (e.g. 16:9 input will give 16:9 format output).
        if convolution_type == 'square':
            # Define parameters for the kernel that executes the first convolution.
            # Kernel height and width.
            kernel_width = int(screen_width / 20)
            kernel_height = int(screen_height / 20)
            # Kernel jump in x and y direction.
            kernel_x_jump = int(screen_width / 40)
            kernel_y_jump = int(screen_height / 40)
        elif convolution_type == 'proportion':
            # Define parameters for the kernel that executes the first convolution.
            # Kernel height and width.
            kernel_width = int(screen_width / 20)
            kernel_height = int(screen_height / 20)
            # Kernel jump in x and y direction (a jump length of 19 gets every pixel for a 600x800 input screen and the
            # kernel dimensions of screen dimensions /20).
            kernel_x_jump = 19
            kernel_y_jump = kernel_x_jump

    else:
        # Don't change the size of the image
        kernel_width = 1
        kernel_height = 1
        kernel_x_jump = 1
        kernel_y_jump = 1
    # Compute the number of pixels the kernel is summing up to create a new pixel.
    n_pixel_kernel = kernel_height * kernel_width

    # Calculate total number of output pixels.
    n_pixel_x = int((screen_width - kernel_width)/kernel_x_jump)
    n_pixel_y = int((screen_height - kernel_height) / kernel_y_jump)
    output_img = np.zeros((n_pixel_x, n_pixel_y))
    for i_pixel_y in range(n_pixel_y):
        for i_pixel_x in range(n_pixel_x):
            # Calculate the x and y pixels used for this kernel position.
            x_range = (kernel_x_jump * i_pixel_x, kernel_x_jump * i_pixel_x + kernel_width - 1)
            y_range = (kernel_y_jump * i_pixel_y, kernel_y_jump * i_pixel_y + kernel_height - 1)
            # Sum up all pixel values that are in this kernel (for no convolution, no range but just one value is used).
            if convolute:
                output_img[i_pixel_x, i_pixel_y] = this_frame[x_range[0]:x_range[1], y_range[0]:y_range[1]].sum()
            else:
                output_img[i_pixel_x, i_pixel_y] = this_frame[x_range[0], y_range[0]].sum()

            # Normalize the value of this new pixel computed by the kernel.
            output_img[i_pixel_x, i_pixel_y] /= screen_depth * max_pixel_value * n_pixel_kernel

    return output_img
