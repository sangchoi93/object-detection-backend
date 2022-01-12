import os
from typing import List
import logging

from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, LargeBinary, Float, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import LargeBinary

from object_detector_backend.data.models import ImageModel
from object_detector_backend.data.models import LabelModel


Base = declarative_base()

class Labels(Base):
    """Labels mapping for each image
    """
    __tablename__ = 'labels'
    id = Column(String, primary_key=True)
    label = Column(String)
    score = Column(Float) # order by certainty when fetching images
    topicality = Column(Float) # order by certainty when fetching images
    image_id = Column(String, ForeignKey('images.id'))
    source = Column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'score': self.score,
            'topicality': self.topicality,
            'image_id': self.image_id,
            'source': self.source
        }

    def __repr__(self):
        return ("<Label("
                "id='%s', "
                "label='%s', "
                "score='%s', "
                "topicality='%s', "
                "image_id='%s', "
                "source='%s"
                % (self.id,
                   self.label,
                   self.score,
                   self.topicality,
                   self.image_id,
                   self.source))


class Images(Base):
    """Images Table
    """
    __tablename__ = 'images'
    id = Column(String, primary_key=True)
    filename = Column(String)
    filetype = Column(String)
    url = Column(String, nullable=True)
    content = Column(LargeBinary)
    checksum = Column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'filetype': self.filetype,
            'url': self.url,
            'check_sum': self.checksum
        }

    def __repr__(self):
        return ("<Image("
                "id='%s', "
                "filename='%s', "
                "filetype='%s', "
                "url='%s', "
                % (self.id,
                   self.filename,
                   self.filetype,
                   self.url,
                   self.check_sum))


class DatabaseAPI:
    """Creates interface with sqlite database to retrieve and store images metadata
    """
    def __init__(self, conn_str: str = 'sqlite:///images.db'):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.engine = create_engine(conn_str)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # set up tables
        Base.metadata.create_all(self.engine)


    def get_images_by_label(self, labels: list) -> List[dict]:
        """Retrieves list of images based on label name
        """
        
        # make label query case insensitive
        labels = self.session.query(Labels) \
            .filter( \
                func.upper( Labels.label ) \
                .in_([l.upper() for l in labels])
            ).all()
        self.logger.info(f'labels: {labels}')

        # get image id's for all found labels
        image_ids = [l.image_id for l in labels]
        images = self.session.query(Images).filter(Images.id.in_(image_ids)).all()

        to_return = []
        for image in images:
            to_return.append(image.to_dict())

        return to_return


    def get_images(self, **kwargs) -> List[dict]:
        """Retrieves list of images based on criteria
        """
        images = self._query(table_class=Images, **kwargs)
        to_return = []

        for image in images:
            d = image.to_dict()
            d['label'] = [
                label.to_dict() for label in \
                    self._query(table_class=Labels, image_id=image.id)]
            to_return.append(d)

        return to_return


    def get_labels_by_image_id(self, image_id: str) -> List[Labels]:
        return [label.to_dict() for label in \
            self._query(Labels, image_id=image_id)]


    def add_label(self, label: LabelModel) -> dict:
        """Stores image metadata in Images table
        """

        duplicates = self._query(Labels,
                                 label=label.label,
                                 image_id=label.image_id,
                                 source=label.source)

        # if no duplicate is found then create a label in db
        if not(duplicates):
            label = Labels(
                id=label.id,
                label=label.label,
                score=label.score,
                topicality=label.topicality,
                image_id=label.image_id,
                source=label.source,
            )
            self.session.add(label)
            self.session.commit()
            return label.to_dict()

        return duplicates[0].to_dict()


    def check_duplicate_image(self, image: ImageModel) -> dict:
        images = self._query(Images, checksum=image.checksum, filename=image.filename)

        if images:
            return images[0].to_dict()
        
        return {}


    def add_image(self, image: ImageModel) -> dict:
        """Stores image metadata in Images table
        """

        image = Images(
            id=image.id,
            filename=image.filename,
            filetype=image.filetype,
            url=image.url,
            content=image.content,
            checksum=image.checksum,
        )

        duplicate = self.check_duplicate_image(image)
        if not(duplicate):
            self.session.add(image)
            self.session.commit()
            return image.to_dict()
        else:
            return duplicate


    def fetch_image_content_by_id(self, id):
        return self._query(Images, id=id)[0].content


    def _query_by_id(self, table_class: Base, id: list):
        q = self.session.query(table_class).filter(table_class.id.in_(id))
        return q.all()


    def _query(self, table_class: Base, **kwargs):
        q = self.session.query(table_class).filter_by(**kwargs)
        return q.all()


    def reset(self):
        os.remove('images.db')
        Base.metadata.create_all(self.engine)


def main():
    db = DatabaseAPI()
    image_to_add = ImageModel(
        id='1234567',
        filename='test',
        url='hello',
        content=b'101'
    )

    db.add_label(image_to_add)
    # db.add_image(image_to_add)
    # images = db.get_images()
    # print(db._query(id='1', table_class = Images))
    # print(type(db.get_images()[2]))
    # db.reset()

if __name__ == '__main__':
    main()
