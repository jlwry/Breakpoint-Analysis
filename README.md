# Breakpoint-Analysis 

Determines two optimal breakpoints across the participant's range of motion, minimizing residual error in a three-segment piecewise linear fit of the moment-angle curve.

## Brief Background: 

Investigations into lumbar spine passive stiffness analyze participant moment-angle curves to identify spinal mechanical characteristics. Many investigations have employed piecewise linear functions to analyze these moment-angle curves [1-6]. The most common algorithm currently in use was developed by Barrett et al. [7], though no open-source implementation has been made publicly available.

Recognizing the need for accessible analysis tools, this project implements an independently developed piecewise linear optimization approach that can be used for moment-angle analysis.

## How It's Made:

The algorithm identifies two breakpoints by minimizing the sum of squared residuals (SSR) across three independently-fit linear segments.

Optimization approach: The function uses scipy.optimize.minimize with the Nelder-Mead method to search for optimal breakpoint locations. At each iteration:

1) The data is divided into three segments based on the current breakpoint positions. 
2) A separate linear regression (using least squares via np.linalg.lstsq) is fit to each segment independently.
3) The total SSR across all three segments is calculated and returned as the objective function.

Output: The final model returns the stiffness (slope) of each segment, representing the Low, Transition, and High stiffness zones across the range of motion.



## References

[1] Beach, T. A. C., Parkinson, R. J., Stothart, J. P., & Callaghan, J. P. (2005). Effects of prolonged sitting on the passive flexion stiffness of the in vivo lumbar spine. Spine Journal, 5(2), 145–154. https://doi.org/10.1016/j.spinee.2004.07.036

[2] de Carvalho, D. E., & Callaghan, J. P. (2011). Passive stiffness changes in the lumbar spine and effect of gender during prolonged simulated driving. International Journal of Industrial Ergonomics, 41(6), 617–624. https://doi.org/10.1016/j.ergon.2011.08.002

[3] Fewster, K. M., Barrett, J. M., & Callaghan, J. P. (2021). Passive stiffness changes in the lumbar spine following simulated automotive low speed rear-end collisions. Clinical Biomechanics, 90. https://doi.org/10.1016/j.clinbiomech.2021.105507

[4] Lowery, J. S. M., Dumasal, C. M., & Fewster, K. M. (2025). The effect of physical activity lifestyle on in-vivo passive stiffness of the lumbar spine. Journal of Electromyography and Kinesiology, 80. https://doi.org/https://doi.org/10.1016/j.jelekin.2024.102965

[5] Lowery, J. S. M., & Fewster, K. M. (2025). Lumbar spine passive stiffness can be predicted using trunk moment of inertia. Gait & Posture, 121, 239–243. https://doi.org/10.1016/j.gaitpost.2025.06.002

[6] Tennant, L. M., Nelson-Wong, E., Kuest, J., Lawrence, G., Levesque, K., Owens, D., Prisby, J., Spivey, S., Albin, S. R., Jagger, K., Barrett, J. M., Wong, J. D., & Callaghan, J. P. (2020). A comparison of clinical spinal mobility measures to experimentally derived lumbar spine passive stiffness. Journal of Applied Biomechanics, 36(6), 397–407. https://doi.org/10.1123/JAB.2020-0030

[7] Barrett, J. M., Fewster, K. M., Gruevski, K. M., & Callaghan, J. P. (2021). A novel least-squares method to characterize in-vivo joint functional passive regional stiffness zones. Human Movement Science, 76. https://doi.org/10.1016/j.humov.2021.102765

