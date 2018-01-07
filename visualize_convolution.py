# Here the convoluted frame is produced as output for further use by the neural network or for visualization.

import threading
import numpy as np
import global_var
from math import floor


# This thread visualizes the convolution of the game screen.
class VisualConvolutionThread(threading.Thread):
    def run(self):
        # Set up the animation window to show the convoluted frame which will be updated every "interval_time"
        # milliseconds.
        def start_animation():
            # "this_conv_frame" is updated in the game loop regularly.
            import matplotlib.pyplot as plt
            from matplotlib.animation import FuncAnimation

            def update(frame):
                img.set_data(np.transpose(global_var.this_conv_frame))
                plt.setp(title_obj, text='Game score: '+str(floor(global_var.game_score)))

            def init():
                img.set_data(np.transpose(global_var.this_conv_frame))

            fig, ax = plt.subplots(1, 1)
            title_obj = plt.title('Game score: 0')

            img = ax.imshow(np.transpose(global_var.this_conv_frame), cmap='gist_gray_r', vmin=0, vmax=1)
            # Start the animation of the convoluted frame (interval time in milliseconds).
            ani = FuncAnimation(fig, update, init_func=init, blit=False, interval=50)
            plt.show()

            return ani

        # Visualize the input convolution.
        animation = start_animation()


# Start convolution thread.
visual_convolution = VisualConvolutionThread()
visual_convolution.start()

