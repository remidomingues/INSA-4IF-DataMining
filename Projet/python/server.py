from flask import Flask, render_template, request
import json
import pandas

app = Flask(__name__)
app.debug = True

filepath = "../result.csv"

@app.route("/")
def index():
	return render_template('index.html')

@app.route("/mapPoint", methods = ['POST','GET'])
def generatePoints():
	if request.method == 'GET':
	    df = pandas.read_csv(filepath_or_buffer=filepath)  # Read the file
    	result = df[['latitude','longitude', 'cluster']].values
    	return json.dumps(result.tolist())


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
 