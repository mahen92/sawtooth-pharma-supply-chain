#!/usr/bin/python3
from flask import Flask, render_template, request
from manufacturer_class import manufacturer
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('distributor.html')

@app.route('/admin')
def hello():
    return render_template('admin.html')


@app.route('/addDistributor', methods = ['GET', 'POST'])
def call():
    m = manufacturer()
    n = request.form['DISTname']
    return m.manufacture(n, 'crocin')