import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import numpy as np
from svgwrite import Drawing
from matplotlib.colors import to_hex

def create_polygon(sides, radius, center, rotation=0):
    angles = np.linspace(0, 2 * np.pi, sides, endpoint=False) + rotation
    points = np.vstack((np.sin(angles), np.cos(angles))).T * radius
    points += center
    return points

def create_mandala_layer(center, max_radius, num_shapes, shape_sides, dwg, color, depth=0, rotation=0):
    if depth == 0:
        return
    for i in range(num_shapes):
        angle = 2 * np.pi / num_shapes * i + rotation
        new_center = center + np.array([np.cos(angle), np.sin(angle)]) * max_radius / (3 + depth)
        radius = max_radius * ((3 - depth) / 3.5)  # reduced radius for complexity
        points = create_polygon(shape_sides, radius, new_center, rotation=np.random.rand() * 2 * np.pi)
        dwg.add(dwg.polygon(points.tolist(), fill=color))
        # Reduce the number of recursive calls
        if depth < 3:
            create_mandala_layer(new_center, radius / 2, num_shapes - 1, shape_sides, dwg, color, depth - 1, rotation=rotation)

def create_mandala(size, layers, num_shapes, shape_sides):
    dwgs = []
    colors = [to_hex(c) for c in plt.cm.viridis(np.linspace(0, 1, layers))]
    center = np.array([size / 2, size / 2])
    for i in range(layers):
        dwg = Drawing(size=(f"{size}px", f"{size}px"), profile='tiny')
        rotation = np.random.rand() * 2 * np.pi
        # Start with a lower depth to reduce complexity
        create_mandala_layer(center, size / 2, num_shapes, shape_sides, dwg, colors[i], depth=2, rotation=rotation)
        dwgs.append((dwg, colors[i]))
    return dwgs

def on_generate(event):
    global dwgs
    ax.clear()
    dwgs = create_mandala(size, layers, num_shapes, shape_sides)
    for dwg, color in dwgs:
        for elem in dwg.elements:
            if hasattr(elem, 'points'):
                points = np.array(elem.points)
                ax.fill(points[:, 0], points[:, 1], color)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')
    fig.canvas.draw_idle()

def on_save(event):
    save_svgs(dwgs)

def save_svgs(dwgs):
    for i, (dwg, _) in enumerate(dwgs):
        filename = f'layer_{i + 1}.svg'
        dwg.saveas(filename)
        print(f"Saved {filename}")

size = 800
layers = 3  # reduced number of layers for complexity
num_shapes = 50  # reduced number of shapes for complexity
shape_sides = 3

fig, ax = plt.subplots(figsize=(8, 8))
ax.set_position([0.1, 0.3, 0.8, 0.65])  # Adjust the position of the main axes
ax_generate = plt.axes([0.7, 0.05, 0.1, 0.075])  # Position of the 'Generate' button
ax_save = plt.axes([0.81, 0.05, 0.1, 0.075])  # Position of the 'Save SVGs' button
btn_generate = Button(ax_generate, 'Generate')
btn_generate.on_clicked(on_generate)
btn_save = Button(ax_save, 'Save SVGs')
btn_save.on_clicked(on_save)
plt.axis('off')
on_generate(None)  # Generate initial pattern
plt.show()
