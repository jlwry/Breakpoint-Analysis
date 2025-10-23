import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
# test
# Generate example data
x = np.linspace(0, 10, 100)
y = x**5 + np.random.normal(0, 2, size=len(x))  # Add small noise for realism


def fit_segment(x_seg, y_seg):
    A = np.vstack([x_seg, np.ones_like(x_seg)]).T
    theta, _, _, _ = np.linalg.lstsq(A, y_seg, rcond=None)
    return theta, A @ theta

def piecewise_linear(breakpoints, x, y):
    """
    Computes the sum of squared residuals (SSR) for a 3-segment
    piecewise linear model defined by two breakpoints.
    """
    t1, t2 = np.sort(breakpoints)  # ensure t1 < t2

    mask1 = x < t1
    mask2 = (x >= t1) & (x < t2)
    mask3 = x >= t2

    theta1, y1_pred = fit_segment(x[mask1], y[mask1])
    theta2, y2_pred = fit_segment(x[mask2], y[mask2])
    theta3, y3_pred = fit_segment(x[mask3], y[mask3])

    # Reconstruct full prediction
    y_pred = np.empty_like(y)
    y_pred[mask1] = y1_pred
    y_pred[mask2] = y2_pred
    y_pred[mask3] = y3_pred

    ssr = np.sum((y - y_pred) ** 2)
    return ssr


# --- Optimize breakpoints ---
initial_guess = [3, 7]
bounds = [(x[1], x[-2]), (x[2], x[-1])]

res = minimize(piecewise_linear, x0=initial_guess, args=(x, y),
               bounds=bounds, method='Nelder-Mead')

best_t1, best_t2 = np.sort(res.x)
print(f"Best breakpoints: t1 = {best_t1:.3f}, t2 = {best_t2:.3f}")
print(f"Minimized SSR: {res.fun:.3f}")


# --- Compute final fit using optimal breakpoints ---
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


# --- Plot results ---
plt.figure(figsize=(8, 5))
plt.plot(x, y, 'o', alpha=0.4, label='Data')
plt.plot(x, y_fit, 'r-', linewidth=2, label='Piecewise fit')
plt.axvline(best_t1, color='k', linestyle='--', label=f'Breakpoint 1 = {best_t1:.2f}')
plt.axvline(best_t2, color='k', linestyle='--', label=f'Breakpoint 2 = {best_t2:.2f}')
plt.legend()
plt.xlabel('x')
plt.ylabel('y')
plt.title('Piecewise Linear Fit with Optimized Breakpoints')
plt.grid(True)
plt.show()
