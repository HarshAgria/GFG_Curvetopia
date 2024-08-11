import os
import numpy as np
import matplotlib.pyplot as plt 
from data_loader import read_csv
from visualization import plot
from regularization import detect_star_shape, detect_polygon, detect_rectangle, detect_circle, detect_line, detect_rounded_rectangle, detect_ellipse, detect_parabola 
from symmetry import detect_symmetry, detect_rotational_symmetry
from completion import complete_curve
from svg_exporter import polylines2svg

def main():
    csv_path = 'problems/occlusion1_sol.csv'  # Replace with your actual file path
    # csv_path = 'problems/frag1.csv'  # Replace with your actual file path
    paths_XYs = read_csv(csv_path)

    plot(paths_XYs, title='Original Data')

    for shape in paths_XYs:
        for path in shape:
            path = np.array(path)
            detected_shape = None

            if detect_line(path):
                detected_shape = 'Line'
                print("Detected a straight line")
            elif detect_circle(path):
                detected_shape = 'Circle'
                print("Detected a circle")
            elif detect_ellipse(path):
                detected_shape = 'Ellipse'
                print("Detected an ellipse")
            elif detect_rectangle(path):
                detected_shape = 'Rectangle'
                print("Detected a rectangle")
            elif detect_rounded_rectangle(path):
                detected_shape = 'Rounded Rectangle'
                print("Detected a rounded rectangle")
            elif detect_polygon(path, num_sides=5):
                detected_shape = 'Polygon'
                print("Detected a regular polygon")
            elif detect_star_shape(path):
                detected_shape = 'Star'
                print("Detected a star shape")
            elif detect_parabola(path):
                detected_shape = 'Parabola'
                print("Detected a parabola shape")
            else:
                detected_shape = 'No Shape'
                print("Unidentified shape")

            symmetry_detected, symmetric_part = detect_symmetry(path, tolerance=5)
            if symmetry_detected:
                detected_shape = 'Symmetry'
                print("Detected reflection symmetry")
                path = symmetric_part
                plt.plot(path[:, 0], path[:, 1], 'b-', label='Symmetric Part')
                plt.title('Symmetry Detected')
                plt.legend()
                plt.show()

            rotation_symmetry_detected, rotation_symmetric_part = detect_rotational_symmetry(path, tolerance=10)
            if rotation_symmetry_detected:
                detected_shape = 'Rotational Symmetry'
                print("Detected rotational symmetry")
                path = rotation_symmetric_part
                plt.plot(path[:, 0], path[:, 1], 'b-', label='Rotational Symmetric Part')
                plt.title('Rotational Symmetry Detected')
                plt.legend()
                plt.show()
        
            completed_curve = complete_curve(path)
            plt.plot(completed_curve[:, 0], completed_curve[:, 1], 'r--')
            plt.plot(path[:, 0], path[:, 1], 'b-')
            plt.title(detected_shape)
            plt.show()

    # polylines2svg(paths_XYs, 'output.svg')
    # Create the SVG file path based on the CSV file name
    svg_filename = os.path.splitext(os.path.basename(csv_path))[0] + '.svg'
    svg_directory = 'My_Svgs'
    if not os.path.exists(svg_directory):
        os.makedirs(svg_directory)
    svg_path = os.path.join(svg_directory, svg_filename)
    
    polylines2svg(paths_XYs, svg_path)

if __name__ == "__main__":
    main()
