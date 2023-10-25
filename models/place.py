#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import ForeignKey, String, Float, Column, Integer, Table
from sqlalchemy.orm import relationship
import models
from models.review import Review
from models.amenity import Amenity
import os


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    reviews = relationship("Review", backref='place',
                           cascade='all, delete, delete-orphan')
    amenities = relationship("Amenity", secondary='place_amenity',
                             viewonly=False)
    if os.getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def reviews(self):
            """Returns list of Review instances with place_id
            equals to self.id(Place instance)"""
            reviewlist = []
            for reviews in models.storage.all(Review).values():
                if self.id == reviews.place_id:
                    reviewlist.append(reviews)
            return reviewlist

        @property
        def amenities(self):
            """Returns the list of Amenity instances related
            to the current Place"""
            amenitieslist = []
            for amenity in models.storage.all(Amenity).values():
                if amenity.id == self.amenity_ids:
                    amenitieslist.append(amenity)
            return amenitieslist

        @amenities.setter
        def amenities(self, value):
            """Setter method for amenities, appends id to amenity_ids if value
            being passed is an Amenity instance"""
            if isinstance(value, Amenity):
                self.amenity_ids.append(value.id)
