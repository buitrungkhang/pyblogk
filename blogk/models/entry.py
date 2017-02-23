import datetime
from sqlalchemy import (
    Column,
    Integer,
    UnicodeText,
    Unicode,
    DateTime,
)

from .meta import Base
from webhelpers2.text import urlify
from webhelpers2.date import distance_of_time_in_words

class Entry(Base):
    __tablename__ = 'entry'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    body = Column(UnicodeText, default=u'')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def slug(self):
        return urlify(self.title)

    @property
    def created_in_words(self):
        return distance_of_time_in_words(self.created, datetime.datetime.utcnow())
