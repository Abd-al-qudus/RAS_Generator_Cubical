#!/usr/bin/python3

"""this class visualizes the generated coordinates"""

import matplotlib.pyplot as plt
import numpy as np
from random import randint as rd


class Visualizer:
    """visualize the coordinates with matplotlib"""

    def __init__(self, ellipsoids):
        self.ellipsoids = ellipsoids

    def generate_ellipsoid(self, a, b, c, alpha, beta, gamma, center):
        # Parametric angles
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        
        # Ellipsoid surface parameterization
        x = a * np.outer(np.cos(u), np.sin(v))
        y = b * np.outer(np.sin(u), np.sin(v))
        z = c * np.outer(np.ones_like(u), np.cos(v))
        
        # Rotation matrices
        Rz = np.array([
            [np.cos(alpha), -np.sin(alpha), 0],
            [np.sin(alpha), np.cos(alpha), 0],
            [0, 0, 1]
        ])
        
        Ry = np.array([
            [np.cos(beta), 0, np.sin(beta)],
            [0, 1, 0],
            [-np.sin(beta), 0, np.cos(beta)]
        ])
        
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(gamma), -np.sin(gamma)],
            [0, np.sin(gamma), np.cos(gamma)]
        ])
        
        # Combined rotation matrix
        R = Rz @ Ry @ Rx
        # print(R)
        # Apply rotation
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                [x[i, j], y[i, j], z[i, j]] = np.dot(R, [x[i, j], y[i, j], z[i, j]])
        
        # Translate to center
        x += center[0]
        y += center[1]
        z += center[2]
        
        return x, y, z

    def visualize(self):
        """visualize a set of polyhedrons"""
        color = (rd(0, 255)/255, 1.0, rd(0, 255)/255, 1.0)
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for ellips in self.ellipsoids:
            x, y, z = self.generate_ellipsoid(
                ellips[0],
                ellips[1],
                ellips[2],
                ellips[3],
                ellips[4],
                ellips[5],
                [ ellips[6], ellips[7], ellips[8] ]
            )
            ax.plot_surface(x, y, z, color=color)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()
