import requests

from bs4 import BeautifulSoup as bs

from sqlalchemy import create_engine, Column, Integer, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#engine = create_engine('sqlite:///test.db')
engine = create_engine('postgres://mlxodpnnjrwuok:2b84fe1535ef25d6c561a4982b0128ebe6828c3280d8bf48ab214838f25c9958@ec2-54-228-235-185.eu-west-1.compute.amazonaws.com:5432/dsb4kb4rsfepb')
Base = declarative_base()

class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    name = Column(JSON)
    roll = Column(Integer, nullable=False)

    def __init__(self, name, roll):
        self.name = name
        self.roll = roll

    def __repr__(self):
        return '<Student name {}, roll {}'.format(self.name, self.roll)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

#result_page_url = 'http://www.wifaqbd.org/mark-sheet.php'
result_page_url = 'http://saharait.com/mark-sheet.php'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

error = []

payload = {}

payload['years'] = 2017
payload['ClassName'] = 2


for i in range(1, 9):
    payload['Roll'] = i
    #বেফাকের ওয়েবসাইট থেকে রেজাল্ট গ্রহন করা
    result = requests.post(result_page_url, payload, headers= headers)
    result.encoding = 'utf-8'
    if not result.ok:
        error.append('result not ok')
            

    html = bs(result.content, 'html.parser')
    e = html.find('div', id = 'printablediv')
    if e.text.strip() == 'দয়া করে সঠিক ভাবে পরীক্ষার সন,তাকমীল, রোল নং পুনরায় সাবমিট করুন':
        error.append('দয়া করে সঠিক ভাবে পরীক্ষার সন,তাকমীল, রোল নং পুনরায় সাবমিট করুন')
    elems = html.select('div table tbody tr th[colspan]')
    numbers = html.select('div table tbody tr td[class]')
     
    name = " ".join(elems[1].text.split())
    father =  " ".join(elems[2].text.split())
    madrasa =  " ".join(elems[3].text.split())
    markaj =  " ".join(elems[4].text.split())

    totalnumber = numbers[32].text.strip()
    division = numbers[33].text.strip()
    medha = numbers[36].text.strip()


    kitab_list = [(numbers[i].text.strip(), numbers[i+1].text.strip()) for i in range(1,30,3) if numbers[i].text.strip()]
    kitab = "\n".join([": ".join(kitab_list[i]) for i in range(len(kitab_list))])

    msg = (name,father,madrasa, markaj ,'মোট নাম্বার: {}'.format(totalnumber),'বিভাগ: {}'.format(division),'মেধাস্থান: {}'.format(medha))

    json_result ={ "messages":[ {"text": "{}\n{}".format(msg[0], msg[1])},
                                {"text": "{}\n{}".format(msg[2], msg[3])},
                                {"text": "{}".format(kitab)},
                                {"text": "{}".format(msg[4])},
                                {"text": "{}\n{}".format(msg[5], msg[6])} ]
      }

    user = Student(json_result, 1)
    session.add(user)
    session.commit()
    print(i)


