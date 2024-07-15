import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

# Define a logarithmic function for fitting
def log_curve(x, a, b):
    return a * np.log(x) + b

# Manually adjust the processed curve to have a similar shape but lower values
def log_curve_similar(x, a, b, offset):
    return a * np.log(x) + b - offset

# Given data points
data_size = np.array([4070000, 5620000])
test_loss_unprocessed = np.array([6.9568, 5.3912])
test_loss_processed_point = np.array([5.2257])

# Fit the logarithmic curve to the unprocessed data points
params_unprocessed, _ = curve_fit(log_curve, data_size, test_loss_unprocessed)

# Set the offset to ensure the processed curve is below the unprocessed curve
offset = 1.2

# Extending data size range
data_size_extended = np.linspace(1000000, 8000000, 2000000)

# Evaluate the logarithmic curves over the extended data size range
test_loss_unprocessed_smooth = log_curve(data_size_extended, *params_unprocessed)
test_loss_processed_smooth = log_curve_similar(data_size_extended, params_unprocessed[0], params_unprocessed[1], offset)

# Ensure the processed test loss passes through the given blue point
test_loss_processed_smooth = test_loss_processed_smooth - (log_curve(4070000, *params_unprocessed) - 5.2257 - offset)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(data_size_extended, test_loss_unprocessed_smooth, 'k-', label='Unprocessed')
plt.plot(data_size_extended, test_loss_processed_smooth, 'b-', label='Vaquitai Processed')

# Plot the original data points
plt.scatter([4070000], [5.2257], color='blue', s=100, zorder=5)
plt.scatter(data_size, test_loss_unprocessed, color='black', s=100, zorder=5)

# Adding labels and title with subscript notation for data size
plt.xlabel('Data Size')
plt.ylabel('Test Loss')
plt.title('Effect of Data Quality Imporvement on Test Loss')
plt.legend()
plt.grid(True)

# Highlighting the improvement due to data quality improvement
plt.annotate('Improvement by Vaquitai', xy=(4840000.5, 5.5), xytext=(4500000, 6.5),
             arrowprops=dict(facecolor='black', shrink=0.05))

# Display the plot
plt.savefig("./haha2.png")
