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

    def compute_volume(self, d, vf, vc, n, d_min, d_max):
        """compute the volume per segment for generation of aggregates"""
        volume = []
        p_mnd = 100 * ((d_min / d_max) ** n)
        p_mxd = 100 * ((d_max / d_max) ** n)
        for i in range(len(d)):
            if i + 1 != len(d):
                p_d = 100 * ((d[i] / d_max) ** n)
                p_nd = 100 * ((d[i + 1] / d_max) ** n)
                bound_vol = ((p_nd - p_d) / (p_mxd - p_mnd)) * vf * vc
                vol_obj = {
                            'volume': bound_vol,
                            'diameters': [d[i], d[i + 1]]
                        }
                volume.append(vol_obj)
        volume = sorted(volume, key=lambda k: k['diameters'])
        volume = volume[-1::-1]
        return volume
    
    def generate_sphere(self, d, rad, h):
        """generate polyhedrons faces"""
        r = (min(d) / 2) + random.uniform(0, 1) * ((max(d)/ 2) - (min(d) / 2))
        x_o = random.uniform(0, 1) * rad * 2
        y_o = random.uniform(0, 1) * rad * 2
        z_o = random.uniform(0, 1) * h
        return [x_o, y_o, z_o, r]

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
            self.config.d_min,
            self.config.d_max
        )
        print(volumes)
        for v in volumes:
            print(v['diameters'])
            if vr > 0:
                v['volume'] += vr
                vr = 0
            while vc <= v['volume']:
                result = self.generate_sphere(
                    v['diameters'],
                    self.config.rad,
                    self.config.height)

                p_vol = 4 * (math.pi * (result[3]**3)) / 3
                if len(self.storage.spheres) > 0:
                    if self.check(result,  
                        self.config.rad,
                        self.config.height,
                        self.storage.spheres,
                        self.config.sd).init_all_checks():
                        self.storage.store_spheres(result)
                        vc += p_vol
                        vl = p_vol
                        print(len(self.storage.spheres), v['volume'], vc)
                    else:
                        continue
                else:
                    if self.check(result,  
                        self.config.rad,
                        self.config.height,
                        self.storage.spheres,
                        self.config.sd).init_check_sphere_in_bound():
                        self.storage.store_spheres(result)
            if v['volume'] - vc + vl > 0:
                vr += v['volume'] - vc + vl
            del self.storage.spheres[-1]
            print(v['volume'], vc, vl, vr)
            vc = 0

