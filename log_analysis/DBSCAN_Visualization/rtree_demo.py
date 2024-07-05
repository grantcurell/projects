from rtree import index
import matplotlib.pyplot as plt

# Create R-tree index
p = index.Property()
p.dimension = 2
idx = index.Index(properties=p)

# Add points to R-tree
points = [(0, 0), (1, 1), (2, 3), (3, 2), (4, 4)]
for i, point in enumerate(points):
    idx.add(i, (*point, *point))

# Plot R-tree
fig, ax = plt.subplots()
for i, point in enumerate(points):
    rect = idx.get_bounds(i)
    ax.add_patch(plt.Rectangle((rect[0], rect[1]), rect[2]-rect[0], rect[3]-rect[1], fill=False))
    ax.scatter(*point)
plt.show()
