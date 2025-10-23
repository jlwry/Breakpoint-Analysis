import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


def plot_with_selection(angle):
    """
    Plots angle vs frames and allows interactive selection of two points (start and stop).
    Returns the indices of the nearest points in the angle array.
    """
    angle = np.ravel(angle)
    x = np.arange(len(angle))  # frame numbers

    fig, ax = plt.subplots()
    ax.plot(x, angle, label='Angle')
    ax.set_xlabel('Frames')
    ax.set_ylabel('Angle')
    ax.set_title('Angle vs Frames')
    ax.grid(True)

    selected_indices = []

    def onclick(event):
        if event.inaxes == ax:
            x_val = event.xdata
            # find the nearest frame
            idx = (np.abs(x - x_val)).argmin()
            selected_indices.append(idx)
            ax.plot(x[idx], angle[idx], 'ro')  # x=frame, y=angle
            fig.canvas.draw()
            print(f"Selected point {len(selected_indices)}: frame={x[idx]}, angle={angle[idx]:.3f} (index={idx})")

            if len(selected_indices) == 2:
                print("Start and stop points selected.")
                fig.canvas.mpl_disconnect(cid)
                plt.close(fig)

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()  # blocking show

    return selected_indices