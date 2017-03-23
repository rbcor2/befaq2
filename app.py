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
    return jsonify({ "messages": [ {"text": "Welcome to our store!"}, {"text": "How can I help you?"} ] })
