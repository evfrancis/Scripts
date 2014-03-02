#!/usr/bin/python

import sys
import colorsys
import copy

from PIL import Image
from PIL import ImageFilter
from os import listdir
from os import remove
from os.path import isfile, join

myPath = "./Image_Processing/";

def read_image(path):
    return Image.open(path)

def write_image(path, Image):
    Image.save(path);

def base_function(x, exponent, midpoint):
    return (2 ** (exponent-1)) * ((x+0.5-midpoint) ** exponent)

def skew(x, exponent, midpoint):
    if x <= midpoint:
        return base_function(x, exponent, midpoint)
    elif x > midpoint and x < 1:
        return 1 - base_function(1-x,exponent, midpoint)
    else:
        return 1

def quantize(x,parts):
    return round(x*parts)/parts

def transform(im, width, height):
    s_total = 0
    # Compute average color value
    for x in range(0,width):
        for y in range(0,height):
            r,g,b = im.getpixel((x,y))
            h,s,v = colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0)
            s_total += s

    s_avg = float(s_total) / (width * height)

    for x in range(0,width):
        for y in range(0,height):
            r,g,b = im.getpixel((x,y))
            h,s,v = colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0)
            r,g,b = colorsys.hsv_to_rgb(h,skew(s,4,s_avg),v)
            im.putpixel( (x,y), (int(r*255.0),int(g*255.0),int(b*255.0)))

    im = im.filter(ImageFilter.CONTOUR)


def process_image(im):
    width, height = im.size
    p_img = im

    transform(im, width, height)

# Remove old outputs
for f in listdir(myPath):
    if "output" in f:
        remove(join(myPath,f))

# Get inputs
image_array = sorted([f for f in listdir(myPath) ])

for img_file in image_array:
    image = read_image(join(myPath,img_file))
    print "Processing: %s" % img_file
    process_image(image)
    write_image(join(myPath,img_file.replace(".","_output.")),image)
