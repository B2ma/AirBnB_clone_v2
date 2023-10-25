#!/usr/bin/python3
'''
This module defines the DBStorage class for HBNB project
based on SQL
'''

import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import os


class DBStorage:
    ''' Database storage class that manages storage using
    SQLAlchemy ORM '''
    __engine = None
    __session = None

    def __init__(self):
        ''' Initialize DBstorage instance'''
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'.
                                      format(os.getenv('HBNB_MYSQL_USER'),
                                             os.getenv('HBNB_MYSQL_PWD'),
                                             os.getenv('HBNB_MYSQL_HOST'),
                                             os.getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
        query on the current database session
        all objects depending of the class name
        '''
        objects = {}
        classes = [User, State, City, Amenity, Place, Review]

        if cls:
            classes = [cls]

        for class_obj in classes:
            query_result = self.__session.query(class_obj).all()
            for obj in query_result:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                objects[key] = obj

        return objects

    def new(self, obj):
        ''' Adds the object to the current database session '''
        self.__session.add(obj)

    def delete(self, obj=None):
        ''' Deletes from the current database session obj if not None '''
        if obj is not None:
            self.__session.delete(obj)

    def save(self):
        '''  Commits all changes of the current database session '''
        self.__session.commit()

    def reload(self):
        ''' Create all tables in the database and create a session '''
        Base.metadata.create_all(self.__engine)
        new_session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(new_session)

        self.__session = Session()

    def close(self):
        '''Close the session.'''
        if self.__session is not None:
            self.__session.close()
