from flask import Flask, render_template,request   
import numpy as np
import pandas
import pickle
import requests

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "gty1PYR_T522sN6_r51HL2g88kxNxhyQXGVp5uPGmGFC"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}







app = Flask(__name__)
model = pickle.load(open(r'rdf.pkl','rb'))
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

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": [names],
                                       "values": [input_feature]}]}

    response_scoring = requests.post(
        'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/a05131f3-dcb8-46cd-bf08-1c2ecf28cc86/predictions?version=2022-11-13',
        json=payload_scoring,
        headers={'Authorization': 'Bearer ' + mltoken})
    predictions = response_scoring.json()
    prediction = predictions['predictions'][0]['values'][0][0]
    print("Scoring response")
    print(response_scoring.json())
    print(prediction)

    # data = pandas.DataFrame(input_feature, columns=names)
    # print(data)
    # prediction=model.predict(data)
    # print(prediction)
    # prediction = int(prediction)
    # print(type(prediction))
    loan=1
    if (prediction == 0):
        loan=0
        return render_template("success.html",result = "Loan will Not be Approved",loan=loan)
    else:
        return render_template("success.html",result = "Loan will be Approved",loan=loan)
    return render_template("success.html")

    
if __name__ == "__main__":
    app.run(debug=True)