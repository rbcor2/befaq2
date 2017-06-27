import requests
from helper import beautify
from models import session, Result

result_url = 'http://saharait.com/mark-sheet.php'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

start = 452
stop = 9021

payload = {}
payload['years'] = 2017
payload['ClassName'] = 2

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
        print('roll {} commited'.format(roll))
    except:
        error_count +=1
        continue

print('data loading complete' if not error_count else str(error_count))
