#!/usr/bin/python3

"""This class contains all the check cases.
    the sole checks are based on the boundary check 
    and the radial check. The geometric intersection
    check is not used in this case"""

from math import sqrt


class Checker:
    """contains the checks on each polygons"""

    def __init__(self, ellipsoid, bounds, ellipsoids, sd):
        """initialize the checker class"""
        self.ellipsoid = ellipsoid
        self.bounds = bounds
        self.ellipsoids = ellipsoids
        self.sd = sd

    def init_check_ellipsoid_in_bound(self, ellipsoid, bounds):
        """
            checker for the boundary conditions of the polyhedron,
            considering wall effect, each polyhedron at the 
            boundary is at a distance of size distribution * 
                diameter of the polyhedron
        """
        x_min, x_max, y_min, y_max, z_min, z_max = bounds
        if ellipsoid[6] + ellipsoid[0] < x_min + (self.sd * self.ellipsoid[0]) or ellipsoid[0] + ellipsoid[6] > x_max - (self.sd * self.ellipsoid[0]):
            return False
        if ellipsoid[7] + ellipsoid[1] < y_min + (self.sd * self.ellipsoid[1]) or ellipsoid[7] + ellipsoid[1] > y_max - (self.sd * self.ellipsoid[1]):
            return False
        if ellipsoid[8] + ellipsoid[2] < z_min + (self.sd * self.ellipsoid[2]) or ellipsoid[2] + ellipsoid[8] > z_max - (self.sd * self.ellipsoid[2]):
            return False
        return True

    def init_is_radially_separated(self, ellips, centers):
        """check the radial separation of the two sphere"""
        for center in centers:
            dist = sqrt(((center[6] - ellips[6])**2) + ((center[7] - ellips[7])**2) + ((center[8] - ellips[8])**2))
            if dist <= 1.2 * (center[0] + ellips[0]):
                return False
        return True

    def init_all_checks(self):
        """check whether the polyhedron is not overriding others"""
        radial = self.init_is_radially_separated(self.ellipsoid, self.ellipsoids)
        bound = self.init_check_ellipsoid_in_bound(self.ellipsoid, self.bounds)
        return bound and radial
