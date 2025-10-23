from utils.interactive_plotting import plot_with_selection
from utils.data_processing import butter_lowpass_filter
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.signal import resample
import numpy as np
import pandas as pd

def breakpoint(data: str):
    data = pd.read_csv(data, header=4, sep="\t")

    angle_raw = data.iloc[:, 1].dropna()                    # Select the column that is to be analysed
    moment_raw = data.iloc[:, 2].dropna()                   # Select the column that is to be analysed
    standing_raw = data.iloc[:, 5].dropna()                 # Select the column that is to be analysed

    # --- Filter signals ---
    moment_filtered = butter_lowpass_filter(moment_raw, sample_freq=2000, cutoff_freq=1)
    angle_filtered = butter_lowpass_filter(angle_raw, sample_freq=100, cutoff_freq=1)
    standing_filtered = butter_lowpass_filter(standing_raw, sample_freq=100, cutoff_freq=1)

    # --- Downsample to match frequency ---
    new_length = len(moment_raw) // 20
    angle_down = resample(angle_filtered, new_length)
    angle_down = angle_down - np.mean(standing_filtered)    # Normalize to standing
    moment_down = resample(moment_filtered, new_length)
    moment_down = (moment_down*101.24) - 0.21223           # mV --> Nm

    # --- Interactive selection of data to analyse ---
    selected_indices = plot_with_selection(angle_down)
    start_index, stop_index = sorted(selected_indices)
    angle_data = angle_down[start_index:stop_index + 1]
    moment_data = moment_down[start_index:stop_index + 1]
    if angle_down[start_index] < angle_down[stop_index]:
        angle_data = angle_data[::-1]
        moment_data = moment_data[::-1]

    # --- Normalize spine angle to % of full ROM ---
    min_angle = np.min(angle_data)
    max_angle = np.max(angle_data)
    angle_norm = (angle_data - min_angle) / (max_angle - min_angle) * 100

    print(f"Angle normalized to 0–100% range (min={min_angle:.2f}, max={max_angle:.2f})")

    # Use normalized angle as x-axis variable
    x = angle_norm
    y = moment_data

    # --- Define fitting functions ---
    def fit_segment(x_seg, y_seg):
        A = np.vstack([x_seg, np.ones_like(x_seg)]).T
        theta, _, _, _ = np.linalg.lstsq(A, y_seg, rcond=None)
        return theta, A @ theta

    def piecewise_linear(breakpoints, x, y):
        t1, t2 = np.sort(breakpoints)
        mask1 = x < t1
        mask2 = (x >= t1) & (x < t2)
        mask3 = x >= t2

        theta1, y1_pred = fit_segment(x[mask1], y[mask1])
        theta2, y2_pred = fit_segment(x[mask2], y[mask2])
        theta3, y3_pred = fit_segment(x[mask3], y[mask3])

        y_pred = np.empty_like(y)
        y_pred[mask1] = y1_pred
        y_pred[mask2] = y2_pred
        y_pred[mask3] = y3_pred

        ssr = np.sum((y - y_pred) ** 2)
        return ssr

    # --- Optimize breakpoints ---
    initial_guess = [20, 80]
    bounds = [tuple(sorted((x[1], x[-2]))), tuple(sorted((x[2], x[-1])))]

    res = minimize(piecewise_linear, x0=initial_guess, args=(x, y), bounds=bounds, method='Nelder-Mead')

    best_t1, best_t2 = np.sort(res.x)
    print(f"Best breakpoints: t1 = {best_t1:.3f}%, t2 = {best_t2:.3f}%")
    print(f"Minimized SSR: {res.fun:.3f}")

    # --- Compute final fit ---
    def fit_full_model(x, y, t1, t2):
        mask1 = x < t1
        mask2 = (x >= t1) & (x < t2)
        mask3 = x >= t2

        def fit_segment(x_seg, y_seg):
            A = np.vstack([x_seg, np.ones_like(x_seg)]).T
            theta, *_ = np.linalg.lstsq(A, y_seg, rcond=None)
            return theta, A @ theta

        theta1, y1_pred = fit_segment(x[mask1], y[mask1])
        theta2, y2_pred = fit_segment(x[mask2], y[mask2])
        theta3, y3_pred = fit_segment(x[mask3], y[mask3])

        y_pred = np.empty_like(y)
        y_pred[mask1] = y1_pred
        y_pred[mask2] = y2_pred
        y_pred[mask3] = y3_pred

        return y_pred, (theta1, theta2, theta3)

    y_fit, thetas = fit_full_model(x, y, best_t1, best_t2)

    print(f"Stiffness in the L, T, and H Stiffness Zones = {thetas[0][0]:.2f}, {thetas[1][0]:.2f}, {thetas[2][0]:.2f}")

    # --- Plot results ---
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, 'o', alpha = 0.1,  label='Data')
    plt.plot(x, y_fit, 'r-', linewidth=2, label='Piecewise fit')
    plt.axvline(best_t1, color='k', linestyle='--', label=f'Breakpoint 1 = {best_t1:.1f}%')
    plt.axvline(best_t2, color='k', linestyle='--', label=f'Breakpoint 2 = {best_t2:.1f}%')
    plt.legend()
    plt.xlabel('Lumbar Spine Angle (% of ROM)')
    plt.ylabel('Moment (Nm)')
    plt.title('Piecewise Linear Fit (Angle Normalized to ROM)')
    plt.grid(True)
    plt.show()