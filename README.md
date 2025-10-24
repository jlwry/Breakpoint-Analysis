# Breakpoint-Analysis 

Determines two optimal breakpoints across the participant's range of motion, minimizing residual error in a three-segment piecewise linear fit of the moment-angle curve.

<img width="400" height="250" alt="example_figure" src="https://github.com/user-attachments/assets/9abf3758-a32e-4b66-8378-1650d5efd955" />

## Brief Background

Investigations into lumbar spine passive stiffness analyze participant moment-angle curves to identify spinal mechanical characteristics. Many investigations have employed piecewise linear functions to analyze these moment-angle curves [1-6]. The most common algorithm currently in use was developed by Barrett et al. [7], though no open-source implementation has been made publicly available.

Recognizing the need for accessible analysis tools, this project implements an independently developed piecewise linear optimization approach that can be used for moment-angle analysis.

## Usage

### Data Format Requirements

Your data file should be tab-separated with the following structure:
- **Header row** starting at line 5 (4 lines of metadata are skipped)
- **Columns** containing:
  - Angle measurements (e.g., joint angle in degrees)
  - Moment measurements (e.g., joint moment in mV -- if in Nm remove calibration)
  - Standing/baseline spine angle for normalization

Example data structure:
```
Frame    Angle    Moment    Standing
1        45.2     12.3      10.5
2        45.5     12.8      10.4
...
```

### Running the Analysis

1. **Identify your column indices** (0-indexed):
   - In the example above: Column 0 = Frame, Column 1 = Angle, Column 2 = Moment, Column 3 = Standing

2. **Run the example:**
```bash
python main.py
```

3. **Analyze your own data** by modifying `main.py`:
```python
from utils.pipeline import breakpoint

breakpoint(
    'path/to/your/data.txt',
    angle_column=1,      # Adjust to your angle column
    moment_column=2,     # Adjust to your moment column
    standing_column=5    # Adjust to your standing column
)
```

### Output

The analysis will:
1. Display an interactive plot for selecting the range of motion to analyze
2. Print the identified breakpoint locations (as % of range of motion)
3. Print the stiffness values for Low, Transition, and High zones
4. Show a final plot with the fitted piecewise linear model

## How It's Made

The algorithm identifies two breakpoints by minimizing the sum of squared residuals (SSR) across three independently-fit linear segments.

**Optimization approach:** The function uses `scipy.optimize.minimize` with the Nelder-Mead method to search for optimal breakpoint locations. At each iteration:

1. The data is divided into three segments based on the current breakpoint positions
2. A separate linear regression (using least squares via `np.linalg.lstsq`) is fit to each segment independently
3. The total SSR across all three segments is calculated and returned as the objective function

**Constraints:** Breakpoints are bounded to ensure sufficient data in each segment—the first breakpoint must fall between the 2nd and 2nd-to-last x-values, while the second breakpoint is constrained between the 3rd and last x-values. The `np.sort()` within the objective function ensures breakpoints remain ordered regardless of the optimization path.

**Initial conditions:** The search begins with breakpoints at 20% and 80% of the normalized range of motion, providing a reasonable starting configuration across typical joint angles.

**Note:** Linear segments are fit independently without continuity constraints at breakpoints. Each segment's slope and intercept are determined solely by the data points within that segment.

**Output:** The final model returns the stiffness (slope) of each segment, representing the Low, Transition, and High stiffness zones across the range of motion.

## Development Notes

This implementation was developed independently to provide an open-source alternative for piecewise linear analysis of moment-angle data. While the author has prior familiarity with piecewise fitting approaches from laboratory experience, the current code was created from scratch without reference to proprietary implementations. As such, specific methodological choices (optimization algorithms, constraints, initial conditions) may differ from other published approaches [7], and results should be validated for the user's specific application.

## References

[1] Beach, T. A. C., Parkinson, R. J., Stothart, J. P., & Callaghan, J. P. (2005). Effects of prolonged sitting on the passive flexion stiffness of the in vivo lumbar spine. Spine Journal, 5(2), 145–154. https://doi.org/10.1016/j.spinee.2004.07.036

[2] de Carvalho, D. E., & Callaghan, J. P. (2011). Passive stiffness changes in the lumbar spine and effect of gender during prolonged simulated driving. International Journal of Industrial Ergonomics, 41(6), 617–624. https://doi.org/10.1016/j.ergon.2011.08.002

[3] Fewster, K. M., Barrett, J. M., & Callaghan, J. P. (2021). Passive stiffness changes in the lumbar spine following simulated automotive low speed rear-end collisions. Clinical Biomechanics, 90. https://doi.org/10.1016/j.clinbiomech.2021.105507

[4] Lowery, J. S. M., Dumasal, C. M., & Fewster, K. M. (2025). The effect of physical activity lifestyle on in-vivo passive stiffness of the lumbar spine. Journal of Electromyography and Kinesiology, 80. https://doi.org/https://doi.org/10.1016/j.jelekin.2024.102965

[5] Lowery, J. S. M., & Fewster, K. M. (2025). Lumbar spine passive stiffness can be predicted using trunk moment of inertia. Gait & Posture, 121, 239–243. https://doi.org/10.1016/j.gaitpost.2025.06.002

[6] Tennant, L. M., Nelson-Wong, E., Kuest, J., Lawrence, G., Levesque, K., Owens, D., Prisby, J., Spivey, S., Albin, S. R., Jagger, K., Barrett, J. M., Wong, J. D., & Callaghan, J. P. (2020). A comparison of clinical spinal mobility measures to experimentally derived lumbar spine passive stiffness. Journal of Applied Biomechanics, 36(6), 397–407. https://doi.org/10.1123/JAB.2020-0030

[7] Barrett, J. M., Fewster, K. M., Gruevski, K. M., & Callaghan, J. P. (2021). A novel least-squares method to characterize in-vivo joint functional passive regional stiffness zones. Human Movement Science, 76. https://doi.org/10.1016/j.humov.2021.102765

