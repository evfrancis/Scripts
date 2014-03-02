#!/usr/bin/python

import sys
import colorsys
import copy

from PIL import Image
from PIL import ImageFilter
from os import listdir
from os import remove
from os.path import isfile, join

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
    # Compute average color value
    for x in range(0,width):
        for y in range(0,height):
            r,g,b = p_img.getpixel((x,y))
            h,s,v = colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0)
            v_total += v

    v_avg = float(v_total) / (width * height)

    for x in range(0,width):
        for y in range(0,height):
            r,g,b = p_img.getpixel((x,y))
            h,s,v = colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0)
            r,g,b = colorsys.hsv_to_rgb(h,0,skew(v,5,v_avg))
            p_img.putpixel( (x,y), (int(r*255.0),int(g*255.0),int(b*255.0)))

    p_img = p_img.filter(ImageFilter.CONTOUR)
    return p_img


def process_image(im):
    width, height = im.size
    p_img = im

    # Compute average color value
    for l in range(1,10):
        level = l/10.0
        temp_img = p_img
        for x in range(0,width):
            for y in range(0,height):
                r,g,b = p_img.getpixel((x,y))
                h,s,v = colorsys.rgb_to_hsv(r/255.0,g/255.0,b/255.0)
                temp_img.putpixel((x,y),  (255,255,255))
                if (v > level):
                    temp_img.putpixel((x,y),  (r,g,b))
        write_image("/home/ev/Desktop/code/python/graphics_processing/Image_Processing/output" + str(l) + ".jpg",temp_img)

    v_total = 0;


    return p_img

PIL_Version = Image.VERSION

myPath = "./Image_Processing/";

# Remove old outputs
for f in listdir(myPath):
    if "output" in f:
        remove(join(myPath,f))

# Get inputs
image_array = sorted([f for f in listdir(myPath) ])

for img_file in image_array:
    image = read_image(join(myPath,img_file))
    print "Processing: %s" % img_file
    p_image = process_image(image)
    write_image(join(myPath,img_file.replace(".","_output.")),p_image)
