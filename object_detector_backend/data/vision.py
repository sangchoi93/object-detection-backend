from google.cloud import vision

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './metal-circle-337704-f5cefa6e0d43.json'

GOOGLE_VISION_API = 'https://vision.googleapis.com'
ANNOTATE_METHPD = '/v1/images:annotate'

class GoogleVisionAPICaller():
    """Calls Google Vision API to annotate image with labels
    """
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def annotate(self, content) -> list:
        """call Annotate method of the API with images.
        Returns list of labels with score and tropicality ordered by score
        """

        if content is None:
            raise Exception('content of an image cannot be none')

        image = vision.Image(content=content)
        response = self.client.label_detection(image=image)
        labels = response.label_annotations

        to_return = []

        for label in labels:
            to_return.append({
                'label': label.description,
                'score': label.score,
                'topicality': label.topicality
            })

        return to_return

def main():
    vision_caller = GoogleVisionAPICaller()

    with open('./images/whale.jpeg', 'rb') as f:
        resp = vision_caller.annotate(content=f.read())

    print(resp)    


if __name__ == '__main__':
    main()
