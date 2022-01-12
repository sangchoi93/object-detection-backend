import uuid

from object_detector_backend.data.persistence import Labels, Images
from object_detector_backend.data.models import LabelModel, ImageModel

def test_get_images(setup_database):
    """Tests posting an image and retrieving it
    """
    # Nothing has been inserted
    db = setup_database
    assert(db.get_images() == [])

    image_id = str(uuid.uuid1())
    with open('images/whale.jpeg', 'rb') as image_file:
        db.add_image(ImageModel(
            id=image_id,
            filename='whale.jpeg',
            url=None,
            content=image_file.read()
        ))


    assert(len(db.get_images()) == 1)
    assert(db.get_images()[0]['id'] == image_id)

    with open('images/cat.jpeg', 'rb') as image_file:
        db.add_image(ImageModel(
            id=str(uuid.uuid1()),
            filename='cat.jpeg',
            url=None,
            content=image_file.read()
        ))

    assert(len(db.get_images()) == 2)
    assert(db.get_images()[0]['id'] == image_id)

def test_post_duplicate_image(setup_database):
    """Tests posting an image and retrieving it
    """
    db = setup_database

    image_id = str(uuid.uuid1())
    with open('images/whale.jpeg', 'rb') as image_file:
        db.add_image(ImageModel(
            id=image_id,
            filename='whale.jpeg',
            url=None,
            content=image_file.read()
        ))

    with open('images/whale.jpeg', 'rb') as image_file:
        db.add_image(ImageModel(
            id=str(uuid.uuid1()),
            filename='whale.jpeg',
            url=None,
            content=image_file.read()
        ))


    # ensure there is only 1 image created
    images = db.get_images()
    assert(len(images) == 1)

    # the only created image should have the image id of the first entry
    assert(images[0]['id'] == image_id)

def test_post_duplicate_image_2(setup_database):
    """Try to create another entry with the same file content \
    but with different file filename.
    the add_image should treat them as two different images to insert
    """
    db = setup_database

    image_id = str(uuid.uuid1())
    with open('images/whale.jpeg', 'rb') as image_file:
        db.add_image(ImageModel(
            id=image_id,
            filename='whale.jpeg',
            url=None,
            content=image_file.read()
        ))

    with open('images/whale.jpeg', 'rb') as image_file:
        db.add_image(ImageModel(
            id=str(uuid.uuid1()),
            filename='cat.jpeg',
            url=None,
            content=image_file.read()
        ))

    # ensure both images are created
    assert(len(db.get_images()) == 2)

def test_get_images_by_label(setup_database):
    db = setup_database
    dog_image_id = str(uuid.uuid1())
    cat_image_id = str(uuid.uuid1())

    db.session.add(Images(id=dog_image_id,
                            filename='dog',
                            content=b'1234',
                            url='test'))

    db.session.add(Images(id=cat_image_id,
                  filename='cat',
                  content=b'1234',
                  url='test'))

    db.session.add(Labels(id=str(uuid.uuid1()),
                  label='dog',
                  score=0.123,
                  topicality=0.123,
                  image_id=dog_image_id))

    db.session.add(Labels(id=str(uuid.uuid1()),
                  label='animal',
                  score=0.123,
                  topicality=0.123,
                  image_id=dog_image_id))

    db.session.add(Labels(id=str(uuid.uuid1()),
                  label='animal',
                  score=0.123,
                  topicality=0.123,
                  image_id=cat_image_id))

    db.session.add(Labels(id=str(uuid.uuid1()),
                  label='cat',
                  score=0.123,
                  topicality=0.123,
                  image_id=cat_image_id))

    db.session.commit()
    images = db.get_images_by_label(labels=['animal'])
    assert(len(images) == 2)

    images = db.get_images_by_label(labels=['dog'])
    assert(len(images) == 1)
    assert(images[0]['id'] == dog_image_id)

    images = db.get_images_by_label(labels=['cat'])
    assert(len(images) == 1)
    assert(images[0]['id'] == cat_image_id)

    images = db.get_images_by_label(labels=['cat', 'dog'])
    assert(len(images) == 2)
    