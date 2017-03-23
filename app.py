#python3

import requests
from bs4 import BeautifulSoup as bs
from flask import Flask, jsonify

app = Flask(__name__)
url = 'http://www.wifaqbd.org/result/mark-sheet.php'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

@app.route('/')
def hello_world():
    return 'working !'

@app.route('/<var>')
def jsonreturn(var):
    payload = {'years':'2016',
           'ClassName':1,
           'Roll':var}
    try:
        r = requests.post(url,payload,headers=headers)
        r.encoding = 'utf-8'
        html = bs(r.content,'html.parser')
        elems = html.select('div table tbody tr th[colspan]')
        numbers = html.select('div table tbody tr td[class]')

        totalnumber = numbers[32].text.split()[0]
        division = numbers[33].text.split()[0]
        medha = numbers[36].text.split()[0]

        name = " ".join(elems[1].text.split())
        father =  " ".join(elems[2].text.split())
        madrasa =  " ".join(elems[3].text.split())
        msg = (name,father,madrasa,'মোট নাম্বার: {}'.format(totalnumber),'বিভাগ: {}'.format(division),'মেধাস্থান: {}'.format(medha))
    except:
        msg = "কোন সমস্যা হইসে মনে হয় :/ "
    return jsonify({ "messages": [ {"text": "Welcome to our store!"}, {"text": "How can I help you?"} ] })
