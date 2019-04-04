from flask import Flask, render_template, request
from pharmacy_class import pharmacy
app = Flask(__name__)

@app.route("/")
def homepage():
	return render_template('pharmacies.html')

@app.route("/getFromDistributer")
def getFromDist():
	p = pharmacy()
	dist_name = request.form['distributer']
	pharma_name = request.form['pharmacy']
	date = request.form['date']
	batchid = request.form['batchid']
	result = p.getFromDistributor(dist_name, pharma_name, batchid, date, "accept")
	return render_template('alert.html', command=result, port="5000")

if __name__=='__main__':
	app.run(debug=True, host="0.0.0.0")

	
