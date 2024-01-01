#!/usr/bin/python3

"""this class is a module containing the storage of the
    coordinates of the polyhedron and its center"""


class Storage:
    """storage class"""
    def __init__(self):
        self.polyhedrons = []
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

