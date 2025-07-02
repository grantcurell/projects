import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R

# Grid parameters (modifiable to simulate GEM settings)
Grdc_ni = 8
Grdc_nj = 4

# Define the Yin grid: center-aligned rectangular patch
yin_lat = np.linspace(-45, 45, Grdc_nj)
yin_lon = np.linspace(-135, 135, Grdc_ni)
yin_lon_grid, yin_lat_grid = np.meshgrid(yin_lon, yin_lat)

# Convert Yin grid to Cartesian
def sph2cart(lon, lat):
    lon_rad = np.radians(lon)
    lat_rad = np.radians(lat)
    x = np.cos(lat_rad) * np.cos(lon_rad)
    y = np.cos(lat_rad) * np.sin(lon_rad)
    z = np.sin(lat_rad)
    return x, y, z

yin_x, yin_y, yin_z = sph2cart(yin_lon_grid, yin_lat_grid)

# Define the Yang grid: same shape, but will be rotated
yang_lat = np.copy(yin_lat)
yang_lon = np.copy(yin_lon)
yang_lon_grid, yang_lat_grid = np.meshgrid(yang_lon, yang_lat)
yang_x, yang_y, yang_z = sph2cart(yang_lon_grid, yang_lat_grid)

# Rotate Yang grid +90° about x-axis
xyz = np.stack((yang_x.flatten(), yang_y.flatten(), yang_z.flatten()), axis=1)
rot = R.from_euler('x', 90, degrees=True)
xyz_rot = rot.apply(xyz)

# Additional 180° rotation around Y-axis to place the Yang grid correctly
rot180 = R.from_euler('y', 180, degrees=True)
xyz_rot = rot180.apply(xyz_rot)

# Reshape for plotting
yang_xr = xyz_rot[:, 0].reshape(yang_x.shape)
yang_yr = xyz_rot[:, 1].reshape(yang_y.shape)
yang_zr = xyz_rot[:, 2].reshape(yang_z.shape)

# Plotting
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(yin_x, yin_y, yin_z, color='blue', alpha=0.5, edgecolor='k', linewidth=0.1)
ax.plot_surface(yang_xr, yang_yr, yang_zr, color='red', alpha=0.5, edgecolor='k', linewidth=0.1)

# Aesthetics
ax.set_box_aspect([1, 1, 1])  # Ensure the sphere is not distorted
ax.set_title("Yin-Yang Grid on the Sphere (Proper Rotation)")
ax.axis('off')
plt.tight_layout()
plt.show()
