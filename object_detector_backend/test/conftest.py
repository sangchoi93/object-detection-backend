import os
import pytest

from object_detector_backend.data.persistence import DatabaseAPI
from object_detector_backend.data.vision import GoogleVisionAPICaller

TEST_DB_PATH = 'test.db'

@pytest.fixture()
def setup_database():
    """create a fresh database for each test
    """
    db = DatabaseAPI(conn_str=f'sqlite:///{TEST_DB_PATH}')

    yield db

    # database teardown
    os.remove(TEST_DB_PATH)

@pytest.fixture
def setup_vision_client():
    """create a vision client for each test
    """
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'metal-circle-337704-f5cefa6e0d43.json'
    if not(os.path.exists(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])):
        raise Exception( \
            'GOOGLE_APPLICATION_CREDENTIALS must be set to a correct' \
            'json filepath in test/test_vision.py')

    vision_caller = GoogleVisionAPICaller()
    return vision_caller


