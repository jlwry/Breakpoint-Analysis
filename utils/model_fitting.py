import numpy as np

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

def fit_full_model(x, y, t1, t2):
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

    return y_pred, (theta1, theta2, theta3)