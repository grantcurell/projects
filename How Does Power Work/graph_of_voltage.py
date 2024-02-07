import numpy as np
import matplotlib.pyplot as plt

# Parameters for the sine wave
frequency = 60  # Hz
amplitude = 120  # Volts (peak value)
time = np.linspace(0, 1, 1000)  # 1 second, 1000 points
omega = 2 * np.pi * frequency  # Angular frequency

# Sine wave equation
voltage = amplitude * np.sin(omega * time)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(time, voltage, label='Voltage Sine Wave')

# Highlighting the peak, trough, and zero-crossings
plt.plot(1/(2*frequency), amplitude, 'ro')  # Peak
plt.text(1/(2*frequency), amplitude, ' Peak', verticalalignment='bottom')
plt.plot(1/frequency, -amplitude, 'ro')  # Trough
plt.text(1/frequency, -amplitude, ' Trough', verticalalignment='top')
plt.axhline(0, color='black', lw=0.5)  # Zero line for reference

# Annotations
plt.title("AC Power Sine Wave")
plt.xlabel("Time (seconds)")
plt.ylabel("Voltage (V)")
plt.legend()
plt.grid(True)

# Additional labels for volts, amperage, frequency, and cycle
plt.annotate('Volts (V)', xy=(0.8, 100), xytext=(0.85, 50),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate('Frequency: 60Hz\nOne Cycle', xy=(1/frequency, 0), xytext=(1/frequency+0.1, 50),
             arrowprops=dict(facecolor='black', shrink=0.05),
             horizontalalignment='center')
plt.axvline(1/frequency, color='green', linestyle='--')  # Marking one cycle

plt.tight_layout()
plt.show()
