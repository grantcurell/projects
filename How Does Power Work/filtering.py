import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import lfilter

# Time array for 20ms at a 50Hz frequency signal
time = np.linspace(0, 0.02, 1000)

# Define the AC voltage signal
voltage_amplitude = 230
ac_voltage = voltage_amplitude * np.sin(2 * np.pi * 50 * time)

# Full-wave rectify the AC voltage signal
rectified_voltage = np.abs(ac_voltage)

# Create a simple RC low-pass filter to simulate the capacitor effect
R = 1e3  # Resistance in ohms
C = 33e-6  # Capacitance in farads
rc_filter = R * C  # RC time constant
sampling_rate = 1000  # Sampling frequency in Hz

# Filter the rectified voltage using a low-pass filter
filtered_voltage = lfilter([1], [1, rc_filter], rectified_voltage)

# Plot the rectified voltage after filtering (left side)
plt.figure(figsize=(14, 5))
plt.subplot(1, 2, 1)
plt.plot(time, filtered_voltage, label='Filtered Voltage')
plt.title('Rectified Voltage After Filtering')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.grid(True)

# Simulate voltage regulation (smoothing) - exponential moving average (EMA)
alpha = 0.01  # Smoothing factor
smoothed_voltage = filtered_voltage.copy()
for i in range(1, len(filtered_voltage)):
    smoothed_voltage[i] = alpha * filtered_voltage[i] + (1 - alpha) * smoothed_voltage[i - 1]

# Plot the smoothed voltage after voltage regulation (right side)
plt.subplot(1, 2, 2)
plt.plot(time, smoothed_voltage, label='Smoothed Voltage', color='orange')
plt.title('Voltage After Smoothing (Voltage Regulation)')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.grid(True)

plt.tight_layout()
plt.show()
