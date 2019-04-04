#!/usr/bin/python3
from flask import Flask, render_template, request
from distributor_class import distributer
app=Flask(__name__)

@app.route("/")
def homepage():
	return render_template('distributor.html')

@app.route('/recieveFromManufacturer', methods = ['POST','GET'])
def recieveFromManufacturer():
    # return "hello"
	# if request.method=='POST':
    d = distributer()
    manu_name = request.form['manufacturer']
    dist_name = request.form['distributer']
    date = request.form['date']
    batchid = request.form['batchid']
    owner = dist_name
    k = d.getFromManufacturer(manu_name, dist_name, batchid, date, owner, "accept")
    if (k == "COMMITTED"):
        return render_template('alert.html',command="SENT THE REQUIRED BATCH SUCCESSFULLY")
    else:
       return render_template('alert.html',command="SOMETHING FAILED! \nOOPS!")

@app.route('/sendToPharmacy', methods=['POST', 'GET'])
def sendToPharmacy():
    d = distributer()
    dist_name = request.form['distributer']
    pharma_name = request.form['pharmacy']
    date = request.form['date']
    batchid = request.form['batchid']
    owner = dist_name
    k = d.giveToPharmacy(dist_name, pharma_name, batchid, date)
    if (k == "COMMITTED"):
        return render_template('alert.html',command="ADDED DISTRIBUTOR")
    else:
       return render_template('alert.html',command="SOMETHING FAILED! \nOOPS!")


@app.route('/listMed', methods = ['GET', 'POST'])
def listMed():
    m = distributer()
    dist_name = request.form['distributor']
    result = m.listMedicines(dist_name)
    return render_template('alert.html',command=result,port="5010")

@app.route('/listMedReq', methods = ['GET', 'POST'])
def listMedReq():
    m = distributer()
    dist_name = request.form['distributor']
    result = m.listMedicines(dist_name, 'request')
    return render_template('alert.html',command=result,port="5010")

if __name__=='__main__':
	app.run(debug=True,host="0.0.0.0")
