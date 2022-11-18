import flask
from flask import request, render_template
from flask_cors import CORS
import joblib

import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "XW9EUMQ8JCF0sDp-JTd4gugsD_CHji5XdLtln4_3VIQU"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = flask.Flask(__name__,static_url_path="")
CORS(app)

@app.route('/',methods=['GET'])
def sendHomePage():
    return render_template('page1.html')

@app.route('/page2',methods=['GET'])
def getinfo():
    return render_template('page2.html')

@app.route('/page3',methods=['POST'])
def predictckd():
    age = float(request.form['age'])

    bp = float(request.form['bp'])
    
    sg = float(request.form['sg'])
    
    al = float(request.form['al'])
    
    su = float(request.form['su'])
    temp_rbc = request.form['rbc']
    if(temp_rbc=="abnormal") :
        rbc = float(0)
    else :
        rbc = float(1)
    
    temp_pc = request.form['pc']
    if(temp_rbc=="abnormal") :
        pc = float(0)
    else :
        pc= float(1)
    
    temp_pcc = request.form['pcc']
    if(temp_pc=="present") :
        pcc = float(1)
    else :
        pcc= float(0)
    
    temp_ba = request.form['ba']
    if(temp_ba=="present") :
        ba = float(1)
    else :
        ba= float(0)
    bgr = float(request.form['bgr'])
    
    bt = float(request.form['bt'])
    
    sub = float(request.form['sub'])
    
    seg = float(request.form['seg'])
    
    pot = float(request.form['pot'])
    
    hemo = float(request.form['hemo'])
    
    pcv = float(request.form['pcv'])
    
    wc = float(request.form['wc'])
    
    rc = float(request.form['rc'])
    
    temp_htn = request.form['htn']
    if(temp_htn=="no"):
        htn = float(0)
    else:
        htn = float(1)
    
    temp_dm = request.form['dm']
    if(temp_dm=="no"):
        dm = float(0)
    else:
        dm = float(1)
    
    temp_cad = request.form['cad']
    if(temp_cad=="no"):
        cad = float(0)
    else:
        cad = float(1)
    
    temp_appet = request.form['appet']
    if(temp_appet=="good"):
        appet = float(0)
    else:
        appet = float(1)
    
    temp_pe = request.form['pe']
    if(temp_pe == "no"):
        pe = float(0)
    else:
        pe = float(1)
    
    temp_ane = request.form['ane']
    if(temp_ane=="no"):
        ane = float(0)
    else:
        ane = float(1)
    
    X = [[age,bp,sg,al,su,rbc,pc,pcc,ba,bgr,bt,sub,seg,pot,hemo,pcv,wc,rc,htn,dm,cad,appet,pe,ane]]
    
    payload_scoring = {"input_data": [{"field": [['age','bp','sg','al','su','rbc','pc','pcc','ba','bgr','bt','sub','seg','pot','hemo','pcv','wc','rc','htn','dm','cad','appet','pe','ane']], "values": X }]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/5789b09f-e0df-4da1-a2fc-0130a2ce175d/predictions?version=2022-11-18', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print(response_scoring)
    predictions = response_scoring.json()
    predict = predictions['predictions'][0]['values'][0][0]
    print('FINAL PREDICTION : ',predict)
    
    if(predict==0):
        v1 = "ONCE YOU CHOOSE HOPE, ANYTHING IS POSSIBLE."
        v2 = "GET WELL SOON "
        v3 = "POSITIVE"
        v4 = "/styles/BG.jpeg"
    else:
        v1 = "THE GREATEST HEALTH IS WEALTH"
        v2 = "STAY HEALTHY "
        v3 = "NEGATIVE"
        v4 = "/styles/emojis.gif"
    return render_template('page3.html',v1=v1,v2=v2,v3=v3,v4=v4)


if __name__ =='__main__':
    app.run()


