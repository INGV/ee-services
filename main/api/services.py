
import sys
sys.path.append('.')
from main.ellipsoid.ellipsoid import Ellipsoid
from flask_api import status as http_status_code
import json


#"python main/api/queries.py"
class Services():

    def __init__(self):
        pass

    def make_ellipsoid_post(self, quakeml):
        try:
            latitude, longitude, delta, xx, xy, yy = self.parse_quakeml(quakeml)

            ellipsoid = Ellipsoid(latitude, longitude, delta, xx, xy, yy)
            geojson = ellipsoid.make_ee_ellipsoid()
            return geojson, http_status_code.HTTP_200_OK
        except Exception as e:
            return json.dumps({'error': str(e)}), http_status_code.HTTP_500_INTERNAL_SERVER_ERROR

    def make_ellipsoid_get(self, lat, lon, delta, xx, xy, yy):
        try:
            ellipsoid = Ellipsoid(lat, lon, delta, xx, xy, yy)
            geojson = ellipsoid.make_ee_ellipsoid()
            return geojson, http_status_code.HTTP_200_OK
        except Exception as e:
            return json.dumps({'error': str(e)}), http_status_code.HTTP_500_INTERNAL_SERVER_ERROR

    def parse_quakeml(self, quakeml):
        return 40.6, 13.2, 1, 111, 55.5, 111

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='early-est ellipsoid',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-f", "--qml_file", type=str, help="quakeml file path")
    parser.add_argument("-s", "--qml_string", type=str, help="quakeml string")
    parser.add_argument("-p", "--plot", action='store_true', help="Plot the elipsoid")
    parser.add_argument("-l", "--lat", type=float, help="latitude")
    parser.add_argument("-o", "--lon", type=float, help="longitude")
    parser.add_argument("-d", "--delta", type=float, help="delta")
    parser.add_argument("-x", "--covxx", type=float, help="coovariance xx")
    parser.add_argument("-y", "--covyy", type=float, help="coovariance yy")
    parser.add_argument("-z", "--covxy", type=float, help="coovariance xy")

    args = parser.parse_args()

    services = Services()

    if args.qml_file or args.qml_string:
        quakeml = None
        if args.qml_file:
            with open (args.qml_file, 'r') as f:
                quakeml = f.read()
        elif args.qml_string:
            quakeml = args.qml_string

        lat, lon, delta, covxx, covxy, covyy = services.parse_quakeml(quakeml)
        ellipsoid = Ellipsoid(lat, lon, delta, covxx, covxy, covyy)

    else:
        for option in ['lat', 'lon', 'delta', 'covxx', 'covxy', 'covyy']:
            if not option in args:
                print(f"ERROR! missing option {option}")
                exit()

        ellipsoid = Ellipsoid(args.lat, args.lon, args.delta, args.covxx, args.covxy, args.covyy)

    geojson = ellipsoid.make_ee_ellipsoid()
    print (geojson)

    if args.plot:
        ellipsoid.plot_elipsoid()