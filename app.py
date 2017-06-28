from flask import Flask, jsonify

import config
from models import session, Result

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def index():
    return "<center>alhamdulillah... its working!</center>"
    
@app.route('/<int:r>')
def roll(r):
    s = session.query(Result).filter_by(roll=r).first()
    if s:
        return jsonify({"messages": [{"text": "{}".format(s.res)}]})
    else:
        return jsonify({"messages": [{"text": "result not found"}]})
    
@app.route('/<int:exec_len>/<int:start>/<int:stop>')
def dataload(exec_len, start, stop):
    import dataloader
    
    s = start
    val = stop-start
    chunk = val//exec_len
    
    for i in range(exec_len-1):
        dataloader.executor.submit(dataloader.loader, start, start+chunk)
        start+=chunk
    dataloader.executor.submit(dataloader.loader, start, stop+1)
    
    return """<html><center>data loading started in background...</br>
            with start value = {}</br>
            and stop value = {} </br>
            and executor = {} </br>
            </br>
            DO NOT HIT THIS URL AGEIN</html></center>""".format(s, stop, exec_len)


@app.route('/loaderio-503d750ec1cfeee8ab19ce83c39edf32/')
def lodario():
    return "loaderio-503d750ec1cfeee8ab19ce83c39edf32"
           
