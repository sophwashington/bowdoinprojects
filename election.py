"""
SOPHIE WASHINGTON
CS1103 PROJECT 4
29 November 2018

This file acts as the Controller, parsing the input data into
Region objects, using a Plot instance to draw and save each of these
regions onto an image.

It also uses the mercator function to translate our longitudinal
and latitudinal coordinates form a sphere onto a cylinder.
"""

import sys
import csv
import math
from region import Region
from plot import Plot


def mercator(lat):
    """project latitude 'lat' according to Mercator"""
    lat_rad = (lat * math.pi) / 180
    projection = math.log(math.tan((math.pi / 4) + (lat_rad / 2)))
    return (180 * projection) / math.pi


def main(results, boundaries, output, width, style):
    """
    Draws an image.
    This function creates an image object, constructs Region objects by reading
    in data from csv files, and draws polygons on the image based on those Regions

    Args:
        results (str): name of a csv file of election results
        boundaries (str): name of a csv file of geographic information
        output (str): name of a file to save the image
        width (int): width of the image
        style (str): either 'GRAD' or 'SOLID'
    """
    def check_int(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    region_list = []
    global_min_lats = []
    global_min_longs = []
    global_max_lats = []
    global_max_longs = []
    
    with open(results, 'r') as results_file, open(boundaries, 'r') as boundaries_file:
        bnd = csv.reader(boundaries_file)
        elc = csv.reader(results_file)
        
        for (co,st,r,d,o), boundary in zip(elc,bnd):
            float_bound = []
            for i in boundary[2:]:
                if check_int(i):
                    float_bound.append(float(i))
            coord = [(x, mercator(y)) for x,y in zip(float_bound[0::2], float_bound[1::2]) ]
            region_object = Region(coord, int(r), int(d), int(o))
            region_list.append(region_object)

        for region_object in region_list:
            global_min_lats.append(region_object.min_lat())
            global_min_longs.append(region_object.min_long())
            global_max_lats.append(region_object.max_lat())
            global_max_longs.append(region_object.max_long())

        min_global_long = min(global_min_longs)
        min_global_lat = min(global_min_lats)
        max_global_long = max(global_max_longs)
        max_global_lat = max(global_max_lats)

        map = Plot(width, min_global_long, min_global_lat, max_global_long, max_global_lat)
        
        for region_object in region_list:
            map.draw(region_object, style)

        map.save(output)
        
    results_file.close()
    boundaries_file.close()        



if __name__ == '__main__':
    results = sys.argv[1]
    boundaries = sys.argv[2]
    output = sys.argv[3]
    width = int(sys.argv[4])
    style = sys.argv[5]
    main(results, boundaries, output, width, style)
