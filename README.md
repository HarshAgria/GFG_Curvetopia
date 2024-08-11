Here is the revised `README.md` file with the updated sections, including the `Usage` section:

```markdown
# Curvetopia

Curvetopia is a Python project designed to detect, regularize, and beautify 2D curves from images. The project supports identifying geometric shapes such as lines, circles, rectangles, and stars, as well as detecting symmetry and completing incomplete curves. The output is visualized using `matplotlib`, and the processed data can be exported as SVG files.

## Table of Contents

- [Curvetopia](#curvetopia)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Features](#features)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Cloning the Repository](#cloning-the-repository)
  - [Usage](#usage)
    - [Running the Project](#running-the-project)
    - [Code Structure](#code-structure)
    - [Customization](#customization)
  - [Examples](#examples)
    - [Detecting and Completing Curves](#detecting-and-completing-curves)
    - [Visualizing the Output](#visualizing-the-output)
  - [Contributing](#contributing)
  - [License](#license)

## Project Overview

Curvetopia aims to assist in the analysis and regularization of 2D curves, with applications in computer graphics, image processing, and geometric data analysis. The project processes data in CSV format, detects common geometric shapes, regularizes curves, and provides visualizations of the detected and completed shapes.

## Features

- **Shape Detection**: Identifies straight lines, circles, rectangles, and star shapes.
- **Symmetry Detection**: Detects vertical and horizontal symmetry in shapes.
- **Curve Completion**: Completes incomplete curves using spline interpolation.
- **Visualization**: Plots original and processed curves with annotations.
- **Data Export**: Optionally exports the processed curves as SVG files.

## Installation

### Prerequisites

Ensure you have Python 3.x installed on your machine. You will also need the following Python libraries:

- `numpy`
- `matplotlib`
- `scikit-learn`
- `scipy`

You can install the required libraries using `pip`:

```bash
pip install numpy matplotlib scikit-learn scipy
```

### Cloning the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/HarshAgria/GFG_Curvetopia.git
cd GFG_Curvetopia
```

## Usage

### Running the Project

1. Place your CSV data file in the `problems` directory.
2. Modify the `main.py` file to point to your CSV file.
3. Run the main script:

```bash
python main.py
```

### Code Structure

- **main.py**: Entry point of the project. Handles loading data, running shape detection, and visualizing results.
- **data_loader.py**: Contains functions for loading and parsing CSV data.
- **visualization.py**: Contains functions for plotting curves and adding labels.
- **regularization.py**: Contains functions for detecting and regularizing shapes.
- **symmetry.py**: Contains functions for detecting symmetry in curves.
- **completion.py**: Contains functions for completing incomplete curves.
- **svg_exporter.py**: (Optional) Handles exporting curves to SVG format.

### Customization

You can customize the project by modifying the following parameters:

- **CSV File Path**: Update the `csv_path` in `main.py` to point to your data file.
- **Detection Tolerances**: Modify the tolerance values in detection functions to adjust sensitivity.

## Examples

### Detecting and Completing Curves

Here's an example of how to use Curvetopia to detect and complete curves:

```python
import numpy as np
from data_loader import read_csv
from visualization import plot
from regularization import detect_straight_lines, detect_circles_and_ellipses, detect_rectangles, detect_star_shapes
from symmetry import detect_symmetry
from completion import complete_curve

csv_path = 'problems/isolated.csv'
paths_XYs = read_csv(csv_path)
plot(paths_XYs, title="Original Curves")

for shape in paths_XYs:
    for path in shape:
        if detect_straight_lines(path):
            print("Detected a straight line")
        # Additional shape detection and curve completion logic...
```

### Visualizing the Output

After running the script, you will see plots with detected shapes labeled and completed curves overlaid on the original curves.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, feel free to fork the repository, make your changes, and submit a pull request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -am 'Add Your Feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Create a new Pull Request


---

Happy coding! If you have any questions or issues, feel free to open an issue on GitHub.
```
