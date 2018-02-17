import os
import math
from PIL import Image
import urllib2
import cStringIO
import numpy as np

class GoogleMapDownloader:
    """
        A class which generates high resolution google maps images given
        a longitude, latitude and zoom level
    """

    def __init__(self, lat, lng, zoom=12):
        """
            GoogleMapDownloader Constructor
            Args:
                lat:    The latitude of the location required
                lng:    The longitude of the location required
                zoom:   The zoom level of the location required, ranges from 0 - 23
                        defaults to 12
        """
        self._lat = lng
        self._lng = lat
        self._zoom = zoom

    def getXY(self):
        """
            Generates an X,Y tile coordinate based on the latitude, longitude
            and zoom level
            Returns:    An X,Y tile coordinate
        """

        tile_size = 256

        # Use a left shift to get the power of 2
        # i.e. a zoom level of 2 will have 2^2 = 4 tiles
        numTiles = 1 << self._zoom

        # Find the x_point given the longitude
        point_x = (tile_size / 2 + self._lng * tile_size / 360.0) * numTiles // tile_size

        # Convert the latitude to radians and take the sine
        sin_y = math.sin(self._lat * (math.pi / 180.0))

        # Calulate the y coorindate
        point_y = ((tile_size / 2) + 0.5 * math.log((1 + sin_y) / (1 - sin_y)) * -(
        tile_size / (2 * math.pi))) * numTiles // tile_size

        return int(point_x), int(point_y)

    def generateUrl(self, **kwargs):

        start_x,start_y = self.getXY()

        url = 'https://mt.google.com/vt/lyrs=s?x=' + str(start_x) + '&y=' + str(start_y) + '&z=' + str(
                    self._zoom)

        return url

    def saveImage(self,name):
        # print(self.generateUrl())
        imgdata = urllib2.urlopen(self.generateUrl()).read()
        img = Image.open(cStringIO.StringIO(imgdata))
        img.info["mew"]="lol"
        img.save(name)


from os import listdir
from os.path import isfile, join


def main1():
    data = np.genfromtxt('dataset.csv', delimiter=',', names=True)
    i=0
    zoom=20
    mypath = '.'
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    # for i in xrange(10000,21000):
    whoops = 0
    for i in xrange(21000):
        name = 'images/' + str(int(data[i]['class'])) + '/' + str(int(data[i]['name'])) + ".jpeg"
        if (name in files):
            print name, ' already done'
            continue
        if whoops>10:
            print 'bro change VPN server'
            break
        gmd = GoogleMapDownloader(data[i]['long'], data[i]['lat'], zoom)
        try:
            gmd.saveImage(name)
            print name, ' done'
        except:
            print "whoops"
            whoops += 1
            continue

# def main2():
#     data = np.genfromtxt('bu_pts.csv', delimiter=',', names=True)
#     i=0
#     zoom=19
#     for i in xrange(200):
#         gmd = GoogleMapDownloader(data[i]['long'],data[i]['lat'], zoom)
#         gmd.saveImage(str(int(data[i]['id']))+".jpeg")

main1()
