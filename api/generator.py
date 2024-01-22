#!/usr/bin/python3

"""this class contains the RAS Generator logics"""
import math
import random
from scipy.spatial import ConvexHull
from configurations import Configuration
from storage import Storage
from checker import Checker


class Generator:
    """generates the RAS coordinates"""
    def __init__(self, config, storage):
        if not isinstance(config, Configuration):
            raise Exception('config must be a configuration class')
        self.config = config
        if not isinstance(storage, Storage):
            raise Exception('storage must be a storage class')
        self.storage = storage
        self.check = Checker

    def compute_volume(self, d, vf, vc, n, r_min, r_max):
        """compute the volume per segment for generation of aggregates"""
        volume = []
        for i in range(len(d)):
            if i + 1 != len(d):
                p_d = 100 * ((d[i] / r_max) ** n)
                p_nd = 100 * ((d[i + 1] / r_max) ** n)
                p_mnd = 100 * ((r_min / r_max) ** n)
                p_mxd = 100 * ((r_max / r_max) ** n)
                bound_vol = ((p_nd - p_d) / (p_mxd - p_mnd)) * vf * vc
                vol_obj = {
                            'volume': bound_vol,
                            'diameters': [d[i], d[i + 1]]
                        }
                volume.append(vol_obj)
        volume = sorted(volume, key=lambda k: k['diameters'])
        volume = volume[-1::-1]
        return volume
    
    def generate_polyhedron(self, d, x_min, x_max, y_min, y_max, z_min, z_max, n_min, n_max):
        """generate polyhedrons faces"""
        poly_coordinates = []
        r = (min(d) / 2) + random.uniform(0, 1) * ((max(d)/ 2) - (min(d) / 2))
        n = n_min + random.uniform(0, 1) * (n_max - n_min)
        x_o = x_min + random.uniform(0, 1) * (x_max - x_min)
        y_o = y_min + random.uniform(0, 1) * (y_max - y_min)
        z_o = z_min + random.uniform(0, 1) * (z_max - z_min)
        for i in range(round(n)):
            polar_corr = random.uniform(0, 1)
            azimuth_corr = random.uniform(0, 1)
            azimuth_angle = azimuth_corr * math.pi
            polar_angle = polar_corr * math.pi * 2
            x_i = r * math.cos(polar_angle) * math.sin(azimuth_angle) + x_o
            y_i = r * math.cos(azimuth_angle) * math.sin(polar_angle) + y_o
            z_i = r * math.cos(azimuth_angle) + z_o
            poly_coordinates.append([x_i, y_i, z_i])
        return poly_coordinates, [x_o, y_o, z_o, r]

    def wrapper(self):
        """initialize the operation"""
        vc = 0
        vr = 0
        vl = 0
        volumes = self.compute_volume(
            self.config.diameters,
            self.config.vf,
            self.config.vc,
            self.config.n,
            self.config.r_min,
            self.config.r_max
        )
        print(volumes)
        for v in volumes:
            print(v['diameters'])
            if vr > 0:
                v['volume'] += vr
                vr = 0
            while vc <= v['volume']:
                result, center = self.generate_polyhedron(
                    v['diameters'],
                    self.config.x_min,
                    self.config.x_max,
                    self.config.y_min,
                    self.config.y_max,
                    self.config.z_min,
                    self.config.z_max,
                    self.config.n_min,
                    self.config.n_max)
                p_vol = ConvexHull(result).volume
                if len(self.storage.polyhedrons) > 0:
                    if self.check(result, 
                        self.storage.polyhedrons, 
                        [self.config.x_min,
                        self.config.x_max,
                        self.config.y_min,
                        self.config.y_max,
                        self.config.z_min,
                        self.config.z_max], 
                        center, 
                        self.storage.centers,
                        self.config.sd).init_all_checks():
                        self.storage.store_polyhedrons(result)
                        self.storage.store_centers(center)
                        vc += p_vol
                        vl = p_vol
                        print(len(self.storage.polyhedrons), v['volume'], vc)
                        # print(result)
                    else:
                        continue
                else:
                    self.storage.store_polyhedrons(result)
                    self.storage.store_centers(center)
            if v['volume'] - vc + vl > 0:
                vr += v['volume'] - vc + vl
            del self.storage.polyhedrons[-1]
            del self.storage.centers[-1]
            print(v['volume'], vc, vl, vr)
            vc = 0

