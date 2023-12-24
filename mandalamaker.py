import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, PathPatch
from matplotlib.path import Path
from matplotlib.widgets import Button
import os
from datetime import datetime


def create_segment(sides, center, radius, rotation=0):
    angles = np.linspace(rotation, rotation + np.pi / sides, 3)  # Segment of a circle
    points = [center]  # Start with the center point
    for angle in angles:
        points.append(center + np.array([np.cos(angle), np.sin(angle)]) * radius)
    return points
def repeat_segment_around_center(segment, center, num_repeats):
    points = []
    for i in range(num_repeats):
        rotation = i * (2 * np.pi / num_repeats)
        rotated_points = [rotate_point(p, center, rotation) for p in segment]
        points.extend(rotated_points[:-1])  # Exclude the last point as it will be repeated
    return points

def rotate_point(point, center, angle):
    offset_point = point - center
    rotated_offset = np.array([
        np.cos(angle) * offset_point[0] - np.sin(angle) * offset_point[1],
        np.sin(angle) * offset_point[0] + np.cos(angle) * offset_point[1]
    ])
    return center + rotated_offset


def create_polygon(sides, radius, center, rotation=0):
    angles = np.linspace(0, 2 * np.pi, sides, endpoint=False) + rotation
    points = np.vstack((np.sin(angles), np.cos(angles))).T * radius
    points += center
    return points

def add_layer(ax, center, max_radius, num_shapes, facecolor, depth=0):
    if depth == 0 or max_radius < 10:
        return []
    polygons = []
    for i in range(num_shapes):
        radius = np.random.uniform(0.1 * max_radius, max_radius / (depth + 2))
        segment = create_segment(num_shapes, center, radius, rotation=np.random.rand() * 2 * np.pi)
        points = repeat_segment_around_center(segment, center, num_shapes)
        path = Path(points, closed=True)
        patch = PathPatch(path, facecolor=facecolor, edgecolor='black', linewidth=0.5)
        ax.add_patch(patch)
        polygons.append(patch)
    return polygons


def create_mandala(ax, size, layers, num_shapes):
    ax.clear()
    center = np.array([size / 2, size / 2])
    all_polygons = []
    for i in range(layers):
        r, g, b, _ = plt.cm.viridis(np.random.rand())
        facecolor = (r, g, b, 0.5)  # Semi-transparent colors
        layer_polygons = add_layer(ax, center, size / 2, num_shapes, facecolor, depth=i + 1)
        all_polygons.append(layer_polygons)
    ax.set_xlim(0, size)
    ax.set_ylim(0, size)
    ax.set_aspect('equal')
    ax.axis('off')
    return all_polygons



def create_symmetrical_shape(sides, center, max_radius, rotation=0):
    # Create shapes with a random but symmetrical pattern
    angles = np.linspace(0, 2 * np.pi, sides, endpoint=False) + rotation
    points = []
    for angle in angles:
        radius = np.random.uniform(0.5 * max_radius, max_radius)
        points.append(center + np.array([np.cos(angle), np.sin(angle)]) * radius)
    return points

def create_complex_shape(sides, inner_radius, outer_radius, center, rotation=0):
    # Enhanced complex shape creation for more intricate patterns
    angles = np.linspace(0, 2 * np.pi, sides * 4, endpoint=False) + rotation
    points = []
    for i, angle in enumerate(angles):
        if i % 4 == 0:
            r = outer_radius
        elif i % 4 == 2:
            r = inner_radius
        else:
            r = (inner_radius + outer_radius) / 2
        point = center + np.array([np.cos(angle), np.sin(angle)]) * r
        points.append(point)
    return points

def on_generate(event):
    global all_polygons
    all_polygons = create_mandala(ax, size, layers, num_shapes)
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

# Initial mandala creation for display
all_polygons = create_mandala(ax, size, layers, num_shapes)
btn_generate = Button(plt.axes([0.7, 0.05, 0.1, 0.075]), 'Generate')
btn_generate.on_clicked(on_generate)
btn_save = Button(plt.axes([0.81, 0.05, 0.1, 0.075]), 'Save SVGs')
btn_save.on_clicked(on_save)


plt.show()
