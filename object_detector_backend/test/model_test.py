from object_detector_backend.data.models import LabelModel, ImageModel

def test_image_model_creation_with_url():
    image = ImageModel(id='test12345',
                       filename='whale.jpeg',
                       url="https://files.worldwildlife.org/wwfcmsprod/images/African_Elephant_Kenya_112367/story_full_width/qxyqxqjtu_WW187785.jpg")

    assert(image.checksum)
    assert(image.content)
    assert(image.filetype == 'jpg')

def test_image_model_creation_with_content():
    with open('images/dog.jpeg', 'rb') as f:
        image = ImageModel(id='test12345',
                           filename='whale.jpeg',
                           content = f.read())

        assert(image.checksum)
        assert(image.content)
        assert(image.filetype == 'jpeg')
        assert(image.url is None)

def test_create_image_without_content():
    try:
        image = ImageModel(id='test12345',
                           filename='whale.jpeg')

        assert(False)
    except Exception:
        pass