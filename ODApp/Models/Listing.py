
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence
from sqlalchemy import Column
from sqlalchemy import Integer, String, Numeric

import json
import decimal

Base = declarative_base()

class Listing(Base):
    __tablename__ = 'listings'
    id = Column(Integer, Sequence('id'), primary_key=True)
    street = Column(String(100), Sequence('street'))
    status = Column(String(100), Sequence('status'))
    price = Column(Numeric(), Sequence('price'))
    bedrooms = Column(Numeric(), Sequence('bedrooms'))
    bathrooms = Column(Numeric(), Sequence('bathrooms'))
    sq_ft = Column(Numeric(), Sequence('sq_ft'))
    lat = Column(Numeric(), Sequence('lat'))
    lng = Column(Numeric(), Sequence('lng'))
