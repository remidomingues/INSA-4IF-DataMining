import parser
import plot
from pandas import *
from numpy import array

from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs

def test():
    #Data
    centers = [[1, 1], [-1, -1], [1, -1]]
    X, _ = make_blobs(n_samples=10000, centers=centers, cluster_std=0.6)

    # Compute clustering with MeanShift
    # Parameters: data, quantile=radius max of the cluster, n_samples=minimum points per cluster
    bandwidth = estimate_bandwidth(X, quantile=0.92, n_samples=1000)

    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(X)

    plot.draw_meanshift(X, ms)


def run_meanshift(data):
    # Compute clustering with MeanShift
    bandwidth = estimate_bandwidth(data, quantile=0.002, n_samples=1000)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, min_bin_freq=30, cluster_all=False)
    ms.fit(data)

    return ms

if __name__ == "__main__":
    #test()

    df = pandas.read_csv(filepath_or_buffer="data.csv")  # Read the file
    ms_data = df[['longitude', 'latitude']].values

    ms = run_meanshift(data=ms_data)
    plot.draw_meanshift(data=ms_data, meanshift=ms)
