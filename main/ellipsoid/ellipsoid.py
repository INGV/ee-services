import numpy as np
import matplotlib.pyplot as plt
from geojson import Polygon
import json
import math

class Ellipsoid(object):

    def __init__(self, latitude, longitude, delta = 1, xx = 10, xy = 10, yy = 10):
        self.latitude = latitude
        self.longitude = longitude
        self.delta_d = delta
        self.xx = xx
        self.xy = xy
        self.yy = yy

    def make_geojson(self, **kwargs):

        polygon = kwargs.get('polygon', None)
        phase_file = kwargs.get('phase_file', None)

        a = Polygon(([polygon]))

        # phase = phase_file.split('_')[-1].split('.')[0]

        geometries = {
            "type": "Feature",
            "geometry": a,
            "properties": {
                "name": 'uncertainty ellipse'
            }}

        return json.dumps(geometries)

    def cov2ele(self, **kwargs):

        xx = kwargs.get('xx', None)
        xy = kwargs.get('xy', None)
        yy = kwargs.get('yy', None)

        # Qui riporto on radianti i miei valori iniziali esperssi in km
        xx = np.radians(xx / 111)
        xy = np.radians(xy / 111)
        yy = np.radians(yy / 111)

        ra2deg = 180 / np.pi
        DELTA_CHI_SQR_68_2 = 2.3

        out = dict()

        A = np.array([[xx, xy], [xy, yy]])
        V, W, Vh = np.linalg.svd(A, full_matrices=True)
        W = np.degrees(W)
        ell_az1 = math.atan2(V[0][0], V[1][0])
        ell_az1 = np.degrees(ell_az1)

        if ell_az1 < 0:
            ell_az1 = ell_az1 + 360
        if ell_az1 >= 360:
            ell_az1 = ell_az1 - 360
        if ell_az1 >= 180:
            ell_az1 = ell_az1 - 180

        ell_len1 = math.sqrt(DELTA_CHI_SQR_68_2) / math.sqrt(1 / W[0])
        ell_len2 = math.sqrt(DELTA_CHI_SQR_68_2) / math.sqrt(1 / W[1])

        out['l1'] = ell_len1
        out['l2'] = ell_len2
        out['theta'] = ell_az1

        return out

    def ele2points(self, **kwargs):

        ele = kwargs.get('elips', None)
        lat = kwargs.get('lat', 0)
        lon = kwargs.get('lon', 0)
        dd = kwargs.get('dd', None)

        dd = np.radians(dd)
        a = np.radians(ele['l1'])
        b = np.radians(ele['l2'])
        t = np.radians(ele['theta'])  # radians

        tt = np.arange(0, 2 * np.pi, dd)
        x, y = np.array([a * np.cos(tt), b * np.sin(tt)])

        ele['x'] = np.degrees(x)
        ele['y'] = np.degrees(y)
        ele['lat'] = np.degrees(lat)
        ele['lon'] = np.degrees(lon)

        return ele

    def rotate(self, **kwargs):

        ele = kwargs.get('elips', None)
        lat = kwargs.get('lat', 0)
        lon = kwargs.get('lon', 0)

        t = ele['theta']
        x = ele['x']
        y = ele['y']

        t = np.radians(t)
        x = np.radians(x)
        y = np.radians(y)

        cos_rad = np.cos(t)
        sin_rad = np.sin(t)

        qx = 1 * cos_rad * x - sin_rad * y
        qy = 1 * sin_rad * x + cos_rad * y

        #print(qx)
        #print(np.degrees(qx))

        vector = np.vectorize(np.float_)

        ele['x_rotated'] = vector(np.degrees(qx) + lon)
        ele['y_rotated'] = vector(np.degrees(qy) + lat)
        ele['x'] = np.degrees(x)
        ele['y'] = np.degrees(y)

        return ele


    def make_ee_ellipsoid(self):
        self.elipsoid = self.cov2ele(xx=self.xx, xy=self.xy, yy=self.yy)

        self.elipsoid = self.ele2points(elips=self.elipsoid, lat=self.latitude, lon=self.longitude, dd=self.delta_d)

        self.elipsoid = self.rotate(elips=self.elipsoid, lat=self.latitude, lon=self.longitude)

        matrix = [[0] * 2 for i in range(len(self.elipsoid['x_rotated']))]

        for i in range(len(self.elipsoid['x_rotated'])):
            matrix[i][0] = self.elipsoid['x_rotated'][i]
            matrix[i][1] = self.elipsoid['y_rotated'][i]

        geojson = self.make_geojson(polygon=matrix)

        return geojson
        # Qui mettere il geogison

    def plot_elipsoid(self):
        plt.scatter(self.elipsoid['x_rotated'], self.elipsoid['y_rotated'])
        plt.scatter(self.longitude, self.latitude)
        plt.show()
