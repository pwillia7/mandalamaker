import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, PathPatch
from matplotlib.path import Path
from matplotlib.widgets import Button
import os
from datetime import datetime

def create_polygon(sides, radius, center, rotation=0):
    angles = np.linspace(0, 2 * np.pi, sides, endpoint=False) + rotation
    points = np.vstack((np.sin(angles), np.cos(angles))).T * radius
    points += center
    return points

def add_layer(ax, center, max_radius, num_shapes, shape_sides, facecolor, depth=0, rotation=0):
    polygons = []
    if depth == 0 or max_radius < 10:  # Prevent radius from becoming too small
        return polygons
    for i in range(num_shapes):
        angle = 2 * np.pi / num_shapes * i + rotation
        new_center = center + np.array([np.cos(angle), np.sin(angle)]) * max_radius / (2 + depth)
        inner_radius = max_radius / (3 + (depth * 2))
        outer_radius = max_radius / (2 + depth)
        points = create_complex_shape(shape_sides, inner_radius, outer_radius, new_center, rotation)
        path = Path(points)
        patch = PathPatch(path, facecolor=facecolor, edgecolor='black', linewidth=0.5)
        ax.add_patch(patch)
        polygons.append(patch)
        # Recursively add more layers
        polygons.extend(add_layer(ax, new_center, outer_radius / 3, num_shapes, shape_sides, facecolor, depth + 1, rotation))
    return polygons

def create_mandala(ax, size, layers, num_shapes, shape_sides):
    ax.clear()
    center = np.array([size / 2, size / 2])
    all_polygons = []
    for i in range(layers):
        # Randomize the rotation and shape parameters for each layer
        rotation = np.random.rand() * 2 * np.pi
        num_shapes_layer = np.random.randint(low=5, high=num_shapes)
        shape_sides_layer = np.random.randint(low=5, high=shape_sides)
        alpha = 0.1 + (0.9 / layers) * (layers - i)
        r, g, b, _ = plt.cm.viridis(i / layers)
        facecolor = (r, g, b, alpha)
        layer_polygons = add_layer(ax, center, size / 2, num_shapes_layer, shape_sides_layer, facecolor, depth=i + 1, rotation=rotation)
        all_polygons.append(layer_polygons)
    ax.set_xlim(0, size)
    ax.set_ylim(0, size)
    ax.set_aspect('equal')
    ax.axis('off')
    return all_polygons


def create_complex_shape(sides, inner_radius, outer_radius, center, rotation=0):
    # Define a complex star-like shape with alternating radii
    angles = np.linspace(0, 2 * np.pi, sides*2, endpoint=False) + rotation
    points = []
    for angle in angles[::2]:
        points.append(center + np.array([np.cos(angle), np.sin(angle)]) * outer_radius)
    for angle in angles[1::2]:
        points.append(center + np.array([np.cos(angle), np.sin(angle)]) * inner_radius)
    return points
def on_generate(event):
    global all_polygons
    # Call create_mandala with the correct number of arguments
    all_polygons = create_mandala(ax, size, layers, num_shapes, shape_sides)
    fig.canvas.draw_idle()
def save_svg(polygons, filename):
    fig_svg, ax_svg = plt.subplots()
    ax_svg.set_xlim(0, size)
    ax_svg.set_ylim(0, size)
    ax_svg.axis('off')
    for poly in polygons:
        # Use the original path of the PathPatch for the new patch
        path_patch = PathPatch(poly.get_path(), facecolor=poly.get_facecolor(), edgecolor='black')
        ax_svg.add_patch(path_patch)
    fig_svg.savefig(filename, bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close(fig_svg)


def on_save(event):
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    directory = f"mandala_layers_{timestamp}"
    os.makedirs(directory, exist_ok=True)
    for i, layer_polygons in enumerate(all_polygons):
        if layer_polygons:  # Check if layer is not empty
            filename = os.path.join(directory, f'layer_{i + 1}.svg')
            save_svg(layer_polygons, filename)

size = 800
layers = 4
num_shapes = 8
shape_sides = 8

fig, ax = plt.subplots(figsize=(8, 8))
btn_generate = Button(plt.axes([0.7, 0.05, 0.1, 0.075]), 'Generate')
btn_generate.on_clicked(on_generate)
btn_save = Button(plt.axes([0.81, 0.05, 0.1, 0.075]), 'Save SVGs')
btn_save.on_clicked(on_save)

# Initial mandala creation for display
all_polygons = create_mandala(ax, size, layers, num_shapes, shape_sides)


plt.show()
