# Breakpoint-Analysis 

Determines two optimal breakpoints across the participant's range of motion, minimizing residual error in a three-segment piecewise linear fit of the moment-angle curve.

## How It's Made:

The algorithm identifies two breakpoints by minimizing the sum of squared residuals (SSR) across three independently-fit linear segments.

Optimization approach: The function uses scipy.optimize.minimize with the Nelder-Mead method to search for optimal breakpoint locations. At each iteration:

1) The data is divided into three segments based on the current breakpoint positions. 
2) A separate linear regression (using least squares via np.linalg.lstsq) is fit to each segment independently.
3) The total SSR across all three segments is calculated and returned as the objective function.

Output: The final model returns the stiffness (slope) of each segment, representing the Low, Transition, and High stiffness zones across the range of motion.



## References
