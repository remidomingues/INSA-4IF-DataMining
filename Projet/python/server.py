from flask import Flask, render_template, request
import json
import pandas

app = Flask(__name__)
app.debug = True

filepathPoints = "./results/clusters.csv"
filepathClusters = "./results/centers.csv"

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/mapPoint", methods = ['POST','GET'])
def generatePoints():
    if request.method == 'GET':
        points = pandas.read_csv(filepath_or_buffer=filepathPoints)  # Read the file
        table_points = points[['latitude','longitude', 'cluster', 'hashtags']].values.tolist()


        points = pandas.read_csv(filepath_or_buffer=filepathClusters)  # Read the file
        table_clusters = points[['latitude','longitude', 'cluster']].values.tolist()

        result =[ [ [cluster,table_clusters[table_clusters[2] == cluster] ], [l for l in table_points if l[3] == cluster]  ] for cluster in set([ p[3] for p in table_points])]
        return json.dumps(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
