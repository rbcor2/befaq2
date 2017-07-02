#বেফাক এর ওয়েবসাইট থেকে ফলাফল লোড করে নিজস্ব ডাটাবেসে সেভ করার স্ক্রিপ্ট
#models.py এক্সিকিউট করে মডেল তৈরি করার পর নির্দিষ্ট মারহালার ফলাফল লোড 
#করতে এই ফাইল এক্সিকিউট করতে হবে

import requests
import config
from concurrent.futures import ThreadPoolExecutor #মাল্টিথ্রেডিং ব্যবহার করা হয়েছে, রেডিস ব্যবহার করার চিন্তা করছি!

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from helper import beautify
from models import Result

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

executor = ThreadPoolExecutor(1)

result_url = 'http://saharait.com/mark-sheet.php' #বেফাকের সাইট, wifaqbd.org টা ডাউন হয়ে আছে! আবার টেস্ট করতে হবে!
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

payload = {}
payload['years'] = 2017
payload['ClassName'] = 2 #ফযিলত, ১ হল তাকমিল, এটা বর্তমানে শুধু ফযীলতের রেজাল্ট লোড করবে, অন্য জামাতের রেজাল্ট লোড করতে সেই জামাতের নাম্বার দিতে হবে।

def loader(start, stop):
    """ডাটা লোড করার মেইন ফাংশন।
    
    start থেকে stop প্যারামিটারের সকল রোল সেভ করবে (start এবং stop রোল সহ।) এবং লগ ইন্টারেক্টিভ শেলে প্রিন্ট করবে, কোন কারনে ছয়বার এরর হলে বা ডাটা লোড করতে না পারলে
    লুপ থেমে যাবে।
    
    ইনপুটঃ শুরু এবং শেষের রোল নং ইন্টেজার। 
    আউটপুটঃ নান"""
    
    error_count = 0
    for roll in range(start, stop+1):
        if error_count > 5: break
        try:
            payload['Roll'] = roll
            r = requests.post(result_url,payload,headers=headers)
            r.encoding = 'utf-8'
            result = beautify(r)
            
            data_row = Result(roll, result)
            session.add(data_row)
            session.commit()
            print('roll {} added to database'.format(roll))
        except:
            error_count +=1
            print('one error occured')
            continue
    if error_count > 4:
        print( "data loading abort due to 5 error!!")
    else:
        print("Data loaded succesfully")
