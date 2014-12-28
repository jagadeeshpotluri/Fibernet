'''
Created on Oct 20, 2014

This code takes house data from OSM files and converts it into a file
format readable by Concorde TSP. 
'''

import shapefile
from plot_mst import distance_between_two_points as calc_dist
from math import sin, cos, sqrt, atan2, radians
import sys


def latlong(houses):
    """
    function calculates midpoint of left and right corner of
    latitude and longitude of each houses.
    """
    latitude_longitude_list = list()
    coordinates=(0,0)
    for shape in houses.iterShapes(): 
        coordinates = (((shape.bbox[1]+shape.bbox[3])/2),
            ((shape.bbox[0]+shape.bbox[2])/2))
        latitude_longitude_list.append((coordinates))

        coordinates=(0,0)

    return latitude_longitude_list

def write_concorde_header(infile, name, comment, dimension):
    '''
    Writes the concorde header to the infile.
    '''
    print("NAME : " + name, file=infile)
    print("COMMENT : " + comment, file = infile)
    print("TYPE : TSP", file = infile)
    print("DIMENSION : " + str(dimension), file = infile)
    print("EDGE_WEIGHT_TYPE : EUC_2D", file = infile)
    print("NODE_COORD_SECTION",file = infile)

def write_concorde_body(infile, coords):
    '''
    Writes the body of the concorde file to infile
    '''
    outnum = 0
    for i, coord in enumerate(coords):
        print(str(i) + " " + str(round(coord[0])) + " " + 
            str(round(coord[1])), file = infile)
        pstr = str(round(coord[0])) + " " + str(round(coord[1]))
        fstr = "{: >4d}".format(round(coord[0]))
        sstr = "{: >4d}".format(round(coord[1]))
        print(" " + fstr + " " + sstr, file = infile)
        outnum = i + 1
    print("EOF", file = infile)
    return outnum


def getxydist(point1, point2):
    '''
    Calculates an x,y coordinate using point 1 as the origin
    And point 2 as the new coordinate. 
    '''

    xdist = calc_dist((point1), (point2[0], point1[1]))*1000
    ydist = calc_dist((point1), (point1[0], point2[1]))*1000

    return (ydist, xdist)


def calc_coords(latlons, point0):
    '''
    Calculates the x,y coordinates of a lat lon from the origin point0
    '''
    coordlist = list()
    for point in latlons:
        coordlist.append(getxydist(point0,point))

    return coordlist

def gen_LLs():
    '''
    Gets the latitude and longitudes from the given file into an array.
    '''
    intpts = list()
    for line in open(sys.argv[1]):
        spln = line.split(',')
        intpts.append((float(spln[0]),float(spln[1])))
    return intpts


def main():
    '''
    Main Function for the conversion.
    '''
    zero_pt = (30.38, -84.24)
    latlons = gen_LLs()
    coords = calc_coords(latlons, zero_pt)

    concorde_file = open(sys.argv[2], 'w')
    write_concorde_body(concorde_file, coords)

    
    


if __name__ == '__main__':
    main()