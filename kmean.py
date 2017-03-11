
import math
import random

def distance(a, b):
    if a.n != b.n:
        raise Exception("Error: non-comparable points")
    error = 0
    for i in range(a.n):
        error += (a.coords[i] - b.coords[i]) * (a.coords[i] - b.coords[i])
    dis = math.sqrt(error)
    return dis

class Point:
    '''
    A point in n dimensional space
    '''
    def __init__(self, coords):
        self.coords = coords
        self.n = len(coords)
    def display(self):
        for coord in self.coords:
            print(coord)

class Cluster:
    def __init__(self, points):
        if len(points) == 0:
            raise Exception("Error: empty cluster")
        self.points = points
        self.n = points[0].n
        for p in points:
            if p.n != self.n:
                raise Exception("Error: inconsistent dimension")
        self.centroid = self.calculateCentroid()
    def calculateCentroid(self):
        numPts = len(self.points)
        centroid = []
        for i in range(self.n):
            avg = 0
            for point in self.points:
                avg += point.coords[i]
            avg = float(avg) / numPts
            centroid.append(avg)
        return Point(centroid)
    def update(self, points):
        old = self.centroid
        self.points = points
        self.centroid = self.calculateCentroid()
        shift = distance(old, self.centroid)
        return shift

def create_random_point(n, low, high):
    p = Point([random.uniform(low, high) for _ in range(n)])
    return p


def kmean(points, k, minerr):
    # choose k random point in points
    count = 0
    initial = random.sample(points, k)
    clusters = [Cluster([p]) for p in initial]
    nClusters = len(clusters)


    while True:
        count = count + 1
        members = [[] for _ in clusters]
        for p in points:
            smallest_distance = distance(p, clusters[0].centroid)
            index = 0
            for i in range(nClusters - 1):
                dis = distance(p, clusters[i + 1].centroid)
                if dis < smallest_distance:
                    smallest_distance = dis
                    index = i + 1
            members[index].append(p)

        biggest_error = 0.0
        for i in range(nClusters):
            error = clusters[i].update(members[i])
            biggest_error = max(biggest_error, error)
        print(" iter %d -> error : %f" % (count, biggest_error))
        if biggest_error < minerr:
            print "Converge , number of iters: %d" % count
            break
    return clusters



def main():


    nPts = 20000
    dim = 2
    low = 0
    high = 1000
    nCluster = 100
    minerr = 0.3

    points = [create_random_point(dim, low, high) for i in range(nPts)]

    clusters = kmean(points, nCluster, minerr)



if __name__ == "__main__":
    main()

