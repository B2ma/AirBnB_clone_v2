#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.city import City
import models
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = name = Column(String(128), nullable=False)
    cities = relationship("City", back_populates="state",
            cascade="all, delete-orphan", passive_deletes=True)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship("City", backref="state", cascade='delete')
    else:
        @property
        def cities(self):
            """ Getter attribute to return the list of City instances 
            with state_id equals to the current State.id It will be 
            the FileStorage relationship between State and City"""
            cities_list = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list   
