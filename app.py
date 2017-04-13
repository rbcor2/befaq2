#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup as bs
from flask import Flask, jsonify

app = Flask(__name__)
url = 'http://www.wifaqbd.org/result/mark-sheet.php'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
marhala_names = {'তাকমীল':'t', 'ফযীলত':'f', 'সানাবিয়া উলইয়া':'s', 'মুতাওয়াসসিতাহ':'m' , 'ইবতিদাইয়্যাহ':'i' , 'হিফযুল কুরআন':'h', 'ইলমুত তাজবীদ ওয়াল কিরাআত':'q'}

#data validation function
def data_validate(data):
    roll, *marhala, year = data.split('+')
    marhala = ' '.join(marhala)
    
    if marhala in marhala_names:
        marhala = marhala_names[marhala] 
    if marhala[0].lower() in 'tfsmihq':
        payload = {}
        try:
            payload['Roll'] = int(roll)
            payload['years'] = int(year)
        except ValueError:
            return False
        payload['ClassName'] = 'tfs_mihq'.index(marhala[0].lower()) + 1
        return payload
    else :
        return False

#grabing result from befaq web
def grab_result(**payload):
    url = 'http://www.wifaqbd.org/result/mark-sheet.php'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    payload = payload
    result = requests.post(url,payload,headers=headers)
    result.encoding = 'utf-8'
    if result.ok:
        return result.content
    else:
        return False
    
#beatify result
def beautify_result(content):
    html = bs(content, 'html.parser')
    e = html.find('div', id = 'printablediv')
    if e.text.strip() == 'দয়া করে সঠিক ভাবে পরীক্ষার সন,তাকমীল, রোল নং পুনরায় সাবমিট করুন':
        return False
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
    
    return { "messages":    [ {"text": "{}\n{}".format(msg[0], msg[1])},
                              {"text": "{}\n{}".format(msg[2], msg[3])},
                              {"text": "{}".format(kitab)},
                              {"text": "{}".format(msg[4])},
                              {"text": "{}\n{}".format(msg[5], msg[6])} ]
      }



@app.route('/')
def hello_world():
    return '<a href="https://www.facebook.com/Befaq-1139031032800784/">    কাজ করছে !!! </a>'

@app.route('/<var>')
def jsonreturn(var):
    try:
        payload = data_validate(var)
        if payload:
            result = grab_result(**payload)
        else:
            return jsonify({"messages": [{"text": "রোল, সন, মারহালার প্রথম অক্ষর ঠিকভাবে লিখে পাঠান! বিস্তারিত জানতে help লিখুন! "}]})
        if result:
            msg = beautify_result(result)
        else:
            return jsonify({"messages": [{"text": "বেফাকের ওয়েবসাইটে কোন সমস্যা হয়েছে, একটু পর আবার চেষ্টা করুন! বেফাকের ওয়েবসাইট ভিজিট করতে www.wifaqbd.org/result/ ঠিকানায় যান"}]})
        if msg:
            return jsonify(msg)
        else:
            return jsonify({"messages": [{"text": "রোল, সন, মারহালার প্রথম অক্ষর ঠিকভাবে লিখে পাঠান! বিস্তারিত জানতে help লিখুন! "}]})
    except:
        return jsonify({"messages": [{"text": "কোন সমস্যা হয়েছে ! " }]})
