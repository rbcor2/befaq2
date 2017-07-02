from flask import Flask, jsonify

import config
from models import session, Result

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def index():
    """হোম পেজ ভিউ, বট লাইভ আছে কিনা সেটা বোঝার জন্য"""
    
    return "<center>alhamdulillah... its working!</center>"
    
@app.route('/<int:r>')
def roll(r):
    """ডাটাবেজ থেকে কুয়েরি করে জেসন ফরমেটে নির্দিষ্ট রোল নং এর ফলাফল রিটার্ন করবে
    রেজাল্ট পাওয়া না গেলে result not found রিটার্ন করবে।
    
    ইনপুটঃ রোল ইন্টেজার
    আউটপুটঃ রেজাল্ট জেসন"""
    
    s = session.query(Result).filter_by(roll=r).first()
    if s:
        return jsonify({"messages": [{"text": "{}".format(s.res)}]})
    else:
        return jsonify({"messages": [{"text": "result not found"}]})
    

@app.route('/41033/<int:start>/<int:stop>')
def dataload(start, stop):
    """নির্দিষ্ট মারহালার সকলের ফলাফল নিজস্ব ডাটাবেজে সেভ করে রাখার ফাংশন
    এই ফাংশন একবারই কল করা হবে, শুরু আর শেষের রোল নাম্বার দিয়ে। বার বার কল করলে 
    ডাটাবেজে ডুপ্লিকেট রেজাল্ট সেভ হবে!
    
    ইনপুটঃ শুরু এবং (ইনক্লুডিং) শেষের রোল । ইন্টেজার
    আউটপুটঃ এইচটিএমএল টেমপ্লেট!
    """
    
    import dataloader
    dataloader.executor.submit(dataloader.loader, start, stop) #ফাংশন কল করার পর ব্যকগ্রাউন্ডে ডাটা লোডিং শুরু হবে !
    return """<html><center>data loading started in background...</br>
            with start value = {}</br>
            and stop value = {} </br>
            </br>
            DO NOT HIT THIS URL AGEIN</html></center>""".format(start, stop)

@app.route('/41033/models')
def models():
    """ফলাফল সেভ করার জন্য ডাটাবেজ মডেল তৈরি
    models.py ফাইল এক্সিকিউট হবে
    
    মেনুয়ালি এই ফাইল এক্সিকিউট করতে হেরোকু CLI তে   
    heroku run -a befaq2 python models.py কমান্ড দিতে হবে
    """
    import models
    return 'models created'


#বিভিন্ন ওয়েবসাইট বা সার্ভিস ভেরিফিকেশনের জন্য এখানের
#ভিউ গুলো ব্যবহার হবে
@app.route('/loaderio-503d750ec1cfeee8ab19ce83c39edf32/')
def lodario():
    #লোড টেস্টিং সাইট লোডার আই ও এর ভেরিফিকেশন কি!
    return "loaderio-503d750ec1cfeee8ab19ce83c39edf32"
