from sqlalchemy import *
from sqlalchemy.orm import *

Base = declarative_base()

# class ItemCreator(Base):
#     __tablename__ = "itemCreators"
#
#     itemID = Column(Integer, primary_key=True)
#     creatorID = Column(Integer)
#     creatorTypeID = Column(Integer)
#     orderIndex = Column(Integer)
item_creator_table = Table(
    "itemCreators",
    Base.metadata,
    Column("itemID", ForeignKey("items.itemID")),
    Column("creatorID", ForeignKey("creators.creatorID")),
)


class Item(Base):
    __tablename__ = "items"

    itemID = Column(Integer, primary_key=True)
    dateAdded = Column(String)
    key = Column(String)

    itemData = relationship("ItemData", viewonly=True)
    creators = relationship("Creator", secondary=item_creator_table, viewonly=True)
    attachments = relationship("ItemAttachment", viewonly=True)
    annotations = relationship("ItemAnnotation", viewonly=True)
    notes = relationship("ItemNote", viewonly=True)
    collections = relationship("CollectionItem", viewonly=True)


class ItemData(Base):
    __tablename__ = "itemData"

    itemID = Column(Integer, ForeignKey('items.itemID'), primary_key=True)
    fieldID = Column(Integer, ForeignKey('fields.fieldID'), primary_key=True)
    valueID = Column(Integer, ForeignKey('itemDataValues.valueID'))

    item = relationship("Item")
    field = relationship("Field")
    value = relationship("ItemDataValue")


class ItemDataValue(Base):
    __tablename__ = "itemDataValues"

    valueID = Column(Integer, primary_key=True)
    value = Column(String)


class Field(Base):
    __tablename__ = "fields"

    fieldID = Column(Integer, primary_key=True)
    fieldName = Column(String)
    fieldFormatID = Column(Integer)


class CollectionItem(Base):
    __tablename__ = "collectionItems"

    collectionID = Column(Integer, primary_key=True)
    itemID = Column(Integer, ForeignKey('items.itemID'), primary_key=True)


class ItemAttachment(Base):
    __tablename__ = "itemAttachments"

    itemID = Column(Integer, ForeignKey('items.itemID'), primary_key=True)
    parentItemID = Column(Integer)


class ItemAnnotation(Base):
    __tablename__ = "itemAnnotations"

    itemID = Column(Integer, ForeignKey('items.itemID'), primary_key=True)
    parentItemID = Column(Integer)


class ItemNote(Base):
    __tablename__ = "itemNotes"

    itemID = Column(Integer, ForeignKey('items.itemID'), primary_key=True)
    parentItemID = Column(Integer)


class Creator(Base):
    __tablename__ = "creators"

    creatorID = Column(Integer, primary_key=True)
    firstName = Column(String)
    lastName = Column(String)
    fieldMode = Column(Integer)
