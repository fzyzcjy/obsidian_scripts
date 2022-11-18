from sqlalchemy import *
from sqlalchemy.orm import *

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"

    itemID = Column(Integer, primary_key=True)
    dateAdded = Column(DateTime)
    key = Column(String)


class ItemData(Base):
    __tablename__ = "itemData"

    itemID = Column(Integer, primary_key=True)
    fieldID = Column(Integer)
    valueID = Column(Integer)


class ItemDataValue(Base):
    __tablename__ = "itemDataValues"

    valueID = Column(Integer, primary_key=True)
    value = Column(String)


class Field(Base):
    __tablename__ = "fields"

    fieldID = Column(Integer, primary_key=True)
    fieldName = Column(String)
    fieldFormatID = Column(Integer)


class Creator(Base):
    __tablename__ = "creators"

    creatorID = Column(Integer, primary_key=True)
    firstName = Column(String)
    lastName = Column(String)
    fieldMode = Column(Integer)


class ItemCreator(Base):
    __tablename__ = "itemCreators"

    itemID = Column(Integer, primary_key=True)
    creatorID = Column(Integer)
    creatorTypeID = Column(Integer)
    orderIndex = Column(Integer)
