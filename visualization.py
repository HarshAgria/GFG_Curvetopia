import matplotlib.pyplot as plt

def plot(paths_XYs, title="Plot"):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    colors = ['blue', 'green', 'red', 'purple', 'orange']
    for i, XYs in enumerate(paths_XYs):
        if XYs:
            color = colors[i % len(colors)]
        for XY in XYs:
            ax.plot(XY[:, 0], XY[:, 1], c=color, linewidth=2)
    ax.set_aspect('equal')
    plt.title(title)
    plt.show()
