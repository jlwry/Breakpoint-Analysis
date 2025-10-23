from utils.model_fitting import piecewise_linear, fit_full_model
from utils.plotting import plot_with_selection, plot_results
from utils.data_processing import butter_lowpass_filter
from scipy.optimize import minimize
from scipy.signal import resample
import pandas as pd
import numpy as np

def breakpoint(data: str, angle_column:int, moment_column:int, standing_column:int):

    data = pd.read_csv(data, header=4, sep="\t")

    angle_raw = data.iloc[:, angle_column].dropna()
    moment_raw = data.iloc[:, moment_column].dropna()
    standing_raw = data.iloc[:, standing_column].dropna()

    moment_filtered = butter_lowpass_filter(moment_raw, sample_freq=2000, cutoff_freq=1)
    angle_filtered = butter_lowpass_filter(angle_raw, sample_freq=100, cutoff_freq=1)
    standing_filtered = butter_lowpass_filter(standing_raw, sample_freq=100, cutoff_freq=1)

    new_length = len(moment_raw) // 20
    angle_down = resample(angle_filtered, new_length)
    angle_down = angle_down - np.mean(standing_filtered)
    moment_down = resample(moment_filtered, new_length)
    moment_down = (moment_down*101.24) - 0.21223           # mV --> Nm conversion equation

    selected_indices = plot_with_selection(angle_down)

    start_index, stop_index = sorted(selected_indices)
    angle_data = angle_down[start_index:stop_index + 1]
    moment_data = moment_down[start_index:stop_index + 1]

    if angle_down[start_index] > angle_down[stop_index]:
        angle_data = -angle_data + 100
        moment_data = -moment_data

    min_angle = np.min(angle_data)
    max_angle = np.max(angle_data)
    angle_norm = (angle_data - min_angle) / (max_angle - min_angle) * 100

    print(f"Angle normalized to 0–100% range (min={min_angle:.2f}, max={max_angle:.2f})")

    x = angle_norm
    y = moment_data

    initial_guess = [20, 80]

    bounds = [tuple(sorted((x[1], x[-2]))), tuple(sorted((x[2], x[-1])))]

    res = minimize(piecewise_linear, x0=initial_guess, args=(x, y), bounds=bounds, method='Nelder-Mead')

    break_1, break_2 = np.sort(res.x)

    print(f"Best breakpoints: t1 = {break_1:.3f}%, t2 = {break_1:.3f}%")
    print(f"Minimized SSR: {res.fun:.3f}")

    y_fit, thetas = fit_full_model(x, y, break_1, break_2)

    print(f"Stiffness in the L, T, and H Stiffness Zones = {thetas[0][0]:.2f}, {thetas[1][0]:.2f}, {thetas[2][0]:.2f}")

    plot_results(x, y, break_1, break_2, y_fit)
