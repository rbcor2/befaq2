#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup as bs
from flask import Flask, jsonify

app = Flask(__name__)
result_page_url = 'http://www.wifaqbd.org/mark-sheet.php'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
marhala_names_first_letter = {'তাকমীল':'t', 'ফযীলত':'f', 'সানাবিয়া উলইয়া':'s', 'মুতাওয়াসসিতাহ':'m' , 'ইবতিদাইয়্যাহ':'i' , 'হিফযুল কুরআন':'h', 'ইলমুত তাজবীদ':'q'}


@app.route('/<data>')
def return_result(data):
    ''' মেসেঞ্জার থেকে যে মেসেজ আসবে সেটা যাচাই করে বেফাকের ওয়েবসাইট থেকে ফলাফল গ্রহন করা হবে
        তারপর ফলাফল মেসেজ হিসেবে রিটার্ন করা হবে।
        কোন সমস্যা হলে এরর মেসেজ রিটার্ন করা হবে।
    '''
    
    #ম্যাসেজ যাচাই করা...
    try:
        #মারহালা বাংলা বা ইংরেজি দুই ফরমেটেই হতে পারে! যেই মারহালার নাম দুই শব্দ দ্বারা সেগুলো + চিহ্নর মাধ্যমে স্প্লিট হয়েছে 
        roll, *marhala, year = data.split('+')
        #দুই শব্দের মারহালাগুলো স্পেস দ্বারা এক করা হয়েছে
        marhala = ' '.join(marhala)
        
        #রেজাল্ট গ্রহন করতে মারহালার ইংরেজি প্রথম অক্ষর ব্যবহার করব  
        #তাই মারহালার নাম বাংলায় হলে সেটাকে ইংরেজি নামের প্রথম অক্ষরে কনভার্ট করতে হবে
        if marhala in marhala_names_first_letter:
            marhala = marhala_names_first_letter[marhala]
            
        #রোল মারহালা এবং সন যাচাই করা
        #প্রথমে রোল যাচাই করা
        try:
            roll = int(roll)
        except ValueError:
            return jsonify({"messages": [{"text": "রোল নং ঠিক ভাবে লিখুন যেমন  3915"}]})
        #মারহালা যাচাই করা
        if marhala[0].lower() in 'tfsmihq':
            pass
        else:
            return jsonify({"messages": [{"text": "মারহালার প্রথম অক্ষর ইংরেজিতে লিখুন যেমন t (তাকমিলের জন্য), f (ফযিলতের জন্য)"}]})
        #সন যাচাই করা
        try:
            year = int(year)
            if year not in [2012,2013,2014,2015,2016]:
                return jsonify({"messages": [{"text": "সন 2012 থেকে 2016 এর মধ্যে হতে হবে "}]})
        except ValueError:
            return jsonify({"messages": [{"text": "সন সঠিক ভাবে লিখুন যেমন 2016"}]})
        
        #পেলোড তৈরি করা যা দ্বারা বেফাকের ওয়েবসাইট থেকে রেজাল্ট আনা হবে
        payload = {}
        payload['Roll'] = roll
        payload['years'] = year
        payload['ClassName'] = 'tfs_mihq'.index(marhala[0].lower()) + 1 #মাঝখানে একটা _ দেয়ার কারন হল বেফাকের ওয়েবসাইটে মারহালার লিস্টে ভুলে একটা সংখ্যা  ()4  বাদ গিয়েছে
        
    except:
        return jsonify({"messages": [{"text": "দয়া করে রোল, মারহালা, সন সঠিক ভাবে লিখুন "}]})
        
    
    #বেফাকের ওয়েবসাইট থেকে রেজাল্ট গ্রহন করা
    try:
        result = requests.post(result_page_url, payload, headers= headers)
        result.encoding = 'utf-8'
        if not result.ok:
            return jsonify({"messages": [{"text": "বেফাকের ওয়েবসাইটে কোন সমস্যা হয়েছে"}]})
    except:
        return jsonify({"messages": [{"text": "বেফাকের ওয়েবসাইটে কোন সমস্যা হয়েছে"}]})
        
    #লোডকৃত রেজাল্ট সঠিক ফরম্যাটে সাজানো
    #বেফাকের পক্ষ থেকে রেজাল্ট জানার কোন এপিআই নেই তাই তাদের ওয়েবসাইট থেকে সব কনটেন্ট লোড করে সেটা থেকে
    #মূল রেজাল্ট তুলে আনা একটু জটিল, এর কোডগুলোও তাই একটু জটিল হয় গিয়েছে :/ 
    try:
        html = bs(result.content, 'html.parser')
        e = html.find('div', id = 'printablediv')
        if e.text.strip() == 'দয়া করে সঠিক ভাবে পরীক্ষার সন,তাকমীল, রোল নং পুনরায় সাবমিট করুন':
            return jsonify({"messages": [{"text": "দয়া করে সঠিক ভাবে পরীক্ষার সন,তাকমীল, রোল নং পুনরায় সাবমিট করুন"}]})
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
        
        return jsonify(json_result)
    except:
        return jsonify({"messages": [{"text": "বেফাকের ওয়েবসাইটে কোন সমস্যা হয়েছে, একটু পর আবার চেষ্টা করুন! বেফাকের ওয়েবসাইট ভিজিট করতে www.wifaqbd.org/result/ ঠিকানায় যান"}]})
        
        
        
@app.route('/')
def hello_world():
    return '<center><a href="https://www.facebook.com/Befaq-1139031032800784/">কাজ করছে !!! </a></center>'
