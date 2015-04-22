__author__ = 'David'


from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Status(Base):
    __tablename__ = 'status'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    status_original = Column(String(280))
    status_stemmed = Column(String(280))
    status_no_common = Column(String(280))
    rank = Column(Integer, nullable=False)


engine = create_engine('sqlite:///statuses.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)