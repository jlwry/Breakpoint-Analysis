from scipy.signal import butter, filtfilt
import pandas as pd


def load_data(path:str, angle_column:int, moment_column:int, standing_column:int):

    data = pd.read_csv(path, header=4, sep="\t")
    angle_raw = data.iloc[:, angle_column].dropna()  # Select the column that is to be analysed
    moment_raw = data.iloc[:, moment_column].dropna()  # Select the column that is to be analysed
    standing_raw = data.iloc[:, standing_column].dropna()  # Select the column that is to be analysed

    return angle_raw, moment_raw, standing_raw

def butter_lowpass_filter(data, sample_freq, cutoff_freq=1, order=4):
    """
    Applies a Butterworth low-pass filter using filtfilt
    """
    nyquist_freq = 0.5 * sample_freq
    normalized_cutoff = cutoff_freq / nyquist_freq
    b, a = butter(order, normalized_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)

    return filtered_data