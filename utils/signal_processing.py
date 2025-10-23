from scipy.signal import butter, filtfilt

def butter_lowpass_filter(data, sample_freq, cutoff_freq=1, order=4):
    """
    Applies a Butterworth low-pass filter using filtfilt
    """
    nyquist_freq = 0.5 * sample_freq
    normalized_cutoff = cutoff_freq / nyquist_freq
    b, a = butter(order, normalized_cutoff, btype='low', analog=False)
    filtered_data = filtfilt(b, a, data)

    return filtered_data