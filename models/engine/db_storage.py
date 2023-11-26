#!/usr/bin/python3
'''
This module defines the DBStorage class for HBNB project
based on SQL
'''

from sqlalchemy.exc import InvalidRequestError
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

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

class DBStorage:
    ''' Database storage class that manages storage using
    SQLAlchemy ORM '''
    __engine = None
    __session = None

    def __init__(self):
        ''' Initialize DBstorage instance'''
        self.__engine = create_engine(
        f"mysql+mysqldb://{os.getenv('HBNB_MYSQL_USER')}:{os.getenv('HBNB_MYSQL_PWD')}\
        @{os.getenv('HBNB_MYSQL_HOST')}:3306/{os.getenv('HBNB_MYSQL_DB')}",
        pool_pre_ping=True)

        HBNB_ENV = os.getenv('HBNB_ENV', 'development')

        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''
        query on the current database session
        all objects depending of the class name
        '''
        objects = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                query_result = self.__session.query(classes[clss]).all()
                for obj in query_result:
                    key = obj.__class__.__name__ + '.' + obj.id
                    objects[key] = obj
        return (objects)

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

        self.__session = Session

    def close(self):
        '''Close the session.'''
        self.__session.remove()
