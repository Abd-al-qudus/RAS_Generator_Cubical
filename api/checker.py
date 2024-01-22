#!/usr/bin/python3

"""this class contains all the check cases"""

import numpy as np
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon


class Checker:
    """contains the checks on each polygons"""

    def __init__(self, poly_A, polyhedrons, bounds, center_A, center_B, min_d):
        """initialize the checker class"""
        self.poly_A = poly_A
        self.polyhedrons = polyhedrons
        self.bounds = bounds
        self.center_A = center_A
        self.centers = center_B
        self.min_d = min_d

    def init_check_polygon_in_bound(self, polyhedron, bounds):
        """check the conditions of the polyhedron"""
        check_x = False
        check_y = False
        check_z = False
        coor_x = [coor[0] for coor in polyhedron]
        coor_y = [coor[1] for coor in polyhedron]
        coor_z = [coor[2] for coor in polyhedron]
        x_min, x_max, y_min, y_max, z_min, z_max = bounds
        x_m = min(coor_x); x_ma = max(coor_x)
        y_m = min(coor_y); y_ma = max(coor_y)
        z_m = min(coor_z); z_ma = max(coor_z)
        if x_m > x_min + self.min_d and x_max - self.min_d > x_ma:
            check_x = True
        if y_m > y_min + self.min_d and y_max - self.min_d > y_ma:
            check_y = True
        if z_m > z_min + self.min_d and z_max - self.min_d > z_ma:
            check_z = True
        return check_x and check_y and check_z

    def init_generate_det_xyz(self, points):
        """generate the determinants of x, y and z"""
        det_x = np.linalg.det([[points[1][1] - points[0][1], points[1][2] - points[0][2]],
                            [points[2][1] - points[0][1], points[2][2] - points[0][2]]])
        det_y = np.linalg.det([[points[1][2] - points[0][2], points[1][0] - points[0][0]],
                            [points[2][2] - points[0][2], points[2][0] - points[0][0]]])
        det_z = np.linalg.det([[points[1][0] - points[0][0], points[1][1] - points[0][1]],
                            [points[2][0] - points[0][0], points[2][1] - points[0][1]]])
        return det_x, det_y, det_z

    def init_generate_Gdet_matrix(self, polyhedron):
        """generate the GO matrix"""
        hull = ConvexHull(polyhedron)
        random_plane = hull.simplices[0]
        points = hull.points[random_plane]
        det_x, det_y, det_z = self.init_generate_det_xyz(points)
        return det_x, det_y, det_z, points[0][0], points[0][1], points[0][2]

    def init_generate_G_matrix(self, polyhedron, vertex):
        """generate the G matrix"""
        d_x, d_y, d_z, x_o, y_o, z_o = self.init_generate_Gdet_matrix(polyhedron)
        G_matrix = ((vertex[0] - x_o) * d_x) + ((vertex[1] - y_o) * d_y) + ((vertex[2] - z_o) * d_z)
        return G_matrix

    def init_is_intersecting(self, polyhedrons, poly_R):
        """check whether polyhedron Left and polyhedron Right do not intersect
        the equation is defined by G(x, y, z) x G(xi, yi, zi) = 0"""
        # mean_O_R = np.mean(poly_R, axis=0)
        # G_O_matrix = self.init_generate_G_matrix(poly_R, mean_O_R)
        # for vert in polyhedrons:
        #     for vertex in vert:
        #         G_V_matrix = self.init_generate_G_matrix(poly_R, vertex)
        #         if G_V_matrix * G_O_matrix >= 0:
        #             return False

        # return True
        # convexhall computation makes it slower
        # G matrix computation makes it faster
        for poly_L in polyhedrons:
            poly_l = Polygon(poly_L)
            poly_r = Polygon(poly_R)
            check = poly_l.convex_hull.intersects(poly_r.convex_hull)
            if check == True:
                return False
            
        return True
    
    def project_onto_axis(self, vertices, axis):
        # Project vertices onto the axis and return the min and max values
        projections = np.dot(vertices, axis)
        return np.min(projections), np.max(projections)

    def separating_axis_test(self, polyhedrons, polyhedron2):
        # Check for intersection along each axis
        for polyhedron1 in polyhedrons:
            for axis in polyhedron1 + polyhedron2:
                min1, max1 = self.project_onto_axis(polyhedron1, axis)
                min2, max2 = self.project_onto_axis(polyhedron2, axis)

                if max1 < min2 or max2 < min1:
                    # Polyhedra are separated along this axis, no intersection
                    return False

            # If no separation along any axis, polyhedra intersect
        return True

    def init_is_radially_separated(self, poly_L, centers):
        """check the radial separation of the two polyhedrons,
        the poly martix contains coordinates of O and r"""
        for poly_R in centers:
            check = (((poly_L[0] - poly_R[0]) ** 2) + ((poly_L[1] - poly_R[1]) ** 2 + (poly_L[2] - poly_R[2]) ** 2) ** 0.5) - (poly_L[3] + poly_R[3]) > self.min_d * poly_L[3] * 2
            if check == False:
                return check
        return True

    def init_all_checks(self):
        """check whether the polyhedron is not overriding others"""
        radial = self.init_is_radially_separated(self.center_A, self.centers)
        bound = self.init_check_polygon_in_bound(self.poly_A, self.bounds)
        # return radial and bound

        # intersect = self.separating_axis_test(self.polyhedrons, self.poly_A)
        # if intersect:
        #     return bound and radial and False
        # else:
        #     return bound and radial and True
        intersect = self.init_is_intersecting(self.polyhedrons, self.poly_A)
        return bound and radial and intersect

