"""
SOPHIE WASHINGTON
CS1103 PROJECT 4
29 November 2018

This file acts as the View. It first interpolates points and lengths
in order to later translate heights and widths to create proportional
heights for translating into map coordinates given a width.

It also defines the style given for the data, either gradient or solid.

Finally, this file draws a polygon image and saves it as a PNG.
"""

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageColor import getrgb
import PIL
import region


class Plot:

    """
    Provides the ability to map, draw and color regions in a long/lat
    bounding box onto a proportionally scaled image.
    """
    @staticmethod
    def interpolate(x_1, x_2, x_3, newlength):
        """
        linearly interpolates x_2 <= x_1 <= x_3 into newlength
        x_2 and x_3 define a line segment, and x1 falls somewhere between them
        scale the width of the line segment to newlength, and return where
        x_1 falls on the scaled line.
        """
        proportion_x_1 = (x_1 - x_2)/(x_3 - x_2)
        new_x_1 = proportion_x_1*newlength
        return new_x_1


    @staticmethod
    def proportional_height(new_width, width, height):
        """
        return a height for new_width that is
        proportional to height with respect to width
        Yields:
            int: a new height
        """
        new_height = (height*new_width)/width
        return new_height


    @staticmethod
    def fill(region, style):
        """return the fill color for region according to the given 'style'"""
        if style == 'SOLID':
            return Plot.solid(region)
        if style == 'GRAD':
            return Plot.gradient(region)
        

    @staticmethod
    def solid(region):
        """
        a solid color based on a region's plurality of votes
        Args:
            region (Region): a region object
        Yields:
            (int, int, int): a triple (RGB values between 0 and 255)
        """
        if region.plurality() == 'REPUBLICAN':
            color = "RED"
        if region.plurality() == 'DEMOCRAT':
            color = "BLUE"
        if region.plurality() == 'OTHER':
            color = "GREEN"
        return PIL.ImageColor.getrgb(color)


    @staticmethod
    def gradient(region):
        """
        a gradient color based on percentages of votes in a region
        Args:
            region (Region): a region object
        Yields:
            (int, int, int): a triple (RGB values between 0 and 255)
        """
        RGB_VAL = 255
        red = region.republican_percentage()*RGB_VAL
        green = region.other_percentage()*RGB_VAL
        blue = region.democrat_percentage()*RGB_VAL
        color = (int(red), int(green), int(blue))
        return color


    def __init__(self, width, min_long, min_lat, max_long, max_lat):
        """
        Create a width x height image where height is proportional to width
        with respect to the long/lat coordinates.
        """
        self.width = width
        self.min_long = min_long
        self.min_lat = min_lat
        self.max_long = max_long
        self.max_lat = max_lat

        self.prop_height = int(self.proportional_height(width, max_long - min_long, max_lat - min_lat))

        self.vis = Image.new("RGB", (width, self.prop_height), (255, 255, 255))


    def save(self, filename):
        """save the current image to 'filename'"""
        self.vis.save(filename, "PNG")


    def draw(self, region, style):
        """
        Draws 'region' in the given 'style' at the correct position on the
        current image
        Args:
            region (Region): a Region object with a set of coordinates
            style (str): 'GRAD' or 'SOLID' to determine the polygon's fill
        """
        interpolated_lats = []
        lat_list = region.lats()
        for i in lat_list:
            trans_lat = self.prop_height - self.interpolate(i, self.min_lat, self.max_lat, self.prop_height)
            interpolated_lats.append(trans_lat)

        interpolated_longs = []
        long_list = region.longs()
        for j in long_list:
            trans_long = self.interpolate(j, self.min_long, self.max_long, self.width)
            interpolated_longs.append(trans_long)

        zipped = []
        coordinates = zip(interpolated_longs, interpolated_lats)
        for i in coordinates:
            zipped += i
              
        ImageDraw.Draw(self.vis).polygon(zipped, fill=self.fill(region, style), outline=None)


#Test code
#r = region.Region([(1,1),(2,2),(4,2),(3,5)], 100, 200,
#300)
#p = Plot(100,0,0,8,10)
#p.draw(r,"GRAD")
#p.save("example.png")

       





