import hashlib
import requests
from object_detector_backend.util.exceptions import InvalidInputException


class ImageModel():
    """Image class to hold image metadata and its content
    """
    def __init__(self,
                 id: str,
                 filename:str = None,
                 url: str = None,
                 content = None,
                 filetype:str = None):
        self.id = id
        self.url = url
        self.content = content
        self.filename = filename
        self.filetype = filetype
        self.checksum = None

        if self.url and self.content is None:
            resp = requests.get(self.url, stream=True)
            resp.raise_for_status()
            self.content = resp.content
            self.filename = url.split('/')[-1]

        if self.content is None:
            raise Exception('Image model should have file content')

        self.checksum = hashlib.md5(self.content).hexdigest()

        if not(self.filetype):
            filename_splits = self.filename.split('.')
            if len(filename_splits) > 1:
                self.filetype = filename_splits[-1]


class LabelModel():
    """Label class to hold label name, certainty of the label, and image id the label is related to.
    """
    def __init__(self,
                 id: str,
                 label: str,
                 image_id: str,
                 source: str,
                 score: float = None,
                 topicality: float = None):
        self.id = id
        self.label = label
        self.score = score # the confidence score, which ranges from 0 (no confidence) to 1 (very high confidence).
        self.topicality = topicality #  It measures how important/central a label is to the overall context of a page.
        self.image_id = image_id
        self.source = source
