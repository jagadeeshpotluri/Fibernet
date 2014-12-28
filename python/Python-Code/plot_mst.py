"""
  Plots the minimum spanning tree for FiberNet
"""

from math import sin, cos, sqrt, radians, asin
from mpl_toolkits.basemap import Basemap
from scipy.sparse import csgraph
import shapefile
import matplotlib.pyplot as plt
from tsp_solver.greedy import solve_tsp
import sys


def latlong():
    """
    function calculates midpoint of left and right corner of
    latitude and longitude of each houses.
    """
    latitude_longitude_list = []
    for line in open(sys.argv[3]):
        latitude_longitude_list.append((float(line.split()[0]),
                                        float(line.split()[1])))

    plot_mst(latitude_longitude_list, calc_mst(latitude_longitude_list))


def tsp_map_plot(latitude_longitude_list, path):
    """
    Function generates the optimal path traversal
    """
    x_coordinate_map = []
    y_coordinate_map = []
    file_roads = sys.argv[1]
    curr_map = Basemap(llcrnrlon=-84.25, llcrnrlat=30.38,
                       urcrnrlon=-84.2, urcrnrlat=30.42, projection='mill')
    plot_roads(curr_map, file_roads)
    dummy_path = []
    total_distance = 0
    for index in path:
        xpoints = []
        ypoints = []
        for i in range(2):
            xpoint, ypoint = curr_map(latitude_longitude_list[index[i]][1],
                                      latitude_longitude_list[index[i]][0])
            xpoints.append(xpoint)
            ypoints.append(ypoint)
        curr_map.plot(xpoints, ypoints, linewidth=0.5, color='r')

    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    fig.savefig(sys.argv[4])


def distance_between_two_points(latlon_i, latlon_j):
    """
    Function calculates distance between two
    coordinate points
    """
    radius = 6373.0
    latitude_1 = radians(latlon_i[0])
    longitude_1 = radians(latlon_i[1])
    latitude_2 = radians(latlon_j[0])
    longitude_2 = radians(latlon_j[1])

    dlongitude = longitude_2 - longitude_1
    dlatitude = latitude_2 - latitude_1
    a_value = (sin(dlatitude / 2)) ** 2 + cos(latitude_1) * \
        cos(latitude_2) * (sin(dlongitude / 2)) ** 2
    c_value = 2 * asin(sqrt(a_value))
    distance = radius * c_value
    return distance


def plot_roads(new_map, fileloc, drawboundsi=False):
    """
    Plotting roads on map
    """
    new_map.readshapefile(fileloc, "roads", drawbounds=drawboundsi)
    for shapedict, shape in zip(new_map.roads_info, new_map.roads):
        xx_value, yy_value = zip(*shape)
        new_map.plot(xx_value, yy_value, linewidth=1.5, color='k')

    new_map.readshapefile(sys.argv[2],
                          "polygon_highways_house", drawbounds=drawboundsi)
    for shapedict, shape in zip(new_map.polygon_highways_house_info,
                                new_map.polygon_highways_house):
        xx_value, yy_value = zip(*shape)
        new_map.plot(xx_value, yy_value, linewidth=0.5, color='k')


def calc_mst(latitude_longitude_list):
    '''
    Uses the Scipy Minimum Spanning Tree calculator to calculate a MST.
    '''
    single_row_entry = []
    distance_matrix = []
    distance = 0
    for i_value in range(0, len(latitude_longitude_list)):
        for j_value in range(0, len(latitude_longitude_list)):
            if i_value == j_value:
                single_row_entry.append(0)
            else:
                distance = distance_between_two_points(
                    latitude_longitude_list[i_value],
                    latitude_longitude_list[j_value])
                single_row_entry.append(distance)
        distance_matrix.append(single_row_entry)
        single_row_entry = []

    return (csgraph.minimum_spanning_tree(
        distance_matrix))


def plot_mst(latitude_longitude_list, mst_arr):
    '''
    Calculates and plots the minimum spanning tree of the given list. 
    '''
    arr_new = mst_arr.toarray()
    outarr = list()
    for i, row in enumerate(arr_new):
        for j, point in enumerate(row):

            if point != 0:
                outarr.append((i, j))
    tsp_map_plot(latitude_longitude_list, outarr)


if __name__ == '__main__':
    latlong()
