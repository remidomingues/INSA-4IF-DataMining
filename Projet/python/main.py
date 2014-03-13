import parser
import plot
from pandas import *
from numpy import array

from sklearn.cluster import MeanShift, estimate_bandwidth

import numpy as np
import pylab as pl
from itertools import cycle

def import_data(filepath):
    print 'Importing data from {}...'.format(filepath)
    df = pandas.read_csv(filepath_or_buffer=filepath)  # Read the file
    print df.count()
    df.drop_duplicates()
    print df.count()
    return df

# Compute clustering with MeanShift
def run_meanshift(data):
    print 'Clustering data (Meanshift algorithm)...'
    bandwidth = estimate_bandwidth(data, quantile=0.002, n_samples=1000)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, min_bin_freq=30, cluster_all=False)
    ms.fit(data)
    return ms

def plot_meanshift(ms_data, cluster_centers, n_centers_):
    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    pl.figure(1)
    pl.clf()

    for k, col in zip(cluster_centers['cluster'], colors):
        cluster_points = ms_data[(ms_data['cluster'] == k)]

        cluster_longitudes = cluster_points['longitude']
        cluster_latitudes = cluster_points['latitude']

        cluster_center = cluster_centers[(cluster_centers['cluster'] == k)]

        pl.plot(cluster_longitudes, cluster_latitudes, col + '.')
        pl.plot(cluster_center['longitude'], cluster_center['latitude'], 'o', markerfacecolor=col,
            markeredgecolor='k', markersize=14)

    pl.title('POI clustering (%d estimated clusters)' % n_centers_)
    pl.show()

def export_data(ms_data, clusters_file, cluster_centers, centers_file):
    print 'Exporting clusters to {}...'.format(clusters_file)
    ms_data.to_csv(path_or_buf=clusters_file, cols=['longitude', 'latitude', 'hashtags', 'cluster'], encoding='utf-8')
    print 'Exporting clusters centers to {}...'.format(centers_file)
    cluster_centers.to_csv(path_or_buf=centers_file, cols=['longitude', 'latitude', 'cluster'], encoding='utf-8')

if __name__ == "__main__":
    ms_data = import_data("data/data.csv")
    ms_values = ms_data[['longitude', 'latitude']].values

    meanshift = run_meanshift(data=ms_values)
    ms_data['cluster'] = meanshift.labels_

    #Filtering data
    ms_data = ms_data[(ms_data['longitude'] < 4.908976) & (ms_data['longitude'] > 4.802508)
        & (ms_data['latitude'] < 45.793688) & (ms_data['latitude'] > 45.715569)]

    ms_data = ms_data.sort(columns='cluster')

    # Removing points which belong to no cluster
    ms_data = ms_data[(ms_data['cluster'] != -1)]

    labels_unique = np.unique(meanshift.labels_).tolist()
    del labels_unique[0]

    #Filetering clusters centers according to data filter
    cluster_centers = DataFrame(meanshift.cluster_centers_, columns=['longitude', 'latitude'])
    cluster_centers['cluster'] = labels_unique
    cluster_centers = cluster_centers[(cluster_centers['longitude'] < 4.908976) & (cluster_centers['longitude'] > 4.802508)
        & (cluster_centers['latitude'] < 45.793688) & (cluster_centers['latitude'] > 45.715569)] #793688
    n_centers_ = len(cluster_centers)

    # Removing clusters which contain less than x pointsnext(df.iterrows())[1]
    for k in range(n_centers_):
        try:
            cluster_points = ms_data[(ms_data['cluster'] == k)]
            if len(cluster_points) < 30:
                ms_data = ms_data[(ms_data['cluster'] != k)]
                cluster_centers = cluster_centers[(cluster_centers['cluster'] != k)]
        except:
            cluster_centers = cluster_centers[(cluster_centers['cluster'] != k)]

    print("> Number of estimated clusters: %d" % n_centers_)

    plot_meanshift(ms_data, cluster_centers, n_centers_)

    export_data(ms_data, "results/clusters.csv", cluster_centers, "results/centers.csv")
