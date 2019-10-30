from flask import Flask, make_response, request
#from flask_jsonpify import jsonpify
import requests
from difflib import SequenceMatcher
import time
import pandas as pd
userLoggedInName='hi'
URL='https://trixcidemo.azurewebsites.net/TriXci'

app = Flask(__name__)

def result1(dataframe):
    dataframe["response"]="A"
    dataframe["similarity"]=0
    
    for i in range(0,dataframe.shape[0]):
        question=dataframe.iloc[i,0]
        PARAMS = {'userLoggedInName':userLoggedInName,'question':question} 
        r = requests.post(url = URL, data =PARAMS)
        data = r.text
        data1=data.split("Display")[1]
        data1=data1.replace(':','')
        data1=data1.replace('"}','')
        data1=data1.replace('"','')
        data1=data1.strip()
        print(data1)
        dataframe.iloc[i,2]=data1
        s = SequenceMatcher(None, dataframe.iloc[i,1], data1)
        dataframe.iloc[i,3]=s.ratio()
        print(dataframe)
        time.sleep(1)
    return dataframe
	

@app.route('/')
def form():
    return """
        <html>
            <body>
                <h1>Get response from POST method</h1>

                <form action="/result1" method="post" enctype="multipart/form-data">
                    <input type="file" name="data_file" />
                    <input type="submit" />
                </form>
            </body>
        </html>
    """

@app.route('/result1', methods=["POST"])
def transform_view():
    request_file = request.files['data_file']
    if not request_file:
        return "No file"

    #file_contents = request_file.stream.read().decode("utf-8")
    file_contents =pd.read_csv(request_file.stream,sep=",")
    file_contents=file_contents.dropna()
    print(type(file_contents))
    print(file_contents.shape)
    
    
    file_contents = result1(dataframe=file_contents)
    file_contents = file_contents.to_csv()   
    result = file_contents
    response = make_response(result)
    response.headers["Content-Disposition"] = "attachment; filename=result.csv"
    return response
	

app.run(host="192.168.2.103",port=5151,debug=True)
	