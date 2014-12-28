'''
This is a file that will run nosetests on the bulk of our work.

'''
import plot_clustering
import bindhousetoint
import clusterpoints
import plot_mst
import convertfromconcorde
import converttoconcorde

def test_distance():
    '''
    Tests calc_distance function from plot_clustering
    '''
    assert (plot_clustering.distance_between_two_points((0, 0),
                                                        (1, 0)) > 111 and
            plot_clustering.distance_between_two_points((0, 0), (1, 0)) < 112)


def test_calc_mst():
    '''
    Tests calc_mst for one set of points.
    '''

    points = [(0, 0), (1, 0)]
    mst_out = plot_clustering.calc_mst(points)
    assert (mst_out.sum() > 111 and mst_out.sum() < 112)


def test_find_closest():
    '''
    Tests find_closest from bindhousetoint
    '''
    print(bindhousetoint.find_closest([(0, 0)], [(1, 1)]))
    assert (bindhousetoint.find_closest([(0, 0)], [(1, 1)]) == (0.0, 0.0))


def test_lloydsdriver():
    '''
    Tests lloyd's driver from the clusterpoints.
    '''

    assert(clusterpoints.lloyds_driver([(0, 0)], 1) == [0])


def test_distance_plot_mst():
    '''
    Tests calc_distance function from plot_mst
    '''
    assert (plot_mst.distance_between_two_points((0, 0),
                                                 (1, 0)) > 111 and
            plot_mst.distance_between_two_points((0, 0), (1, 0)) < 112)


def test_calc_mst_plot():
    '''
    Tests calc_mst for one set of points from plot_msconvet
    '''

    points = [(0, 0), (1, 0)]
    mst_out = plot_mst.calc_mst(points)
    assert (mst_out.sum() > 111 and mst_out.sum() < 112)


def test_uncalc_dist():
    '''
    Tests uncalc_dist from convertfromconcorde
    '''
    xy = convertfromconcorde.uncalc_dist((0,0), (0,111.5))
    
    assert (xy[0] > 0.5 and xy[0] < 1.5) and xy[1]==0


def test_getxy():
    '''
    Tests getxydistance from converttoconcorde
    '''

    xy = converttoconcorde.getxydist((0,0),(1,0))
    assert (xy[1] > 111000 and xy[1] < 112000) and xy[0]==0

def test_calccoords():
    '''
    Tests calccoords from converttoconcorde
    '''

    xylist = converttoconcorde.calc_coords([(1,0)],(0,0))
    xy = xylist[0]
    assert (xy[1] > 111000 and xy[1] < 112000) and xy[0]==0

def test_writebody():
    '''
    tests write_concorde_body from converttoconcorde
    '''

    numwritten = converttoconcorde.write_concorde_body(open('testcov.txt',
        'w'), [(0,0)])
    assert numwritten == 1