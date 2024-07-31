#!/usr/bin/python3

"""this class contains the RAS Generator logics"""
import math
import random
import numpy as np
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
    
    def generate_ellipsoid(self, d, x_min, x_max, y_min, y_max, z_min, z_max):
        """generate the ellipsoid"""
        # generate the variables of the ellipsoid
        a = (min(d) / 2) + random.uniform(0, 1) * ((max(d)/ 2) - (min(d) / 2))
        b = a * random.uniform(0, 1)
        c = a * random.uniform(0, 1)
        alpha = 2 * np.pi * random.uniform(0, 1)
        beta = 2 * np.pi * random.uniform(0, 1)
        gamma = 2 * np.pi * random.uniform(0, 1)
        x_o = x_min + random.uniform(0, 1) * (x_max - x_min)
        y_o = y_min + random.uniform(0, 1) * (y_max - y_min)
        z_o = z_min + random.uniform(0, 1) * (z_max - z_min)

        # x_ellip = np.array([
        #     [(1/a)**2,  0,       0,        0],
        #     [0,     (1/b)**2,    0,        0],
        #     [0,         0,    (1/c)**2,    0],
        #     [0,         0,       0,       -1]
        # ])
        
        # # define rotation matrix for the ellipsoid
        # Z_alpha = np.array([
        #     [np.cos(alpha), -np.sin(alpha),     0,  0],
        #     [np.sin(alpha), np.cos(alpha),      0,  0],
        #     [0,         0,                      1,  0],
        #     [0,         0,                      0,  1]
        # ])
        # X_beta = [
        #     [1,         0,          0,              0],
        #     [0,     np.cos(beta), -np.sin(beta),    0],
        #     [0,     np.sin(beta),  np.cos(beta),    0],
        #     [0,         0,                0,        1]
        # ]
        # Z_gamma = [
        #     [np.cos(gamma), -np.sin(gamma),     0,  0],
        #     [np.sin(gamma), np.cos(gamma),      0,  0],
        #     [0,         0,                      1,  0],
        #     [0,         0,                      0,  1]
        # ]
        # rot = np.matmul(Z_alpha, X_beta)
        # final_rot = np.matmul(rot, Z_gamma)
        # ellips_coor = np.matmul(final_rot, x_ellip)

        # init = np.array([
        #     [1, 0, 0, x_o],
        #     [0, 1, 0, y_o],
        #     [0, 0, 1, z_o],
        #     [0, 0, 0,   1]
        # ])
        # final = np.matmul(init, ellips_coor)
        return [a, b, c, alpha, beta, gamma, x_o, y_o, z_o]

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
                result = self.generate_ellipsoid(
                    v['diameters'],
                    self.config.x_min,
                    self.config.x_max,
                    self.config.y_min,
                    self.config.y_max,
                    self.config.z_min,
                    self.config.z_max)

                p_vol = 4 * (math.pi * (result[0] * result[0] * result[0])) / 3
                if len(self.storage.ellipsoids) > 0:
                    if self.check(result,  
                        [self.config.x_min,
                        self.config.x_max,
                        self.config.y_min,
                        self.config.y_max,
                        self.config.z_min,
                        self.config.z_max],
                        self.storage.ellipsoids,
                        self.config.sd).init_all_checks():
                        self.storage.store_ellipsoids(result)
                        vc += p_vol
                        vl = p_vol
                        print(len(self.storage.ellipsoids), v['volume'], vc)
                    else:
                        continue
                else:
                    self.storage.store_ellipsoids(result)
            if v['volume'] - vc + vl > 0:
                vr += v['volume'] - vc + vl
            del self.storage.ellipsoids[-1]
            print(v['volume'], vc, vl, vr)
            vc = 0

