from flask import Flask, render_template, request

app=Flask(__name__)

@app.route("/")
def fun1():
	return render_template('pharmacies.html')


if __name__=='__main__':
	app.run(debug=True, host="0.0.0.0")

	
