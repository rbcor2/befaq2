import requests
from concurrent.futures import ThreadPoolExecutor

from helper import beautify
from models import session, Result

executor = ThreadPoolExecutor(1)

result_url = 'http://saharait.com/mark-sheet.php'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

payload = {}
payload['years'] = 2017
payload['ClassName'] = 2

def loader(start, stop):
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
