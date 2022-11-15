from flask import Flask, render_template,request   
import numpy as np
# import pickle
import requests

API_KEY = "q3P7ZbT4fGZALq9E6p2WnN8A673uSOz3MREKcwiy4H_V"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(_name_)

# model = pickle.load(open(r'rdf.pkl','rb'))

@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template("home.html")
    
@app.route("/predict",methods=['POST','GET'])
def predict():
    if request.method == 'POST':
        project_name=request.form['full-name']
        print(project_name)
    return render_template("predict.html",project_name=project_name)

@app.route("/success",methods=['POST','GET'])
def evaluate():
    input_feature = [int(x) for x in request.form.values()]
    print(input_feature)
    # input_feature=[np.array(input_feature)]
    print(input_feature)
    names = ['Gender', 'Married', 'Dependents', 'Education', 'Self Employed', 'Applicant Income', 'Coapplicant Income', 'Loan Amount', 'Loan_Amount_Term', 'Credit_History', 'Property_Area']
    payload_scoring = {"input_data": [{"fields": [names],
                                       "values": [input_feature]}]}
    response_scoring = requests.post(
        'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/cfb7dd73-4afb-4559-b3d2-b5087422dba4/predictions?version=2022-11-15',
        json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
    predictions = response_scoring.json()
    prediction = predictions['predictions'][0]['values'][0][0]
    print("Predictions are ",predictions)
    if (prediction == 0):
        return render_template("success.html",result = "Loan will Not be Approved",loan=0)
    else:
        return render_template("success.html",result = "Loan will be Approved",loan=1)

if _name_ == "_main_":
    app.run(debug=True)