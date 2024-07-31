#!/usr/bin/python3

"""This class contains all the check cases.
    the sole checks are based on the boundary check 
    and the radial check. The geometric intersection
    check is not used in this case"""

from math import sqrt


class Checker:
    """contains the checks on each polygons"""

    def __init__(self, coordinates, rad, h, centers, sd):
        """initialize the checker class"""
        self.coordinates = coordinates
        self.h = h
        self.rad = rad
        self.centers = centers
        self.sd = sd

    def init_check_sphere_in_bound(self):
        """
            checker for the boundary conditions of the polyhedron,
            considering wall effect, each polyhedron at the 
            boundary is at a distance of size distribution * 
                diameter of the polyhedron
        """
        xy = ((self.rad - self.coordinates[0])**2 + (self.rad - self.coordinates[1])**2)**0.5
        if xy + self.coordinates[3] > self.rad - 0.1:
            return False
        if self.coordinates[0] - self.coordinates[3] < 0.1 or self.coordinates[0] + self.coordinates[3] > 2 * self.rad - 0.1:
            return False
        if self.coordinates[2] - self.coordinates[3] < 0.1 or self.coordinates[2] + self.coordinates[3] > self.h - 0.1:
            return False
        return True

    def init_is_radially_separated(self):
        """check the radial separation of the two sphere"""
        for center in self.centers:
            dist = sqrt(((center[0] - self.coordinates[0])**2) + ((center[1] - self.coordinates[1])**2) + ((center[2] - self.coordinates[2])**2))
            if dist <= 1.05 * (center[3] + self.coordinates[3]):
                return False
        return True

    def init_all_checks(self):
        """check whether the polyhedron is not overriding others"""
        radial = self.init_is_radially_separated()
        bound = self.init_check_sphere_in_bound()
        return bound and radial
