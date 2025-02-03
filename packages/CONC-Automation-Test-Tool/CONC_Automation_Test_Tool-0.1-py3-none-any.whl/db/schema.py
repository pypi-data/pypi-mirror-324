from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Test1_conc(Base):
    __tablename__ = 'test1_conc'
    id = Column(Integer, primary_key=True, index=True)
    fname = Column(String)
    lname = Column(String)
    email = Column(String)
    password = Column(String)
    roll_no = Column(String)

