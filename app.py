import argparse
import logging
import traceback
import os
import requests

from flask import Flask
from flask import make_response

from object_detector_backend.blueprints.images import images


app = Flask(__name__)
app.register_blueprint(images, url_prefix='/images')


@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    traceback.print_exc()
    response = make_response({
        'message': str(e)}, getattr(e, 'status_code', 500))
    return response

@app.errorhandler(requests.exceptions.HTTPError)
def handle_exception(e):
    """User has provided invalid URL"""
    traceback.print_exc()
    response = make_response({
        'message': str(e)}, getattr(e, 'status_code', 400))
    return response

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cred', required=True, help='Filepath to Google API Auth file')
    args = parser.parse_args()

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = args.cred
    
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port=8080, debug=True)
