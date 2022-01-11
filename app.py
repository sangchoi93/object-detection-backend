import argparse
import logging
import traceback
import os

from flask import Flask
from flask import make_response

from object_detector_backend.blueprints.images import images


app = Flask(__name__)
app.register_blueprint(images, url_prefix='/images')

app.config.from_mapping(
    SECRET_KEY='dev',
    # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

# TODO: More specific exception to distinguish between client/service side errors
@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    traceback.print_exc()
    response = make_response({
        'message': str(e)}, getattr(e, 'status_code', 500))
    return response

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--cred', required=True, help='Filepath to Google API Auth file')
    args = parser.parse_args()

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = args.cred
    
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
    app.run(host='0.0.0.0', port=8080, debug=True)
