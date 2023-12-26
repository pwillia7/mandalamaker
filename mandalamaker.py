import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib.widgets import Button
import os
from datetime import datetime
import random
import matplotlib.colors as mcolors


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

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib.widgets import Button
import os
from datetime import datetime
import matplotlib.colors as mcolors
import random

initial_zoom_out_factor = 1.2  # This factor can be adjusted based on the pattern size
def generate_color_palette(num_colors):
    colors = []
    for _ in range(num_colors):
        hue = random.random()  # Random hue from 0 to 1
        color = mcolors.hsv_to_rgb([hue, 1, 1])
        colors.append(color)
    return colors


def generate_base_shape(center, radius, num_sides):
    angles = np.linspace(0, 2 * np.pi, num_sides, endpoint=False)
    return [(center[0] + np.cos(angle) * radius, center[1] + np.sin(angle) * radius) for angle in angles]

def generate_star(center, radius, num_points, randomness=False):
    points = []
    inner_radius = radius * (0.5 + random.uniform(-0.1, 0.1) if randomness else 0.5)
    for i in range(num_points * 2):
        angle = i * np.pi / num_points
        r = inner_radius if i % 2 else radius
        points.append((center[0] + np.cos(angle) * r, center[1] + np.sin(angle) * r))
    points.append(points[0])
    return points

def create_pattern(center, size, num_layers):
    pattern_paths = []
    for layer in range(num_layers):
        # Ensure that the number of sides is even for symmetry
        shape = random.choice([6, 8, 12])
        radius = size * (layer + 1) / num_layers
        star_radius = radius * random.uniform(0.8, 1.2)
        # Ensure star points are even and the shape is closed for symmetry
        star_points = random.choice([6, 8, 10, 12]) * 2
        base_shape = generate_base_shape(center, radius, shape)
        star = generate_star(center, star_radius, star_points)
        # Close the shape to complete the pattern
        star.append(star[0])
        base_shape.append(base_shape[0])
        pattern_paths.extend([base_shape, star])  # Combine base and star
    return pattern_paths



def generate_interlaced_star(center, size, num_vertices):
    # Create the main star
    star_points = generate_star(center, size, num_vertices)
    # Create interlacing
    interlaced_points = []
    for i in range(len(star_points) - 1):
        interlaced_points.append(star_points[i])
        mid_point = ((star_points[i][0] + star_points[i + 1][0]) / 2,
                     (star_points[i][1] + star_points[i + 1][1]) / 2)
        interlaced_points.append(mid_point)
    return interlaced_points

def draw_pattern(ax, center, size, num_layers):
    global all_paths
    all_paths = []
    num_colors = random.randint(2, 5)  # Randomly choose between 2 to 5 colors
    color_palette = generate_color_palette(num_colors)  # Generate a color palette with the chosen number of colors


    pattern_layers = create_pattern(center, size, num_layers)
    base_line_width = 1.0  # Base line width for the outermost layer
    for i, pattern in enumerate(pattern_layers):
        line_width = max(base_line_width - 0.1 * i, 0.3)
        color = color_palette[i % len(color_palette)]
        hex_color = mcolors.to_hex(color)  # Convert color to hex string
        pattern_path = Path(pattern)
        patch = PathPatch(pattern_path, facecolor='none', edgecolor=hex_color, linewidth=line_width)
        ax.add_patch(patch)
        # Store path along with its hex color and line width
        all_paths.append((pattern_path, hex_color, line_width))


    # Set the plot limits to ensure the pattern is centered and zoomed appropriately
    ax.set_xlim(center[0] - size, center[0] + size)
    ax.set_ylim(center[1] - size, center[1] + size)
    ax.set_aspect(1)
    ax.axis('off')


def on_generate(event):
    ax.clear()
    layers = random.randrange(5,20)
    draw_pattern(ax, (0, 0), size, layers)
    ax.set_xlim(-size * initial_zoom_out_factor, size * initial_zoom_out_factor)
    ax.set_ylim(-size * initial_zoom_out_factor, size * initial_zoom_out_factor)
    ax.set_aspect(1)
    ax.axis('off')
    fig.canvas.draw()


def save_svg(figure, filename):
    figure.savefig(filename, format='svg', bbox_inches='tight', pad_inches=0.1, transparent=True)
def on_save(event):
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    parent_dir = f"mandala_generation_{timestamp}"
    os.makedirs(parent_dir, exist_ok=True)

    # Save the full mandala without buttons
    full_fig, full_ax = plt.subplots(figsize=(6, 6))
    for path, hex_color, line_width in all_paths:
        full_ax.add_patch(PathPatch(path, facecolor='none', edgecolor=hex_color, linewidth=line_width))
    full_ax.set_xlim(-size, size)
    full_ax.set_ylim(-size, size)
    full_ax.axis('off')
    full_path = os.path.join(parent_dir, f"mandala_full_{timestamp}.svg")
    full_fig.savefig(full_path, format='svg', bbox_inches='tight', pad_inches=0.1, transparent=True)
    plt.close(full_fig)

    # Save individual layers and color layers within the parent directory
    layers_dir = os.path.join(parent_dir, "layers")
    color_layers_dir = os.path.join(parent_dir, "color_layers")
    os.makedirs(layers_dir, exist_ok=True)
    os.makedirs(color_layers_dir, exist_ok=True)

    # Save individual layers
    for i, (path, hex_color, line_width) in enumerate(all_paths):
        fig_layer, ax_layer = plt.subplots(figsize=(6, 6))
        ax_layer.add_patch(PathPatch(path, facecolor='none', edgecolor=hex_color, linewidth=line_width))
        ax_layer.set_xlim(-size, size)
        ax_layer.set_ylim(-size, size)
        ax_layer.axis('off')
        layer_path = os.path.join(layers_dir, f'layer_{i + 1}.svg')
        fig_layer.savefig(layer_path, format='svg', bbox_inches='tight', pad_inches=0.1, transparent=True)
        plt.close(fig_layer)

    # Save color layers
    colors_used = set(hex_color for _, hex_color, _ in all_paths)
    for hex_color in colors_used:
        fig_color, ax_color = plt.subplots(figsize=(6, 6))
        for path, path_color, line_width in all_paths:
            if path_color == hex_color:
                ax_color.add_patch(PathPatch(path, facecolor='none', edgecolor=hex_color, linewidth=line_width))
        ax_color.set_xlim(-size, size)
        ax_color.set_ylim(-size, size)
        ax_color.axis('off')
        color_layer_path = os.path.join(color_layers_dir, f'color_{hex_color[1:]}.svg')
        fig_color.savefig(color_layer_path, format='svg', bbox_inches='tight', pad_inches=0.1, transparent=True)
        plt.close(fig_color)


size = 1.0
layers = random.randrange(5,20)
all_paths = []

fig, ax = plt.subplots()
button_width = 0.15
button_height = 0.075
btn_generate = Button(plt.axes([0.7, 0.05, button_width, button_height]), 'Generate')
btn_generate.on_clicked(on_generate)
btn_save = Button(plt.axes([0.7 + button_width + 0.01, 0.05, button_width, button_height]), 'Save SVGs')
btn_save.on_clicked(on_save)

ax.set_xlim(-size * initial_zoom_out_factor, size * initial_zoom_out_factor)
ax.set_ylim(-size * initial_zoom_out_factor, size * initial_zoom_out_factor)

ax.set_aspect(1)
ax.axis('off')

# Generate initial mandala
on_generate(None)

plt.show()
