#python3

import requests
from bs4 import BeautifulSoup as bs
from flask import Flask, jsonify

app = Flask(__name__)
url = 'http://www.wifaqbd.org/result/mark-sheet.php'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

@app.route('/')
def hello_world():
    return '<a href="https://www.facebook.com/Befaq-1139031032800784/">কাজ করছে !!! </a>'

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

        totalnumber = numbers[32].text.strip()
        division = numbers[33].text.strip()
        medha = numbers[36].text.strip()

        name = " ".join(elems[1].text.split())
        father =  " ".join(elems[2].text.split())
        madrasa =  " ".join(elems[3].text.split())
        markaj =  " ".join(elems[4].text.split())
        
        t = []
        n = 2
        for i in range(10):
            t.append(numbers[n].text.strip())
            n+=3
        kitab = "বুখারি ১মঃ {}\nমুসলিম ১মঃ {} \nতিরমিযী ১মঃ {} \nআবু দাউদঃ {} \nবুখারী ২য়ঃ {} \nমুসলিম ২য়ঃ {} \nতিরমিযী ২য়ঃ {} \nনাসাঈ ও ইবনু মাজাহঃ {} \nত্বহাবীঃ {} \nমুআত্তানঃ {}".format(t[0],t[1],t[2],t[3],t[4],t[5],t[6],t[7],t[8],t[9])
        msg = (name,father,madrasa,markaj,'মোট নাম্বার: {}'.format(totalnumber),'বিভাগ: {}'.format(division),'মেধাস্থান: {}'.format(medha))
        return jsonify({ "messages": [ {"text": "{}\n{}".format(msg[0], msg[1])},
                              {"text": "{}\n{}".format(msg[2], msg[3])},
                              {"text": "{}".format(kitab)},
                              {"text": "{}".format(msg[4])},
                              {"text": "{}\n{}".format(msg[5], msg[6])} ] 
                       })
    
    except:
        return jsonify({ "messages": [ {"text": "কোন সমস্যা হয়েছে মনে হয় :( \nআবার চেষ্টা করুন !"} ]})

