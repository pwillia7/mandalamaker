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

def generate_color_palette():
    # Exclude cyan by avoiding hues close to cyan's hue in the HSV color space
    hue = random.choice(np.concatenate((np.linspace(0, 0.4, 10), np.linspace(0.6, 1, 10))))
    # Use color harmonies such as analogous or complementary color schemes
    complementary_hue = (hue + 0.5) % 1.0
    analogous_hue1 = (hue + 1/12) % 1.0
    analogous_hue2 = (hue - 1/12) % 1.0
    colors = mcolors.hsv_to_rgb([[hue, 1, 1], [complementary_hue, 1, 1], [analogous_hue1, 1, 1], [analogous_hue2, 1, 1]])
    return colors.tolist()


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
        # Introduce more variety in the shapes
        shape = random.choice([6, 8, 10, 12])
        radius = size * (layer + 1) / num_layers
        star_radius = radius * random.uniform(0.8, 1.2)
        star_points = random.choice([6, 8, 10, 12])  # More points for complexity
        base_shape = generate_base_shape(center, radius, shape)
        star = generate_star(center, star_radius, star_points)
        # Combine base shapes and stars to form a complex pattern
        combined_pattern = base_shape + star
        pattern_paths.append(combined_pattern)
    return pattern_paths


def generate_color_palette():
    base_color = mcolors.hsv_to_rgb(np.array([random.random(), 1, 1]))
    complementary_color = mcolors.hsv_to_rgb(np.array([(base_color[0] + 0.5) % 1.0, 1, 1]))
    return [base_color, complementary_color]

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
    color_palette = generate_color_palette()  # Generate a new color palette for each pattern

    pattern_layers = create_pattern(center, size, num_layers)
    base_line_width = 1.0  # Base line width for the outermost layer
    for i, pattern in enumerate(pattern_layers):
        # Adjust line width for visibility without overcrowding
        line_width = max(base_line_width - 0.15 * i, 0.4)
        color = color_palette[i % len(color_palette)]
        pattern_path = Path(pattern + [pattern[0]])  # Close the path for each combined pattern
        patch = PathPatch(pattern_path, facecolor='none', edgecolor=color, linewidth=line_width)
        ax.add_patch(patch)
        all_paths.append(pattern_path)

    # Set the plot limits to ensure the pattern is centered and zoomed appropriately
    pattern_bound = size * num_layers
    ax.set_xlim(center[0] - pattern_bound, center[0] + pattern_bound)
    ax.set_ylim(center[1] - pattern_bound, center[1] + pattern_bound)
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
