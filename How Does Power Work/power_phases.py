import numpy as np
import matplotlib.pyplot as plt

# Time array from 0 to 0.2 seconds, 1000 points for higher resolution
time = np.linspace(0, 0.2, 1000)
# Frequency of the AC system
frequency = 60  # Hz

# Angular frequency
omega = 2 * np.pi * frequency

# First phase sine wave
phase1 = np.sin(omega * time)

# Second phase sine wave, 90 degrees (pi/2 radians) out of phase
phase2 = np.sin(omega * time + np.pi / 2)

# Plotting

# Plot for the first phase
plt.figure(figsize=(15, 4))
plt.subplot(1, 3, 1)  # 1 row, 3 columns, 1st subplot
plt.plot(time, phase1, label='First Phase')
plt.title('First Phase')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.grid(True)

# Plot for the second phase
plt.subplot(1, 3, 2)  # 1 row, 3 columns, 2nd subplot
plt.plot(time, phase2, label='Second Phase', color='orange')
plt.title('Second Phase')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.grid(True)

# Plot for both phases overlaid
plt.subplot(1, 3, 3)  # 1 row, 3 columns, 3rd subplot
plt.plot(time, phase1, label='First Phase')
plt.plot(time, phase2, label='Second Phase', linestyle='--')
plt.title('Both Phases Overlaid')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
