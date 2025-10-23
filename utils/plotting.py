import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def plot_results(x, y, break_1, break_2, y_fit):
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, 'o', alpha=1, label='Data')
    plt.plot(x, y_fit, 'r-', linewidth=2, label='Piecewise fit')
    plt.axvline(break_1, color='k', linestyle='--', label=f'Breakpoint 1 = {break_1:.1f}%')
    plt.axvline(break_2, color='k', linestyle='--', label=f'Breakpoint 2 = {break_2:.1f}%')
    plt.legend()
    plt.xlabel('Lumbar Spine Angle (% of ROM)')
    plt.ylabel('Moment (Nm)')
    plt.title('Piecewise Linear Fit (Angle Normalized to ROM)')
    plt.grid(True)
    plt.show()


def plot_with_selection(angle):

    """
    argument: pandas df of lumbar spine angle

    plots the angle data, and prompts the user to select the data they wish to analyze

    output: the start and stop indices
    """

    angle = np.ravel(angle)
    frames = np.arange(len(angle))

    fig, ax = plt.subplots()
    ax.plot(frames, angle, label='Lumbar Spine Angle')
    ax.set_xlabel('Frames')
    ax.set_ylabel('Lumbar Spine Angle (deg)')
    ax.grid(True)

    selected_indices = []

    def onclick(event):
        if event.inaxes == ax:
            frames_val = event.xdata
            idx = (np.abs(frames - frames_val)).argmin()
            selected_indices.append(idx)
            ax.plot(frames[idx], angle[idx], 'ro')
            fig.canvas.draw()
            print(f"Selected point {len(selected_indices)}: frame={frames[idx]}, angle={angle[idx]:.3f} (index={idx})")

            if len(selected_indices) == 2:
                print("Start and stop points selected.")
                fig.canvas.mpl_disconnect(cid)
                plt.close(fig)

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

    return selected_indices