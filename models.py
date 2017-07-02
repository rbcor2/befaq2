#ফলাফল ডাটাবেজে রাখার জন্য ডাটাবেজ মডেল
#ব্যবহার করা হয়েছে সিকুয়েল এলকেমি ও আর এম
#ডাটাবেজ ব্যাকএন্ড হল পোস্টগ্রে সিকুয়েল
#ডাটাবেজে ডাটা লোড করার আগে অবশ্যই এই ফাইল 
#জাস্ট এক্সিকিউট করে মডেল তৈরি করে নিতে হবে।

from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
Base = declarative_base()

class Result(Base):
    """ডাটাবেজ মডেল
    
    তিনটা ফিল্ডঃ
    ১) আইডি,
    ২) রোল ইন্টেজার
    ৩) রেজাল্ট টেক্সট
    """
    __tablename__ = "results" 

    id = Column(Integer, primary_key=True)
    roll = Column(Integer)
    res = Column(Text)
    
    def __init__(self,roll, res):
        self.roll = roll
        self.res = res

#এখান থেকেই সেশন তৈরি হবে এবং
#এটা app.py তে ব্যবহার হবে 
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    

