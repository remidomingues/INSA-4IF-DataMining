import parser
import plot

from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs

def test():
    #Data
    centers = [[1, 1], [-1, -1], [1, -1]]
    X, _ = make_blobs(n_samples=10000, centers=centers, cluster_std=0.6)

    # Compute clustering with MeanShift
    # Parameters: data, quantile=radius max of the cluster, n_samples=minimum points per cluster
    bandwidth = estimate_bandwidth(X, quantile=0.2, n_samples=500)

    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(X)

    plot.draw_meanshift(X, ms)


def run_meanshift(data):
    print data[0]
    # Compute clustering with MeanShift
    # Parameters: data, quantile=radius max of the cluster, n_samples=minimum points per cluster
    
    #TODO; data class must be ndarray (cf numpy) => see other examples
    bandwidth = estimate_bandwidth(data, quantile=0.002, n_samples=30)
    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
    ms.fit(data)

    return ms


def get_ms_data(headers, data):
    ms_data = []
    lat_idx = headers['latitude']
    lon_idx = headers['longitude']

    for row in data:
        ms_data.append([row[lat_idx], row[lon_idx]])

    return ms_data


if __name__ == "__main__":
    test()

    headers, data = parser.parse_csv(filepath="data.csv", limit=5000)
    ms_data = get_ms_data(headers=headers, data=data)
    ms = run_meanshift(data=ms_data)
    plot.draw_meanshift(data=ms_data, meanshift=ms)
