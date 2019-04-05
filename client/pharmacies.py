from flask import Flask, render_template, request
from pharmacy_class import pharmacy
app = Flask(__name__)

@app.route("/")
def homepage():
	return render_template('pharmacies.html')

@app.route("/getFromDistributer", methods = ['GET', 'POST'])
def getFromDist():
	p = pharmacy()
	dist_name = request.form['distributer']
	pharma_name = request.form['pharmacy']
	date = request.form['date']
	batchid = request.form['batchid']
	action = request.form['choice']
	result = p.getFromDistributor(dist_name, pharma_name, batchid, date, action)
	# return str(request.form)
	return render_template('alert.html', command=result, port="5030")

@app.route('/listMed', methods = ['GET', 'POST'])
def listMed():
    p = pharmacy()
    pharma_name = request.form['pharmacy']
    result = p.listMedicines(pharma_name)
    return render_template('alert.html',command=result, port="5030")

@app.route('/listMedReq', methods = ['GET', 'POST'])
def listMedReq():
    p = pharmacy()
    pharma_name = request.form['pharmacy']
    result = p.listMedicines(pharma_name, 'request')
    return render_template('alert.html',command=result, port="5030")

@app.route('/track', methods = ['GET', 'POST'])
def track():
	p = pharmacy()
	batchid = request.form['batchid']
	result = p.readMedicineBatch(batchid)
	# return str(result)
	i = 0
	args = ['0', '0', '0']
	result = result.split(',')
	# return str(result)
	while result[i] != " +":
		args[i] = result[i]
		i = i + 1
	args.extend(result[i+1:])
	# return str(args)
	return render_template('tracking.html', manufacturer = args[0], distributer = args[1], pharmacy = args[2], medicine = args[3], batchid = args[4], manu_date = args[5], exp_date = args[6])

if __name__=='__main__':
	app.run(debug=True, host="0.0.0.0")
