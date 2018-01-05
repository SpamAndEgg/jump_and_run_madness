import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from init_convolution import convolution


def get_array(img_name):
    # load and return the image.
    img = mpimg.imread(img_name)
    # Normalize the image depth.
    return convolution(img, convolute=False)


def plot_array(img_name):
    # Get image array to plot.
    img_to_plot = get_array(img_name)
    # Plot the image.
    plt.imshow(img_to_plot, cmap='gray')


def get_convolution(img_name):
    # Load the image (RGBA information).
    img = mpimg.imread(img_name)
    # Convolute the image and return it.
    return convolution(img)


def plot_convolution(img_name):
    # Get the convoluted image.
    img_convoluted = get_convolution(img_name)
    # Print the convoluted image.
    plt.imshow(img_convoluted, cmap='gray')
