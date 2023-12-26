# Mandala Maker

This Python script, known as "Mandala Maker," is designed to create and export intricate Arab-inspired geometric patterns. These patterns adhere to Islamic geometric design principles and are suitable for artistic and design applications such as laser cutting.

## Features

- Generates complex geometric patterns with random variations.
- Exports patterns as SVG files with organized folder structure.
- Customizable pattern complexity and color aesthetics.

## Screenshot

![Generated Mandala Pattern](screen.png)

## Folder Structure

- `/mandala_generation_timestamp/` - Contains all outputs from a single generation session.
  - `/layers/` - Individual SVG files for each layer.
  - `/color_layers/` - SVG files grouped by color.
  - `mandala_full_timestamp.svg` - A single SVG file with the full pattern.

## Usage

Run the script to display an initial pattern. Use the 'Generate' button to create a new pattern, and the 'Save SVGs' button to save the pattern layers as SVG files.

## Requirements

- Python 3.x
- Matplotlib
- Numpy

## Running the Script

To start Mandala Maker:
```
python mandala_maker.py
```
## ToDo
- Integrate color palette customization within the user interface.
- Enhance the algorithm for more advanced pattern interlacing.
- Scale up the generation for a larger number of layers while maintaining pattern clarity.
-  Develop a graphical user interface for ease of use by those not familiar with command-line operations.
## License
This project is released under the MIT License.
