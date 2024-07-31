#!/usr/bin/python3

"""this class visualizes the generated coordinates"""

from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from random import randint as rd


class Visualizer:
    """visualize the coordinates with matplotlib"""

    def __init__(self, polyhedrons, cv_hull):
        self.polyhedrons = polyhedrons
        self.chull = cv_hull

    def visualize(self):
        """visualize a set of polyhedrons"""
        color = (rd(0, 255)/255, 1.0, rd(0, 255)/255, 1.0)
        volume = 0
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for polyhedron in self.polyhedrons:
            polyhedron = np.array(polyhedron)
            hull = ConvexHull(polyhedron)
            self.chull.append(hull.simplices.tolist())
            ax.plot_trisurf(polyhedron[:, 0], polyhedron[:, 1], polyhedron[:, 2], triangles=hull.simplices, color=color)
            volume += hull.volume

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        print(f"volume is {volume}")

        plt.show()
