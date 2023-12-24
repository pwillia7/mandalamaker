import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
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
        radius = max_radius * ((3 - depth) / 3.5) 
        points = create_polygon(shape_sides, radius, new_center, rotation=np.random.rand() * 2 * np.pi)
        polygon = Polygon(points, closed=True, facecolor=facecolor, edgecolor='black')
        ax.add_patch(polygon)
        polygons.append(polygon)
        polygons.extend(add_layer(ax, new_center, radius / 2, num_shapes, shape_sides, facecolor, depth + 1, rotation))
    return polygons

def create_mandala(ax, size, layers, num_shapes, shape_sides):
    ax.clear()
    colors = plt.cm.viridis(np.linspace(0, 1, layers))
    center = np.array([size / 2, size / 2])
    all_polygons = []
    for i in range(layers):
        rotation = np.random.rand() * 2 * np.pi  # Randomize rotation for each layer
        polygons = add_layer(ax, center, size / 2, num_shapes, shape_sides, colors[i], depth=i+1, rotation=rotation)
        all_polygons.append(polygons)
    ax.set_xlim(0, size)
    ax.set_ylim(0, size)
    ax.set_aspect('equal')
    ax.axis('off')
    return all_polygons

def on_generate(event):
    global all_polygons
    all_polygons = create_mandala(ax, size, layers, num_shapes, shape_sides)
    fig.canvas.draw_idle()

def save_svg(polygons, filename):
    # Create a new figure for saving SVGs
    fig_svg, ax_svg = plt.subplots()
    ax_svg.set_xlim(0, size)
    ax_svg.set_ylim(0, size)
    ax_svg.axis('off')
    for poly in polygons:
        ax_svg.add_patch(Polygon(poly.get_xy(), closed=True, facecolor=poly.get_facecolor(), edgecolor='black'))
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
