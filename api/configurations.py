#!/usr/bin/python3

"""this class contains the configuration of the 
    RAS Generator"""


class Configuration:
    """contains the RAS generator configuration"""
    def __init__(self, d, vf, vol_n, sd, **kwargs):
        if not isinstance(d, list):
            raise Exception('d must be a list containing the diameters')
        if len(d) == 0:
            raise Exception('diameters must not be empty')
        self.diameters = d
        for keys in kwargs.keys():
            if not isinstance(kwargs.get(keys), (float, int)) or kwargs.get(keys) < 0:
                raise Exception('arguments must be an integer or float and greater than 0')
        self.vf= vf
        self.n = vol_n
        self.sd = sd
        self.x_min = kwargs.get('x_min', None)
        self.x_max = kwargs.get('x_max', None)
        self.y_min = kwargs.get('y_min', None)
        self.y_max = kwargs.get('y_max', None)
        self.z_min = kwargs.get('z_min', None)
        self.z_max = kwargs.get('z_max', None)
        if kwargs.get('n_min') < 8 and kwargs.get('n_max') > 17:
            raise Exception('n values are bound within 8 and 16')
        if kwargs.get('n_max') < kwargs.get('n_min'):
            raise Exception('minimum and maximum values incorrectly configured')
        self.n_min = kwargs.get('n_min', None)
        self.n_max = kwargs.get('n_max', None)
        self.vc = self.x_max * self.y_max * self.z_max
        self.r_min = min(self.diameters)
        self.r_max = max(self.diameters)
