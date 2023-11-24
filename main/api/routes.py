import flask_api.status
from main.api import util
from flask import Blueprint, jsonify, render_template
from flask import (
    request,
    Response,
    make_response
)
from flask_api import status as http_status_code
from main import logger
from main.api.services import Services
route = Blueprint('webserver', __name__)
from flask_cors import CORS
from datetime import datetime

cors = CORS(route, resources={r"/*": {"origins": "*"}})

services = Services()

errors = Blueprint('webservsr_errors', __name__)
@errors.app_errorhandler(Exception)

def handle_unexpected_error(error):
    status_code = 500
    return f"{type(error)}, {str(error)}", status_code

@route.before_request
def before_request_callback():
    path = request.path
    method = request.method
    logger.info(path + " [" + method + "]")

@route.route('/api/test', methods=["GET"])
def test():
    return 'test OK!!'


@route.route('/api/make_ee_ellipsoid', methods=["GET"])
def make_ee_ellipsoid_GET():
    args = request.args
    for param in ['lat', 'lon', 'delta', 'xx', 'xy', 'yy']:
        if not param in args:
            raise Exception(f"Missing parameter [{param}]")
    lat = float(args['lat'])
    lon = float(args['lon'])
    delta = float(args['delta'])
    xx = float(args['xx'])
    xy = float(args['xy'])
    yy = float(args['yy'])
    json_data, status = services.make_ellipsoid_get(lat, lon, delta, xx, xy, yy)
    if status != http_status_code.HTTP_200_OK:
        json_data = util.completeErrorStruct(request, json_data)
    result = (Response(json_data, content_type='application/json'), status)
    return result

@route.route('/api/make_ee_ellipsoid', methods=["POST"])
def make_ee_ellipsoid_POST():
    quakeml = request.get_json(force=True)
    json_data, status = services.make_ellipsoid_post(quakeml)
    if status != http_status_code.HTTP_200_OK:
        json_data = util.completeErrorStruct(request, json_data)
    result = (Response(json_data, content_type='application/json'), status)
    return result
