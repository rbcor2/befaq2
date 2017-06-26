from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgres://mlxodpnnjrwuok:2b84fe1535ef25d6c561a4982b0128ebe6828c3280d8bf48ab214838f25c9958@ec2-54-228-235-185.eu-west-1.compute.amazonaws.com:5432/dsb4kb4rsfepb')
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
    

