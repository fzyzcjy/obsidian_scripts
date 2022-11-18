from sqlalchemy import *
from sqlalchemy.orm import *

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"

    itemID = Column(Integer, primary_key=True)
    dateAdded = Column(DateTime)
    key = Column(String)
