#!/usr/bin/python3

"""this class visualizes the generated coordinates"""

import matplotlib.pyplot as plt
import numpy as np
from random import randint as rd


class Visualizer:
    """visualize the coordinates with matplotlib"""

    def __init__(self, spheres):
        self.spheres = spheres

    def visualize(self):
        """visualize a set of polyhedrons"""
        color = (rd(0, 255)/255, 1.0, rd(0, 255)/255, 1.0)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for sphere in self.spheres:
            x_center, y_center, z_center, radius = sphere
            u = np.linspace(0, 2 * np.pi, 100)
            v = np.linspace(0, np.pi, 100)
            u, v = np.meshgrid(u, v)
            x = x_center + radius * np.cos(u) * np.sin(v)
            y = y_center + radius * np.sin(u) * np.sin(v)
            z = z_center + radius * np.cos(v)
            ax.plot_surface(x, y, z, color=color)
            # ax.scatter([x_center], [y_center], [z_center], color='r', s=100)

        ax.set_box_aspect([1, 1, 1])
        plt.show()
