#!/usr/bin/python3

"""this class is a module containing the storage of the
    coordinates of the polyhedron and its center"""

import csv


class Storage:
    """storage class"""
    def __init__(self):
        self.polyhedrons = []
        self.hull = []
        self.centers = []

    def store_polyhedrons(self, coordinates):
        """stores the polyhedron"""
        if coordinates is None:
            raise Exception("coordinates must not be null")
        if len(coordinates) == 0:
            raise Exception("coordinates must not be empty")
        self.polyhedrons.append(coordinates)
    
    def store_centers(self, coordinates):
        """stores the centers"""
        if coordinates is None:
            raise Exception("coordinates must not be null")
        if len(coordinates) == 0:
            raise Exception("coordinates must not be empty")
        self.centers.append(coordinates)

    def export_to_csv(self):
        """export the coordinates to csv"""
        with open('coordinates_40.csv', 'w', newline='') as file_obj:
            writer = csv.writer(file_obj)
            writer.writerow(['node-label', 'x', 'y', 'z'])
            [writer.writerow([i+1] + row) for i, rows in enumerate(self.polyhedrons) for row in rows]

        with open('hulls_40.csv', 'w', newline='') as file_obj:
            writer = csv.writer(file_obj)
            writer.writerow(['polygon-label', 'a', 'b', 'c'])
            [writer.writerow([i+1] + row) for i, rows in enumerate(self.hull) for row in rows]