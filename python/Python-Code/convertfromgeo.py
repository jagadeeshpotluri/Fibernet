'''
Created on Oct 20, 2014

This code takes house data from OSM files and converts it into a file
format readable by Concorde TSP.
'''

import shapefile
from math import sin, cos, sqrt, atan2, radians
import math
import sys



def uncalc_dist(latlon_b, xy_p):
    '''
    Function, using the xy distance from base point b, that will return the
    correct lat/lon for xy_p.
    '''

    R = 6373.0
    brng = math.atan2(xy_p[0], xy_p[1])
    d = math.sqrt(xy_p[0] ** 2 + xy_p[1] ** 2)  # Distance in km

    lat1 = math.radians(latlon_b[0])  # Current lat point converted to radians
    lon1 = math.radians(latlon_b[1])  # Current long point converted to radians

    lat2 = math.asin(math.sin(lat1) * math.cos(d / R) +
                     math.cos(lat1) * math.sin(d / R) * math.cos(brng))

    lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(d / R) * math.cos(lat1),
                             math.cos(d / R) - math.sin(lat1) * math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    return (lat2, lon2)


def latlong(houses):
    """
    function calculates midpoint of left and right corner of
    latitude and longitude of each houses.
    """
    latitude_longitude_list = list()
    coordinates = (0, 0)
    for shape in houses.iterShapes():
        coordinates = (((shape.bbox[1] + shape.bbox[3]) / 2),
                       ((shape.bbox[0] + shape.bbox[2]) / 2))
        latitude_longitude_list.append((coordinates))

        coordinates = (0, 0)

    return latitude_longitude_list



def calc_coords(latlons, point0):
    '''
    Calculates the lat lons from point0 using the xys given
    '''
    coordlist = list()
    for point in latlons:
        coordlist.append(uncalc_dist(point0, point))

    return coordlist


def gen_LLs():
    '''
    Opens the output file and reads it into an array.
    '''
    intpts = list()
    for line in open(sys.argv[1]):
        spln = line.split()
        intpts.append((float(spln[0]) / 1000, float(spln[1]) / 1000))
    return intpts


def main():
    '''
    Main function, runs the program that will convert from geosteiner points
    to lat lons.
    '''
    zero_pt = (30.38, -84.24)
    latlons = gen_LLs()
    coords = calc_coords(latlons, zero_pt)

    concorde_file = open(sys.argv[2], 'w')
    for coord in coords:
        print(coord[0], coord[1], file=concorde_file)


if __name__ == '__main__':
    main()
