import svgwrite
import numpy as np

def polylines2svg(paths_XYs, svg_path):
    W, H = 0, 0
    for path_XYs in paths_XYs:
        for XY in path_XYs:
            W, H = max(W, np.max(XY[:, 0])), max(H, np.max(XY[:, 1]))
    padding = 0.1
    W, H = int(W + padding * W), int(H + padding * H)

    dwg = svgwrite.Drawing(svg_path, size=(W, H), profile='tiny', shape_rendering='crispEdges')
    
    group = dwg.g()
    colors = ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black']
    for i, path in enumerate(paths_XYs):
        path_data = []
        color = colors[i % len(colors)]
        for XY in path:
            path_data.append(("M", (XY[0, 0], XY[0, 1])))
            for j in range(1, len(XY)):
                path_data.append(("L", (XY[j, 0], XY[j, 1])))
            if not np.allclose(XY[0], XY[-1]):
                path_data.append(("Z", None))
        group.add(dwg.path(d=path_data, fill='none', stroke=color, stroke_width=2))
    dwg.add(group)
    dwg.save()
