from object_detector_backend.data.models import LabelModel, ImageModel

def test_image_model_creation():
    image = ImageModel('test12345', 'whale.jpeg', None)
    assert(image.filetype == 'jpeg')
