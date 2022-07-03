# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 12:25:19 2022

@author: Padmakar
"""
# import necessary libraries
from flask import Flask, render_template, request
import joblib

# initialize the app
app = Flask(__name__)

# load the model
model = joblib.load("model.pkl")

# welcome page with the form loaded
@app.route('/')
def welcome():
    return render_template("index.html")

    
# Submit the details
@app.route('/submit',methods= ["POST", "GET"])
def submit():    
    # initialize the variables
    cluster_desc=""
    target = ""
    annual_income=30
    spending_score=50
    
    if request.method == "POST":
        annual_income = float(request.form["annual_income"])
        spending_score = float(request.form["spending_score"])
        
    # after receiving the input find the cluster
    cluster = find_cluster(annual_income, spending_score)
    
    # find the description of the cluster and corresponding targetted marketing campaigne         
    cluster_desc, target = info_customer_segment(cluster)
    
    # show the result by showing the result.html page     
    return render_template("result.html", income=annual_income, score=spending_score,
                           cluster_description=cluster_desc, target_for=target)    
    

# find the cluster by taking the inputs and using model predicition to get cluster number
def find_cluster(annual_income, spending_score):
    # input is required to by numpy array
    cluster = model.predict([[annual_income, spending_score]])
    
    # result is an array so choose the zeroth element
    return cluster[0]
    
# function to add information regarding the customer segment
def info_customer_segment(cluster):
    cluster_desc = ""
    target = ""
        
    # Below description is based on the values seen in jupyter notebook     
    if cluster == 0:
        target = "both clearence sale and seasonal sales on medium price range items"
        cluster_desc = "Mid Income Casual Shoppers"
    elif cluster == 1:
        target = "expensive items or limited collections as they are likely to make one time purchases"
        cluster_desc = "High Income NonFrequent Shoppers"
    elif cluster == 2:
        target = "expensive items without any discount"
        cluster_desc = "High Income Frequent Shoppers"
    elif cluster == 3:
        target = "seasonal sale discount on cheaper items"
        cluster_desc = "Low Income NonFrequent Shoppers"
    else:
        target= "clearence sale discount on cheaper items at any time"
        cluster_desc = "Low Income Frequent Shoppers"
    
    return cluster_desc, target

    
if __name__ == "__main__":
    app.run(debug=False)