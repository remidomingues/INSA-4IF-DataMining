from flask import Flask, render_template, request
import json
import pandas
import math

app = Flask(__name__)
app.debug = True

filepathPoints = "./results/points.csv"
filepathClusters = "./results/centers.csv"


def max_cluster(list_points, key):
    max_c = 0
    for p in list_points : 
        distance =math.sqrt(math.pow( p[0]-key[0],2) + (math.pow(p[1]- key[1],2) ))
        if distance > max_c :
            max_c = distance
            return p
    return 0


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/mapPoint", methods = ['POST','GET'])
def generatePoints():
    if request.method == 'GET':
        points = pandas.read_csv(filepath_or_buffer=filepathPoints)  # Read the file

        table_points = points[['longitude', 'latitude','hashtags' ,'cluster' ]].values.tolist()


        points = pandas.read_csv(filepath_or_buffer=filepathClusters)  # Read the file
        table_clusters = points[['longitude','latitude', 'cluster']].values.tolist()


        # now creating a list of objects in this form : [cluster_number, center point] , [list of the points contained in this cluster]
        result =[ [ [cluster,table_clusters[(table_clusters[2] == cluster)],[] ], [l for l in table_points if l[3] == cluster]  ] for cluster in set([ p[3] for p in table_points])]
        
        for cluster in result :
            cluster[0][2] = max_cluster(cluster[1],cluster[0][1])

        return json.dumps(result)

        result =[ [ [cluster,table_clusters[table_clusters[2] == cluster] ], [l for l in table_points if l[3] == cluster]  ] for cluster in set([ p[3] for p in table_points])]
        return json.dumps(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
