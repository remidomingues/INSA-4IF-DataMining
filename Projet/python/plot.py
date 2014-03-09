import numpy as np
import pylab as pl
from itertools import cycle

def draw_meanshift(data, meanshift):
    labels = meanshift.labels_
    cluster_centers = meanshift.cluster_centers_

    labels_unique = np.unique(labels)
    n_clusters_ = len(labels_unique)

    print("number of estimated clusters : %d" % n_clusters_)

    pl.figure(1)
    pl.clf()

    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    for k, col in zip(range(n_clusters_), colors):
        my_members = labels == k
        cluster_center = cluster_centers[k]
        pl.plot(data[my_members, 0], data[my_members, 1], col + '.')
        pl.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                markeredgecolor='k', markersize=14)
    pl.title('Estimated number of clusters: %d' % n_clusters_)
    pl.show()