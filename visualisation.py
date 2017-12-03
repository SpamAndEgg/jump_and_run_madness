"""
This module allows a visualisation of the game image interpretation after the first kernel (how the input image of the
neural net looks like).
"""

def start(this_conv_frame):
    import matplotlib.pyplot as plt

    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111)
    img = ax.imshow(this_conv_frame, cmap='gist_gray_r', vmin=0, vmax=33488638)
    #img = plt.imshow(this_conv_frame, cmap='gist_gray_r', vmin=0, vmax=255)
    fig.canvas.draw()

    return img


# CREATING TEST ANIMATIONS
# def start_animation():
#
#     def get_matrix():
#         arr = np.random.randint(0, 256, x_size * y_size)
#         arr.resize((x_size, y_size))
#         time.sleep(0.5)
#         return arr
#
#     def update(frame):
#         """ A simple random walk with memory """
#         arr = get_matrix()
#         img.set_data(arr)
#         return img
#
#     def init():
#         arr = get_matrix()
#         img.set_data(arr)
#
#     fig, ax = plt.subplots(1, 1)
#     arr = get_matrix()
#     img = plt.imshow(arr, cmap='gist_gray_r', vmin=0, vmax=255)
#     ani = FuncAnimation(fig, update, init_func=init, blit=False)
#     plt.show()
#
# if __name__ == '__main__':
#     start_animation()
