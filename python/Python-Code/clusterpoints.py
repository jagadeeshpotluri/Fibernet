import sys
import math
import random
import copy
import matplotlib.pyplot as plt
import timeit
from mpl_toolkits.mplot3d import Axes3D

def lloydsmethod(inarr, numclusters):
    '''
    Uses lloyd's method to calculate an inexact k-means clustering. 
    '''
    #calculate centers
    centers = set()
    while len(centers) != numclusters: 
        centers.add(inarr[rolldice(len(inarr)-1)])

    clusterlist = assignclusters(centers,inarr)
    prevclusterlist = []
    means = computemeans(inarr, clusterlist)
    while clusterlist != prevclusterlist:
        prevclusterlist = copy.deepcopy(clusterlist)
        clusterlist = assignclusters(means, inarr)

        means = computemeans(inarr, clusterlist)


    return clusterlist


def lloyds_driver(inarr, numclusters):
    '''
    Drives the lloyd's method for 10,000 iterations, selecting
    the one with the best k-means clustering.
    This is a monty-carlo method, but one with a high level of accuracy.
    '''
    best_clustering = lloydsmethod(inarr, numclusters)
    min_kmeans = kmeanscost(inarr, best_clustering)

    for i in range(10000):
        curr_clustering = lloydsmethod(inarr, numclusters)
        curr_cost = kmeanscost(inarr, curr_clustering)
        if min_kmeans > curr_cost:
            best_clustering = copy.deepcopy(curr_clustering)
            min_kmeans = curr_cost

    return best_clustering




def computemeans(inarr, clusterlist):
    '''
    Compute the mean points of the clusters.
    '''
    clusteraverages = [[] for i in range(1 + max(clusterlist))]
    numinclusters = [0] * (1 + max(clusterlist))
    #print(clusterlist)
    for i, clusternum in enumerate(clusterlist):
        clusteraverages[clusternum].append(inarr[i])
        numinclusters[clusternum] += 1
    #print(clusteraverages)
    for i, cluster in enumerate(clusteraverages):
        #print(i)
        try:
            x = [0]*len(cluster[0])
        except IndexError:
            continue

        for point in cluster:

            for j, coordinate in enumerate(point):
                x[j] = x[j] + (coordinate / numinclusters[i])
        clusteraverages[i] = tuple(x)
    #print(clusteraverages)
    return clusteraverages



def assignclusters(centers, inarr):
    '''
    Assign the points to their nearest centers.
    '''
    outarr = list()

    for point in inarr:
        minval = float("inf")
        minloc = -1
        for i, center in enumerate(centers):
            #print(center, calcdist(center,point))
            newminval = min(calcdist(center,point),minval)
            if newminval < minval:
                minloc = i
                minval = newminval

        outarr.append(minloc)
    return outarr



def rolldice(max):
    '''gets a dice roll from 0 to the max.
    '''
    return random.randint(0,max)

def calcdist(latlon_i,latlon_j):
    """
    Function calculates distance between two
    coordinate points in km.
    """
    radius= 6373.0
    latitude_1 = math.radians(latlon_i[0])
    longitude_1 = math.radians(latlon_i[1])
    latitude_2 = math.radians(latlon_j[0])
    longitude_2 = math.radians(latlon_j[1])

    dlongitude = longitude_2 - longitude_1
    dlatitude = latitude_2 - latitude_1
    a = (math.sin(dlatitude/2))**2 + math.cos(latitude_1) * math.cos(latitude_2) * (math.sin(dlongitude/2))**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = radius * c
    return distance


def kmeanscost(inarr, clustering):
    '''
    Calculates the kmeans cost for a clustering.
    '''
    means = computemeans(inarr, clustering)
    finalcost = 0
    for cluster in set(clustering):
        clusterpoints = [x for i,x in enumerate(inarr) if clustering[i] == cluster]
        for point in clusterpoints:
            finalcost += (abs(calcdist(point, means[cluster]))**2)

    return finalcost


def loadfile(fp):
    '''
    Loads the file and outputs an array

    '''

    retlist = list()
    for line in fp:
        tup = tuple([float(x) for x in line.rstrip().split(',')])
        if tup != ():
            retlist.append(tup)
    return retlist

def plot2DCluster(inarr, clustering, showcenters = False, centerpt = (0,0)):
    '''
    Plots the 2D clustering of a set of points using matplotlib
    '''
    xpoints = [x[0] for x in inarr]
    ypoints = [y[1] for y in inarr]

    
    plt.scatter(ypoints, xpoints, c=clustering)
    plt.show()


def main(args):
    '''
    Main function that actually drives the program.
    '''
    if len(args) < 3:
        print("Need 3 args")
        return

    filepointer = open(str(args[1]))

    valarr = loadfile(filepointer)

    clarr = lloyds_driver(valarr, int(args[2]))
    fileslist = list()
    for i in range(max(clarr)+1):
        fileslist.append(open(str(i) + "_cluster.txt", 'w'))
    for i, point in enumerate(clarr):
        print(valarr[i][0], valarr[i][1], file = fileslist[point] )
    plot2DCluster(valarr, clarr)


    


if __name__ == '__main__':
    main(sys.argv)