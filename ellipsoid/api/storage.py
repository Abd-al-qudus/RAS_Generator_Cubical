#!/usr/bin/python3

"""this class is a module containing the storage of the
    coordinates of the polyhedron and its center"""

import csv


class Storage:
    """storage class"""
    def __init__(self):
        self.ellipsoids = []

    def store_ellipsoids(self, coordinates):
        """stores the spheres"""
        if coordinates is None:
            raise Exception("spheres must not be null")
        if len(coordinates) == 0:
            raise Exception("spheres must not be empty")
        self.ellipsoids.append(coordinates)
    
    def export_to_csv(self):
        """export the coordinates to csv"""
        with open('ellipsoids.csv', 'w', newline='') as file_obj:
            writer = csv.writer(file_obj)
            writer.writerow(['label', 'a', 'b', 'c', 'alpha', 'beta', 'gamma', 'x', 'y', 'z'])
            [writer.writerow([i+1] + row) for i, row in enumerate(self.ellipsoids)]
