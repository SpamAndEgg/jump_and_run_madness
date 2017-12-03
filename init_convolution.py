"""
First convolution, that calculates the input for the neural net from one frame of the game.
"""

import numpy as np


def convolution(this_frame):
    # Calculate width and height of the given frame.
    screen_width = this_frame.shape[0]
    screen_height = this_frame.shape[1]
    # Define parameters for the kernel that executes the first convolution.
    # Kernel height and width.
    kernel_width = int(screen_width / 20)
    kernel_height = int(screen_height / 20)
    # Kernel jump in x and y direction.
    kernel_x_jump = int(screen_width / 40)
    kernel_y_jump = int(screen_height / 40)
    # Calculate total number of output pixels.
    n_pixel_x = int((screen_width - kernel_width)/kernel_x_jump)
    n_pixel_y = int((screen_height - kernel_height) / kernel_y_jump)
    output_img = np.zeros((n_pixel_x, n_pixel_y))
    for i_pixel_y in range(n_pixel_y):
        for i_pixel_x in range(n_pixel_x):
            # Calculate the x and y pixels used for this kernel position.
            x_range = (kernel_x_jump * i_pixel_x, kernel_x_jump * i_pixel_x + kernel_width - 1)
            y_range = (kernel_y_jump * i_pixel_y, kernel_y_jump * i_pixel_y + kernel_height - 1)
            # Sum up all pixel values that are in this kernel.
            output_img[i_pixel_x, i_pixel_y] = this_frame[x_range[0]:x_range[1], y_range[0]:y_range[1]].sum()

    return output_img