'''
Goes through the House data and looks for the closest intersection point
to each of the four corners of the houses. This will then give us a baseline
to where we need to run the cables to.
'''
import plot_mst
import shapefile
import sys


def get_int_points():
    '''
    Goes through the house data and only appends the lat lon point.
    '''
    intpts = list()
    for line in open(sys.argv[1]):
        spln = line.split(',')
        intpts.append((spln[3], spln[2]))
    return intpts


def find_closest(housells, intpoints):
    '''
    finds the closest corner of the house to the intersection points.
    '''
    mindist = 999999
    minll = (0, 0)
    for ll in housells:
        for intpoint in intpoints:
            dist = plot_mst.distance_between_two_points(
                (float(ll[0]), float(ll[1])), (float(intpoint[0]),
                                               float(intpoint[1])))
            if dist < mindist:
                mindist = dist
                minll = (float(ll[0]), float(ll[1]))
    return minll


def closestpts_houses(houses, intpoints):
    '''
    Appends each of the corners of the house to generate the
    corners of house list.
    '''
    for shape in houses.iterShapes():
        housell = list()
        housell.append((shape.bbox[1], shape.bbox[0]))
        housell.append((shape.bbox[1], shape.bbox[2]))
        housell.append((shape.bbox[3], shape.bbox[0]))
        housell.append((shape.bbox[3], shape.bbox[2]))
        minll = find_closest(housell, intpoints)
        print(str(minll[0]) + "," + str(minll[1]))


def main():
    '''
    Main Function, uses hardcoded input.
    '''
    file_houses = sys.argv[2]
    sf_houses = shapefile.Reader(file_houses)
    intpts = get_int_points()
    closestpts_houses(sf_houses, intpts)


if __name__ == '__main__':
    main()
