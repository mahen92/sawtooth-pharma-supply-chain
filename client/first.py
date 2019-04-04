#!/usr/bin/python3
from flask import Flask, render_template, request
from manufacturer_class import manufacturer
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('manufacturer.html')

@app.route('/addMed', methods = ['GET', 'POST'])
def hello():
    m = manufacturer()
    manu_name = request.form['manufacturer']
    med = request.form['medicine']
    
    result = m.manufacture(manu_name, med)
    return render_template('alert.html',command=result,port="5000")

@app.route('/giveToDist', methods = ['GET', 'POST'])
def sendtoDist():
    m = manufacturer()
    manu = request.form['manufacturer']
    dist = request.form['distributor']
    med = request.form['medicine']
    result = m.giveToDistributor(manu, dist, med)
    return render_template('alert.html',command=result,port="5000")

@app.route('/addDistributor', methods = ['GET', 'POST'])
def call():
    m = manufacturer()
    n = request.form['DISTname']
    return m.manufacture(n, 'crocin')