from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from config.db_config import db

class AnotherTable(db.Model):
    __tablename__ = 'another_table'
    id = Column(Integer, primary_key=True, index=True)
    column1 = Column(String, nullable=False)
    column2 = Column(Integer, nullable=False)