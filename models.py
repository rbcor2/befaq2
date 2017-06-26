from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///befaq.db')
Base = declarative_base()

class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True)
    roll = Column(Integer)
    res = Column(Text)
    
    def __init__(self,roll, res):
        self.roll = roll
        self.res = res

Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    

