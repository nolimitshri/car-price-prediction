from flask import Flask, render_template, request
import pickle
import jsonify
import requests
import numpy as np
import sklearn
from datetime import date

app = Flask(__name__)

model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

@app.route('/', methods=['GET'])
def Home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    today = date.today()
    if request.method == "POST":
        Duration = int(today.year) - int(request.form['year'])
        Present_Price = float(request.form['present_price'])
        Kms_Driven = int(request.form['kms_driven'])
        Owner = int(request.form['ownership'])
        Fuel_Type_Petrol = 0
        Fuel_Type_Diesel = 0
        if(request.form['fuel_type'] == "Petrol"):
            Fuel_Type_Petrol = 1
        elif(request.form['fuel_type'] == "Diesel"):
            Fuel_Type_Diesel = 1
        # else:
        #     fuel_petrol = 0
        #     fuel_diesel = 0 
        Seller_Type_Individual = 0
        if(request.form['seller_type'] == "Individual"):
            Seller_Type_Individual = 1

        Transmission_Manual = 0
        if(request.form['transmission_type'] == "Automatic"):
            Transmission_Manual = 0
        else: 
            Transmission_Manual = 1

        important = {
            "Purchased Year": int(request.form['year']),
            "Present Price": f"₹ {float(request.form['present_price'])} Lacs",
            "KMs Driven": f"{Kms_Driven} KM",
            "Ownership": Owner,
            "Fuel Type": request.form['fuel_type'],
            "Seller Information": request.form['seller_type'],
            "Transmission Type": request.form['transmission_type']
        }

        prediction = model.predict([[Duration, Present_Price, Kms_Driven, Owner, Fuel_Type_Diesel, Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual]])
        output = round(prediction[0], 2)

        if(output < 0):
            return render_template('prediction.html', predicted="Sorry you cannot sell this car !!", table_content=important)
        else:
            return render_template('prediction.html', predicted=f"You can sell this car @ ₹{output} Lacs", table_content=important)

    else:
        return render_template('index.html')      

if __name__ == "__main__":
    app.run(debug=True)