import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib.widgets import Button
import os
from datetime import datetime
import random

def create_hexagon(center, radius):
    points = []
    for i in range(6):
        angle = i * np.pi / 3
        points.append((center[0] + np.cos(angle) * radius, center[1] + np.sin(angle) * radius))
    return points

def create_grid(center, size, num_layers):
    points = []
    for i in range(num_layers):
        for j in range(num_layers):
            grid_center = (center[0] + i * size / num_layers, center[1] + j * size / num_layers)
            hexagon_points = create_hexagon(grid_center, size / num_layers / 2)
            points.extend(hexagon_points)
    return points


def create_star(center, radius, num_points):
    # Generate a star with precise geometric properties
    points = []
    for i in range(num_points * 2):
        angle = i * np.pi / num_points
        r = radius if i % 2 == 0 else radius / 2
        points.append((center[0] + np.cos(angle) * r, center[1] + np.sin(angle) * r))
    points.append(points[0])  # Close the star path
    return points


def create_complex_star(center, size, num_layers):
    # Create a more complex and layered star pattern
    points = []
    for i in range(1, num_layers + 1):
        radius = size * (num_layers - i + 1) / num_layers
        num_points = random.choice([5, 6, 8, 10, 12])  # More traditional point numbers
        star_points = create_star(center, radius, num_points)
        points.extend(star_points)
    return points



def generate_layer(center, size, num_layers, layer_num):
    # Adjust the size of the star based on the layer
    inner_radius = size * 0.1 * (num_layers - layer_num)
    outer_radius = size * 0.2 * (num_layers - layer_num)
    num_points = np.random.randint(5, 9)  # Random number of star points
    star_points = create_star(center, inner_radius, outer_radius, num_points)
    path = Path(star_points + [star_points[0]])  # Close the star path
    return path

def draw_mandala(ax, center, size, num_layers):
    global all_paths
    all_paths = []  # Clear the list of paths
    grid_size = int(np.sqrt(num_layers))
    cell_size = size / grid_size
    for i in range(grid_size):
        for j in range(grid_size):
            star_points = create_complex_star(center, cell_size, random.randint(1, 5))
            path = Path(star_points)
            all_paths.append(path)  # Store the path
            patch = PathPatch(path, facecolor=np.random.rand(3,), alpha=0.5, edgecolor='none')
            ax.add_patch(patch)



def on_generate(event):
    global all_paths
    ax.clear()
    all_paths = []  # Clear the list of paths
    draw_mandala(ax,(0.5, 0.5),1.0, layers)  # Adjust the size to 1.0
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw()



def save_svg(path, filename):
    fig, ax = plt.subplots(figsize=(6, 6))  # Set the figure size to be square
    ax.add_patch(PathPatch(path))
    ax.relim()
    ax.autoscale_view()
    plt.axis('off')
    plt.rcParams['svg.fonttype'] = 'none'
    plt.savefig(filename, format='svg')



def on_save(event):
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    directory = f"mandala_layers_{timestamp}"
    os.makedirs(directory, exist_ok=True)
    for i, path in enumerate(all_paths):
        filename = os.path.join(directory, f'layer_{i + 1}.svg')
        save_svg(path, filename)

size = 1.0
layers = 5
all_paths = []

fig, ax = plt.subplots()
btn_generate = Button(plt.axes([0.7, 0.05, 0.1, 0.075]), 'Generate')
btn_generate.on_clicked(on_generate)
btn_save = Button(plt.axes([0.81, 0.05, 0.1, 0.075]), 'Save SVGs')
btn_save.on_clicked(on_save)

ax.set_xlim(-0.5, 0.5)
ax.set_ylim(-0.5, 0.5)

ax.set_aspect(1)
ax.axis('off')

# Generate initial mandala
on_generate(None)

plt.show()
