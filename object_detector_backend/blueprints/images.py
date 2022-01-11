import uuid
import logging

from flask import Blueprint, request, make_response
from object_detector_backend.data.models import ImageModel, LabelModel

from object_detector_backend.data.persistence import DatabaseAPI
from object_detector_backend.data.vision import GoogleVisionAPICaller

images = Blueprint('image', __name__)
logger = logging.getLogger(__name__)


class InvalidInputException(Exception):
    """Invalid user input
    """
    def __init__(self, message: str):
        self.status_code = 400
        self.message = message
        super().__init__(self.message)

@images.route('', methods=['GET'])
def get_images():
    """
    Endpoint to retrieve images.
    If labels are provided, images with specified labels will be retrieved.
    i.e /images?objects="cat,dog"
    """
    objects = request.args.get('objects')
    db_api = DatabaseAPI()

    if objects:
        objects = [o.strip() for o in objects.strip('"').split(',')]
        to_return = db_api.get_images_by_label(labels=objects)

    else:
        to_return = db_api.get_images()
    
    return {
        'images': to_return
    }

@images.route('/<image_id>', methods=['GET'])
def get_image_by_id(image_id: str):
    """
    Retrieve image metadata and its labels  of an image with specified image_id
    """
    db_api = DatabaseAPI()
    images = db_api.get_images(id=image_id)
    
    if len(images) != 0:
        return {
            'images': images
        }
    else:
        return {}

@images.route('', methods=['POST'])
def post_images():
    """
    Post new image. If detection is enabled, 
    calls Google Vision API to annotate the image with labels.
    Image will also be labeled with user provided label.

    """
    if 'image' not in request.files.keys():
        raise InvalidInputException('image input is missing')

    _content = request.files['image'].read()
    if not(_content):
        raise InvalidInputException('a file must be uploaded as image input')

    _filename = request.form.get('filename', type=str)
    if not(_filename):
        raise InvalidInputException('filename must be provided as an input')

    _enable_detection = request.form.get('enable_detection', 'True', type=str)
    _enable_detection = _enable_detection.upper()

    _optional_label = request.form.get('label', None, type=str)

    db_api = DatabaseAPI()
    _image_id = str(uuid.uuid1())
    image = ImageModel(id=_image_id,
                       filename=_filename,
                       url=None,
                       content=_content)

    duplicate_image_found = db_api.check_duplicate_image(image)
    if not(duplicate_image_found):
        committed_image = db_api.add_image(image)
    else:
        committed_image = duplicate_image_found

    try:
        if _enable_detection == 'TRUE':
            logger.info('Detection enabled...')
            vision_client = GoogleVisionAPICaller()
            vision_labels = vision_client.annotate(content=_content)

            for label in vision_labels:
                db_api.add_label(
                    LabelModel(
                        id=str(uuid.uuid1()),
                        label=label['label'],
                        score=label['score'],
                        topicality=label['topicality'],
                        image_id=committed_image['id'],
                        source='Google Vision'
                    )
                )

        if _optional_label:
            logger.info(f'Optional label({_optional_label}) provided by the user')
            db_api.add_label(
                LabelModel(
                    id=str(uuid.uuid1()),
                    label=_optional_label,
                    image_id=committed_image['id'],
                    source='User'
                )
            )

        return make_response({
            'id': committed_image['id'],    
            'labels': db_api.get_labels_by_image_id(committed_image['id']),
        }, 200)

    except Exception as e:
        db_api.session.rollback()
        raise e

@images.route('reset', methods=['POST'])
def reset_db():
    """
    Cleans up the database file and recreate tables based on ORM schema
    """
    db_api = DatabaseAPI()
    db_api.reset()

    return make_response({
        'message': 'database recreated'
    }, 200)
