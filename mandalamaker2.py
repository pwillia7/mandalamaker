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
        shape = random.choice([6, 8, 12])  # Choose among hexagons, octagons, dodecagons
        radius = size * (layer + 1) / num_layers
        star_radius = radius * random.uniform(0.8, 1.2)
        star_points = random.randint(5, 12)  # Randomize the number of points for the stars
        base_shape = generate_base_shape(center, radius, shape)
        star = generate_star(center, star_radius, star_points, randomness=True)
        pattern_paths.append((base_shape, star))
    return pattern_paths

def generate_color_palette():
    base_color = mcolors.hsv_to_rgb(np.array([random.random(), 1, 1]))
    complementary_color = mcolors.hsv_to_rgb(np.array([(base_color[0] + 0.5) % 1.0, 1, 1]))
    return [base_color, complementary_color]

def draw_pattern(ax, center, size, num_layers):
    global all_paths
    all_paths = []
    color_palette = generate_color_palette()  # Generate a new color palette for each pattern

    pattern_layers = create_pattern(center, size, num_layers)
    # Determine line width based on layer
    base_line_width = 1.0  # Base line width for the outermost layer
    for i, (base_shape, star) in enumerate(pattern_layers):
        line_width = base_line_width - 0.1 * i if i < 7 else 0.3
        color = color_palette[i % len(color_palette)]
        base_path = Path(base_shape + [base_shape[0]])
        star_path = Path(star)
        patch1 = PathPatch(base_path, facecolor='none', edgecolor=color, linewidth=line_width)
        patch2 = PathPatch(star_path, facecolor='none', edgecolor=color, linewidth=line_width)
        ax.add_patch(patch1)
        ax.add_patch(patch2)
        all_paths.extend([base_path, star_path])


    # Calculate and set the plot limits to ensure the pattern is centered and zoomed appropriately
    pattern_bound = size * num_layers
    ax.set_xlim(center[0] - pattern_bound, center[0] + pattern_bound)
    ax.set_ylim(center[1] - pattern_bound, center[1] + pattern_bound)
    ax.set_aspect(1)
    ax.axis('off')


        
def on_generate(event):
    ax.clear()
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
layers = 6
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