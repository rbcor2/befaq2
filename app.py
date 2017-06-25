from flask import Flask, jsonify
app = Flask(__name__)
app.config['SECRETE_KEY'] = 'dfkjdlfk'

from sqlalchemy import create_engine, Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgres://mlxodpnnjrwuok:2b84fe1535ef25d6c561a4982b0128ebe6828c3280d8bf48ab214838f25c9958@ec2-54-228-235-185.eu-west-1.compute.amazonaws.com:5432/dsb4kb4rsfepb')
Base = declarative_base()

class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    roll = Column(Integer, nullable=False)

    def __init__(self, name, roll):
        self.name = name
        self.roll = roll

    def __repr__(self):
        return '<Student name {}, roll {}'.format(self.name, self.roll)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

@app.route('/')
def index():
    return 'alhamdulillah'
@app.route('/show')
def show():
    l = {}
    for student in session.query(Student).all():
        l[student.name] = student.roll
    return jsonify(l)
        
@app.route('/add')
def add():
    import start
    return 'added'
